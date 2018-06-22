#!/usr/bin/env python

#-*- encoding: utf-8 

'''
                      ______   ___  __
                     / ___\ \ / / |/ /
                    | |    \ V /| ' / 
                    | |___  | | | . \ 
                     \____| |_| |_|\_\
 ==========================================================================
@author: Yekun Chai

@license: School of Informatics, Edinburgh

@contact: s1718204@sms.ed.ac.uk

@file: Bootstrap.py

@time: 17/06/2018 21:00

@desc：       
               
'''
import codecs, logging, string, datetime
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from numba import jit
from collections import defaultdict

from baseline import Basic
from _config import *
from eval import *
from ie_utils import days_hours_mins_secs
from Bootstrapping.Seed import Seed
from Bootstrapping.Tuple import Tuple
from Bootstrapping.Definition import Definition
from Bootstrapping.Pattern import Pattern

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Bootstrap(Basic):
    def __init__(self, chunksize=10000):
        self.start_time = datetime.datetime.now()
        self.chunksize = chunksize
        self.tbl_name = 'UrbanDict'
        super(Bootstrap, self).__init__(chunksize=self.chunksize, sql=self.load_sql)

        self.patterns = list()
        self.candidate_patterns = list()

        self.seeds = list()
        self.candidate_tuples = list()

        self.iter_num = 0
        self.seeds_num = list()
        self.rec=[]
        self.prec=[]


    @property
    def load_sql(self):
        sql_loadUD = "SELECT defid, word, definition FROM %s" % self.tbl_name
        # sql_loadUD = "SELECT defid, word, definition FROM %s LIMIT 90000" % self.tbl_name
        # sql_loadUD = "SELECT defid, word, definition FROM %s WHERE word in ('ho', 'owned', 'owns', 'chode', 'cool')" % self.tbl_name
        # sql_loadUD = "SELECT defid, word, definition FROM UrbanDict WHERE defid=172638"
        return sql_loadUD

    def reset_generator(self):
        self.UD_data = pd.read_sql(sql=self.load_sql, con=self.conn, chunksize=self.chunksize)

    def reset_candidate_tuples(self):
        self.candidate_tuples = []

    def reset_candidate_pattern(self):
        self.candidate_patterns = []

    def init_bootstrap(self):
        # initialize seed instances from file
        self.read_init_seeds_from_file(seed_file=SEED_FILE)

        while self.iter_num < MAX_ITER:
            self.seeds_num.append(len(self.seeds))
            print("Iteratin num: {}, seed_num:{}".format(self.iter_num, self.seeds_num[self.iter_num]))
            # print("Pattern list: {}".format(self.patterns))
            print("Seed list: {}".format(self.seeds))
            print('-'*80)
            logger.info("Iteration {} starting...".format(self.iter_num))

            self.generate_pattern_from_seeds()
            # score metric
            self.score_candidate_pattern()
            self.get_seed_from_pattern()


            # if self.iter_num>1 and self.seeds_num[self.iter_num] == self.seeds_num[self.iter_num - 1]:
            #     print('Overall 0-{} iteration'.format(self.iter_num))
            #     break

            self.iter_log()
            self.iter_num = self.iter_num + 1

        # self.close_bootstrap()

    def read_init_seeds_from_file(self, seed_file=SEED_FILE):
        logger.info('Start reading initial seeds ...')
        with codecs.open(seed_file, mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                line_ = line.split()
                if len(line_) == 2:
                    tup_seed = Tuple(line_[0].lower(), line_[1].lower())
                    self.seeds.append(tup_seed)
            print("Initial {} seeds: {}".format(len(self.seeds), self.seeds))

    def generate_pattern_from_seeds(self):
        """
        Given seeds, generate patterns accordingly.
        :return:
        """
        logger.info('Iteration {}: start generating candidate patterns ...'.format(self.iter_num))
        if self.iter_num > 0:
            self.reset_generator()
            self.reset_candidate_pattern()

        # assert self.chunksize is not None, "Chunksize is None!! Assign a real number and continue:)"
        seed_words = [tup_.word for tup_ in self.seeds]
        for i, chunk in enumerate(self.UD_data):
            # print(chunk)
            df_word = chunk.ix[chunk['word'].str.lower().isin(seed_words)]
            for index, row in df_word.iterrows():
                defn_sents = row['definition']
                word = row['word'].lower()
                defid = row['defid']
                variant = self._find_variant_for_word(word)
                for defn_sent in sent_tokenize(defn_sents):
                    if len([tok for tok in word_tokenize(defn_sent) if tok not in '.,']) == 1: continue
                    defn = Definition(word, variant, defn_sent, defid)
                    if defn.match_seed is True and defn.isCtxValid is True:
                        # TODO: use pattern obj to count?
                        pat_ = Pattern(defn.ctx_bef, defn.ctx_aft)
                        if pat_ not in self.candidate_patterns:
                            self.candidate_patterns.append(pat_)
                        # print("Before Ctx: %s" % pat_.ctx_bef)
                        # print("After Ctx: %s" % pat_.ctx_aft)
                        continue
        logger.info("Iteration %s: \n %s candidate patterns: %s"
                    %
                    (self.iter_num, len(self.candidate_patterns), self.candidate_patterns)
        )

    def _find_variant_for_word(self, word):
        for seed in self.seeds:
        # for seed in self.processed_tuples:
            if word == seed.word:
                return seed.variant

    # TODO: score candidate patterns: RlogF metric
    def score_candidate_pattern(self):

        seeds_list = [(tup_.word, tup_.variant) for tup_ in self.seeds]

        for _, pat in enumerate(self.candidate_patterns):
            _ctx_bef = pat.ctx_bef
            # use mysql engine to search
            try:
                sql = "SELECT defid, word, definition FROM UrbanDict WHERE definition like '%%"+_ctx_bef+"%%'"
                pat_data = pd.read_sql(sql=sql, con=self.conn, chunksize=self.chunksize)
            except Exception as e:
                logger.warning("Ctx:%s \n Except: %s" % (_ctx_bef, e))
                continue

            for _, chunk in enumerate(pat_data):
                # print(chunk)
                for _, row in chunk.iterrows():
                    defn_sents = row['definition']
                    word = row['word'].lower()
                    defid = row['defid']

                    for defn_sent in sent_tokenize(defn_sents):
                        # print('*' * 80)
                        # print("start searching pattern %s: %s" % (i, pat))
                        pair = pat.ctx_match(defn_sent, word, seeds_list)
                        if pair is None:
                            continue
                        else:
                            # tup = Tuple(pair[0], pair[1])
                            #
                            # if tup not in self.candidate_tuples:
                            #     self.candidate_tuples.append(tup)
                            #
                            # # tuple score count
                            # if pat not in tup.pattern_list:
                            #     tup.pattern_list.append(pat)
                            #     tup.defid_list.append(defid)
                            # only match the first var
                            break
        for pat in self.candidate_patterns:
            pat.calc_pattern_score()

        self.candidate_patterns.sort(key=lambda p: p.overallscore, reverse=True)

        self.candidate_patterns = [p for p in self.candidate_patterns if p.overallscore > p.threshold]
        if len(self.candidate_patterns) <= N_pattern:
            # self.patterns += [p for p in self.candidate_patterns if p not in self.patterns]
            self.patterns = self.candidate_patterns
        else:
            # self.patterns += [p for p in self.candidate_patterns[:N_pattern] if p not in self.patterns]
            self.patterns = self.candidate_patterns[:N_pattern]

        for pat in self.patterns:
            print('#'*80)
            print("overall score of patterns:")
            print("pattern: %s" % pat)
            print("overallscore: %s" % pat.overallscore)
            print('-'*20)
            print("RlogF_score: %s" % pat.RlogF_score)
            print("match_seed_count: %s" % pat.match_seed_count)
            print("match_tot_count: %s" % pat.match_tot_count)
            print("candidate tuples: %s" % pat.tuples_list)

        save_iter(self.iter_num, self.candidate_patterns, 'candi_pat')
        save_iter(self.iter_num, self.patterns, 'pat')

        # logger.info("%s candidate seeds: %s" % (len(self.candidate_tuples), self.candidate_tuples))


        # filter out top tuples
    def get_seed_from_pattern(self):
        if self.iter_num > 0:
            self.reset_candidate_tuples()

        seeds_list = [(tup_.word, tup_.variant) for tup_ in self.seeds]
        # seeds_list = [(tup_.word, tup_.variant) for tup_ in self.processed_tuples]
        for _, pat in enumerate(self.patterns):
            _ctx_bef = pat.ctx_bef
            # use mysql engine to search
            try:
                sql = "SELECT defid, word, definition FROM UrbanDict WHERE definition like '%%" + _ctx_bef + "%%'"
                pat_data = pd.read_sql(sql=sql, con=self.conn, chunksize=self.chunksize)
            except Exception as e:
                logger.warning("Ctx:%s \n Except: %s" % (_ctx_bef, e))
                continue
            for _, chunk in enumerate(pat_data):
                # print(chunk)
                for _, row in chunk.iterrows():
                    defn_sents = row['definition']
                    word = row['word'].lower()
                    defid = row['defid']

                    for defn_sent in sent_tokenize(defn_sents):
                        # print('*' * 80)
                        # print("start searching pattern %s: %s" % (i, pat))
                        pair = pat.ctx_match(defn_sent, word, seeds_list)
                        if pair is None:
                            continue
                        else:
                            tup = Tuple(pair[0], pair[1])

                            if tup not in self.candidate_tuples:
                                self.candidate_tuples.append(tup)
                            else:
                                # if tuple exists, add `defid`
                                i = self.candidate_tuples.index(tup)
                                self.candidate_tuples[i].defid_list.append(defid)

                            # tuple score count
                            if pat not in tup.pattern_list:
                                tup.pattern_list.append(pat)
                                tup.defid_list.append(defid)
                            # only match the first variant
                            break

        # TODO: select top patterns, add to pattern, empty pattern pool

        for tup in self.candidate_tuples:
            tup.calc_tuple_score()

        self.candidate_tuples.sort(key=lambda t: t.overallscore, reverse=True)

        # self.candidate_tuples = [t for t in self.candidate_tuples if t.overallscore > t.threshold]

        rec = eval_recall([(t.word, t.variant) for t in self.candidate_tuples])
        self.rec.append(rec)

        if len(self.candidate_tuples) <= N_tuple:
            self.seeds += [tup for tup in self.candidate_tuples if tup not in self.seeds]
        else:
            self.seeds += [tup for tup in self.candidate_tuples[:N_tuple] if tup not in self.seeds]

        for t in self.seeds:
            print('='*80)
            print("score of tuples:")
            print("overall score of tuples: %s" % t.overallscore)
            print('-'*20)
            print("tuple: %s" % t)
            print("Numerator:", t.numerator)
            print("denom:", t.pattern_list)
            print("RlogF_entity_score: %s" % t.RlogF_ent_score)
            print("candidate patterns: %s" % t.pattern_list)

        save_iter(self.iter_num, self.seeds, 'tup')
        save_iter(self.iter_num, self.candidate_tuples, 'candi_tup')


    # def close_bootstrap(self):
    #     self.get_runtime()


    def iter_log(self):
        finish_time = datetime.datetime.now()
        timedelta = finish_time - self.start_time
        run_time = days_hours_mins_secs(timedelta)
        logger.info("Runtime:{}".format(run_time))
        logpath = os.path.join(EXP_DIR, 'logs')
        with open(logpath, 'a') as f:
            f.write("Iteration {}, runtime:{}, rec:{:.4f}, prec:{},seed_num: {}, pattern num: {}\n".
                format(self.iter_num, run_time, self.rec[self.iter_num], 'None',len(self.seeds), len(self.patterns))
            )



def main():
    bootstrap_ = Bootstrap(chunksize=10000)
    # test ===================================
    # bootstrap_.read_init_seeds_from_file()
    # bootstrap_.generate_pattern_from_seeds()
    # bootstrap_.score_candidate_pattern()
    # bootstrap_.get_seed_from_pattern()
    # bootstrap_.get_runtime()
    # test ===================================
    # start bootstrap
    bootstrap_.init_bootstrap()
    print('-'*100)
    # print("Candidate pattern list:", bootstrap_.patterns)
    # print("Candidate seed list:", bootstrap_.seeds)
    # bootstrap_ie.get_seed_from_pattern()

if __name__ == "__main__":
    main()
