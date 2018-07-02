#!/usr/bin/env python

# -*- encoding: utf-8

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

@file: BootstrapIE.py

@time: 11/06/2018 20:50 

@desc：       
               
'''
import codecs, logging, string, datetime
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from numba import jit

from baseline import Basic
from _config import *
from ie_utils import days_hours_mins_secs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BootstrapIE(Basic):
    def __init__(self, chunksize=10000):
        self.start_time = datetime.datetime.now()
        self.chunksize = chunksize
        super(BootstrapIE, self).__init__(chunksize=self.chunksize, sql=self.load_sql)
        self.patterns = list()
        self.candidate_patterns = list()
        self.seeds = list()
        self.candidate_seeds = list()
        self.iter_num = 0
        self.seeds_num = list()

    @property
    def load_sql(self):
        db_name = 'UrbanDict'
        # sql_loadUD = "SELECT defid, word, definition FROM %s" % db_name
        sql_loadUD = "SELECT defid, word, definition FROM %s WHERE word in " \
                     "('ur','looser','m8s','partay','peaple')" % db_name
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

        while True:
            self.seeds_num.append(len(self.seeds))
            print("Iteratin num: {}, seed_num:{}".format(self.iter_num, self.seeds_num[self.iter_num]))
            print("*" * 80)
            print("Pattern list: {}".format(self.patterns))
            print("Seed list: {}".format(self.seeds))
            print('-' * 80)
            logger.info("Iteration {} starting...".format(self.iter_num))

            self.generate_pattern_from_seeds()

            # TODO: score patterns
            self.score_candidate_pattern()
            self.get_seed_from_pattern()
            # TODO: evaluate seeds
            self.score_candidate_seed()

            if self.iter_num > 1 and self.seeds_num[self.iter_num] == self.seeds_num[self.iter_num - 1]:
                print('Overall 0-{} iteration'.format(self.iter_num))
                break
            self.iter_num = self.iter_num + 1

        self.close_bootstrap()

    def read_init_seeds_from_file(self, seed_file=SEED_FILE):
        logger.info('Start reading initial seeds ...')
        seeds_init = list()
        with codecs.open(seed_file, mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                seed = line.split()
                if len(seed) == 2:
                    seeds_init.append((seed[0].lower(), seed[1].lower()))
            # print(seeds_init)
        self.seeds = seeds_init

    def generate_pattern_from_seeds(self):
        """
        Given seeds, generate patterns accordingly.
        :return:
        """
        logger.info('Iteration {}: start generating candidate patterns ...'.format(self.iter_num))
        if self.iter_num > 0:
            self.reset_generator()
            self.reset_candidate_pattern()
        # seed_words = [seed_tuple[0] for seed_tuple in self.seeds]
        # seed_variants = [seed_tuple[1] for seed_tuple in self.seeds]
        seeds_dict = dict()
        for seed_tuple in self.seeds:
            seeds_dict[seed_tuple[0]] = set()
            seeds_dict[seed_tuple[0]].add(seed_tuple[1])

        seed_words = list(seeds_dict.keys())

        assert self.chunksize is not None, "Chunksize is None!! Assign a real number and continue:)"

        for i, chunk in enumerate(self.UD_data):
            # print(chunk)
            df_word = chunk.ix[chunk['word'].str.lower().isin(seed_words)]
            for index, row in df_word.iterrows():
                defn_tokenized = self.definition_tokenize(row['definition'])
                print(defn_tokenized)
                word = row.at['word'].lower()
                variant_index_dict = self.get_index_of_varaint(defn_tokenized, seeds_dict[word])
                for sent_num, index_set in variant_index_dict.items():
                    defn_sent = defn_tokenized[sent_num]
                    for index in index_set:
                        variant = defn_sent[index]
                        lexico_context_before = defn_sent[:index]
                        lexico_context_after = defn_sent[index + 1:]

                        lexico_pattern = []
                        if useBothContext:
                            lexico_pattern = lexico_context_before
                        elif usePreviousContext:
                            if len(lexico_context_before) >= CTX_SIZE:
                                lexico_pattern = lexico_context_before[-CTX_SIZE:]
                            else:
                                lexico_pattern = lexico_context_before
                        if len(lexico_pattern) > 0:
                            logger.info("Candidate pattern: %s" % lexico_pattern)
                            self.candidate_patterns.append(lexico_pattern)
            # self.pattern_duplicate_removal()

    def get_index_of_varaint(self, defn_tokenized, variant_set):
        # k -> v:
        # sent_num: int -> index in each sent: set{}
        variant_index_dict = {}
        for sent_index, defn_sent in enumerate(defn_tokenized):
            variant_index_dict[sent_index] = []
            # collect all the variant occurrence
            for variant in variant_set:
                candidate_index_list = [i for i, tok in enumerate(defn_sent) if tok == variant]
                # if the variant occur once
                if len(candidate_index_list) == 1:
                    variant_index_dict[sent_index].append(candidate_index_list[0])
                # variant appear multiple times, choose by the context quote symbol
                elif len(candidate_index_list) > 1:
                    for index in candidate_index_list:
                        if defn_sent[index - 1] in ('"', "'", "``") and len(defn_sent) >= index + 1 and defn_sent[
                            index + 1] in ('"', "'", "``"):
                            variant_index_dict[sent_index].append(candidate_index_list[0])
        return {k: v for k, v in variant_index_dict.items() if len(v) > 0}

    def definition_tokenize(self, definition):
        """
        tokenize definition sentences,
        :param definition: definition sentences
        :return: 2-dim array, each inside array represents a sentence.
        """
        defn_tokenized = []
        sent_list = sent_tokenize(definition)
        for sent in sent_list:
            defn_tokenized.append([tok.lower() for tok in word_tokenize(sent)])
        return defn_tokenized

    # TODO: score candidate patterns
    def score_candidate_pattern(self):

        for pat in self.candidate_patterns:
            if self.pattern_filter(pat) is False:
                self.candidate_patterns.remove(pat)
        self.patterns = self.patterns + self.candidate_patterns
        self.pattern_duplicate_removal()

    # TODO
    def get_seed_from_pattern(self):
        # test
        # self.patterns = [['individuals', 'way', 'of', 'saying'],
        #                  ['moronic', 'abbreviation', 'for', '``']]
        logger.info('Iteration {}: start parsing candidate seeds ...'.format(self.iter_num))

        self.reset_generator()
        self.reset_candidate_seeds()

        for i, chunk in enumerate(self.UD_data):
            # print(chunk)
            for index, row in chunk.iterrows():
                defn_tokenized = self.definition_tokenize(row['definition'])
                # print(defn_tokenized)
                for sent in defn_tokenized:
                    for sent_pattern in self.candidate_patterns:
                        var = self.surface_match_pattern(sent_pattern, sent)
                        if var is not None:
                            candidate_pair = (row['word'].lower(), var.lower())
                            self.candidate_seeds.append(candidate_pair)
                            print("matching pattern: {}".format(sent_pattern))
                            logger.info("Candidate pair: {}".format(candidate_pair))
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
        for i in range(len_defn - len_pat + 1):
            if definition[i:i + len_pat] == seed_pattern and len_defn > i + len_pat:
                var = definition[i + len_pat]
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
        non_pat_list = ['synonym', ]
        for non_pat in non_pat_list:
            if non_pat in candidate_pattern:
                print("Remove pattern: {}".format(candidate_pattern))
                return False
            elif len(candidate_pattern) == 1 and 'meaning' not in candidate_pattern:
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
    bootstrap_ie = BootstrapIE(chunksize=10000)
    seeds = bootstrap_ie.seeds
    # start bootstrap
    bootstrap_ie.init_bootstrap()
    print('-' * 100)
    print("Candidate pattern list:", bootstrap_ie.patterns)
    print("Candidate seed list:", bootstrap_ie.seeds)
    # bootstrap_ie.get_seed_from_pattern()


if __name__ == "__main__":
    main()
