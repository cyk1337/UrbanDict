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
        super(Bootstrap, self).__init__(chunksize=self.chunksize, sql=self.load_sql)
        self.patterns = list()
        self.candidate_patterns = list()

        self.seeds = list()
        self.candidate_seeds = list()
        # self.candidate_seeds = defaultdict(list)

        self.iter_num = 0
        self.seeds_num = list()


    @property
    def load_sql(self):
        db_name = 'UrbanDict'
        sql_loadUD = "SELECT defid, word, definition FROM %s" % db_name
        # sql_loadUD = "SELECT defid, word, definition FROM %s WHERE word in ('ur','looser','m8s','partay','peaple')" % db_name
        return sql_loadUD

    def reset_generator(self):
        self.UD_data = pd.read_sql(sql=self.load_sql, con=self.conn, chunksize=self.chunksize)

    def reset_candidate_seeds(self):
        self.candidate_seeds = []

    def reset_candidate_pattern(self):
        self.candidate_patterns = []

    def init_bootstrap(self):
        # initialize seed instances from file
        self.read_init_seeds_from_file(seed_file=SEED_FILE)

        while self.iter_num <= MAX_ITER:
            self.seeds_num.append(len(self.seeds))
            print("Iteratin num: {}, seed_num:{}".format(self.iter_num, self.seeds_num[self.iter_num]))
            print("*"*80)
            # print("Pattern list: {}".format(self.patterns))
            print("Seed list: {}".format(self.seeds))
            print('-'*80)
            logger.info("Iteration {} starting...".format(self.iter_num))

            self.generate_pattern_from_seeds()

            # TODO: score patterns
            self.score_candidate_pattern()
            self.get_seed_from_pattern()
            # TODO: evaluate seeds
            self.score_candidate_seed()

            if self.iter_num>1 and self.seeds_num[self.iter_num] == self.seeds_num[self.iter_num - 1]:
                print('Overall 0-{} iteration'.format(self.iter_num))
                break
            self.iter_num = self.iter_num + 1

        self.close_bootstrap()


    def read_init_seeds_from_file(self, seed_file=SEED_FILE):
        logger.info('Start reading initial seeds ...')
        with codecs.open(seed_file, mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                line_ = line.split()
                if len(line_) == 2:
                    tup_seed = Seed(line_[0].lower(), line_[1].lower())
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

        for i, chunk in enumerate(self.UD_data):
            # print(chunk)
            seed_words = [tup_.word for tup_ in self.seeds]

            df_word = chunk.ix[chunk['word'].str.lower().isin(seed_words)]
            for index, row in df_word.iterrows():
                defn_sents = row['definition']
                word = row['word'].lower()
                defid = row['defid']
                variant = self._find_variant_for_word(word)
                for defn_sent in sent_tokenize(defn_sents):
                    defn = Definition(word, variant, defn_sent, defid)
                    if defn.match_seed is True and defn.isCtxValid is True:
                        # TODO: use pattern obj to count?
                        pat_ = Pattern(defn.ctx_bef, defn.ctx_aft)
                        self.candidate_patterns.append(pat_)
                        # print("Before Ctx: %s" % pat_.ctx_bef)
                        # print("After Ctx: %s" % pat_.ctx_aft)
        logger.info("Iteration %s: \n candidate patterns: %s" % (self.iter_num,self.candidate_patterns))

    def _find_variant_for_word(self, word):
        for seed in self.seeds:
            if word == seed.word:
                return seed.variant

    # def get_index_of_varaint(self, defn_tokenized, variant_set):
    #     # k -> v:
    #     # sent_num: int -> index in each sent: set{}
    #     variant_index_dict = {}
    #     for sent_index, defn_sent in enumerate(defn_tokenized):
    #         variant_index_dict[sent_index] = []
    #         # collect all the variant occurrence
    #         for variant in variant_set:
    #             candidate_index_list = [i for i, tok in enumerate(defn_sent) if tok==variant]
    #             # if the variant occur once
    #             if len(candidate_index_list) == 1:
    #                 variant_index_dict[sent_index].append(candidate_index_list[0])
    #             # variant appear multiple times, choose by the context quote symbol
    #             elif len(candidate_index_list) > 1:
    #                 for index in candidate_index_list:
    #                     if defn_sent[index-1] in ('"', "'", "``") and len(defn_sent)>= index+1 and defn_sent[index+1] in ('"', "'", "``"):
    #                         variant_index_dict[sent_index].append(candidate_index_list[0])
    #     return {k: v for k, v in variant_index_dict.items() if len(v)>0}


    # def definition_tokenize(self, definition):
    #     """
    #     tokenize definition sentences,
    #     :param definition: definition sentences
    #     :return: 2-dim array, each inside array represents a sentence.
    #     """
    #     defn_tokenized = []
    #     sent_list = sent_tokenize(definition)
    #     for sent in sent_list:
    #         defn_tokenized.append([tok.lower() for tok in word_tokenize(sent)])
    #     return defn_tokenized

    # TODO: score candidate patterns
    def score_candidate_pattern(self):

        # self.reset_candidate_seeds()

        for i, pat in enumerate(self.candidate_patterns):
            print('*'*80)
            print("start searching pattern %s: %s" % (i,pat))
            self.reset_generator()
            for i, chunk in enumerate(self.UD_data):
                # print(chunk)
                for index, row in chunk.iterrows():
                    defn_sents = row['definition']
                    word = row['word'].lower()
                    for defn_sent in sent_tokenize(defn_sents):
                        pair = pat.ctx_match(defn_sent, word)
                        if pair is not None and pair not in self.candidate_seeds:
                            self.candidate_seeds.append(pair)
        logger.info("Candidate seeds: %s" % self.candidate_seeds)



        # for pat in self.candidate_patterns:
        #     if self.pattern_filter(pat) is False:
        #         self.candidate_patterns.remove(pat)
        # self.patterns = self.patterns+self.candidate_patterns
        # self.pattern_duplicate_removal

    # TODO
    def get_seed_from_pattern(self):
        # test
        # self.patterns = [['individuals', 'way', 'of', 'saying'],
        #                  ['moronic', 'abbreviation', 'for', '``']]
        logger.info('Iteration {}: start parsing candidate seeds ...'.format(self.iter_num))

        self.reset_generator()
        # self.reset_candidate_seeds()

        for i, chunk in enumerate(self.UD_data):
            # print(chunk)
            for index, row in chunk.iterrows():
                # TODO: match definition
                row['definition']
                # defn_tokenized = self.definition_tokenize()
                # print(defn_tokenized)
                # for sent in defn_tokenized:
                #     for sent_pattern in self.candidate_patterns:
                #         var = self.surface_match_pattern(sent_pattern, sent)
                #         if var is not None:
                #             candidate_pair = (row['word'].lower(),var.lower())
                #             self.candidate_seeds.append(candidate_pair)
                #             print("matching pattern: {}".format(sent_pattern))
                #             logger.info("Candidate pair: {}".format(candidate_pair))
        # self.seed_duplicate_removal()


    def surface_match_pattern(self, seed_pattern, definition):
        """
        simply match the pattern and
        :param seed_pattern: array, that contains 1 pattern
        :param definition: array, per definition sentence
        :return: candidate spelling variant if matched
        """
        len_pat = len(seed_pattern)
        len_defn = len(definition)
        for i in range(len_defn-len_pat+1):
            if definition[i:i+len_pat] == seed_pattern and len_defn > i+len_pat:
                var = definition[i+len_pat]
                if self.variant_filter(var):
                    return var

    def variant_filter(self, candidate_variant):
        filter_list = string.punctuation + '``'
        if candidate_variant in filter_list:
            return False
        else:
            return True

    def pattern_filter(self, candidate_pattern):
         # TODO: discard contexts that contains only 2 or fewer stopwords,
         # allowing at most 2 stopwords in context
        # TODO: ﻿create flexible patterns by ignoring the words {‘a’, ‘an’, ‘the’, ‘,’, ‘.’}
        #  TODO: with and without POS tag restrictionnof ﻿target(e.g. contains Nouns)
        non_pat_list = ['synonym',]
        for non_pat in non_pat_list:
            if non_pat in candidate_pattern:
                print("Remove pattern: {}".format(candidate_pattern))
                return False
            elif len(candidate_pattern)==1 and 'meaning' not in candidate_pattern:
                return False
            else:
                for tok in candidate_pattern:
                    if tok in ['a', 'an', 'the', ',', '.', 'or', '``', 'has', 'extreme2']:
                        candidate_pattern.remove(tok)
                if len(candidate_pattern) > 0:
                    return True
                else:
                    return False

    # TODO: score candidate seeds
    def score_candidate_seed(self):
        self.seeds = self.seeds + self.candidate_seeds
        self.seed_duplicate_removal()


    def pattern_duplicate_removal(self):
        self.candidate_patterns = list(list(i) for i in set([tuple(t) for t in self.candidate_patterns]))
        self.patterns = list(list(i) for i in set([tuple(t) for t in self.patterns]))

    def seed_duplicate_removal(self):
        self.candidate_seeds = list(set([tuple(t) for t in self.candidate_seeds]))
        self.seeds = list(set([tuple(t) for t in self.seeds]))

    def close_bootstrap(self):
        self.get_runtime()


    def get_runtime(self):
        finish_time = datetime.datetime.now()
        timedelta = finish_time - self.start_time
        run_time = days_hours_mins_secs(timedelta)
        logger.info("Runtime:{}".format(run_time))


def main():
    bootstrap_ = Bootstrap(chunksize=10000)
    bootstrap_.read_init_seeds_from_file()
    bootstrap_.generate_pattern_from_seeds()
    bootstrap_.score_candidate_pattern()
    # bootstrap_.get_seed_from_pattern()
    # candidate_patterns = bootstrap_.candidate_patterns

    # start bootstrap
    # bootstrap_ie.init_bootstrap()
    print('-'*100)
    # print("Candidate pattern list:", bootstrap_.patterns)
    # print("Candidate seed list:", bootstrap_.seeds)
    # bootstrap_ie.get_seed_from_pattern()


if __name__ == "__main__":
    main()
