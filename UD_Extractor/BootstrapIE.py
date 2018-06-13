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

@file: BootstrapIE.py

@time: 11/06/2018 20:50 

@desc：       
               
'''
import codecs, logging
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from numba import jit

from baseline import Basic
from _config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BootstrapIE(Basic):
    def __init__(self, chunksize=10000):
        self.chunksize = chunksize
        super(BootstrapIE, self).__init__(chunksize=self.chunksize, sql=self.load_sql)
        self.patterns = list()
        self.candidate_patterns = list()
        self.seeds = set()
        self.candidate_seeds = list()

        # start bootstrap
        self.init_bootstrap()


    @property
    def load_sql(self):
        db_name = 'UrbanDict'
        sql_loadUD = "SELECT defid, word, definition FROM %s" % db_name
        # sql_loadUD = "SELECT defid, word, definition FROM %s WHERE word in " \
        #              "('ur','looser','m8s','partay','peaple')" % db_name
        return sql_loadUD

    def reset_generator(self):
        self.UD_data = pd.read_sql(sql=self.load_sql, con=self.conn, chunksize=self.chunksize)

    def init_bootstrap(self):
        # initialize seed instances from file
        self.read_init_seeds_from_file(seed_file=SEED_FILE)
        self.generate_pattern_from_seeds()
        # TODO: score patterns
        self.patterns = self.candidate_patterns
        self.get_seed_from_pattern()
        # TODO: evaluate seeds
        # TODO: loop

    def read_init_seeds_from_file(self, seed_file=SEED_FILE):
        logger.info('Start reading initial seeds ...')
        seeds_init = set()
        with codecs.open(seed_file, mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                seed = line.split()
                if len(seed) == 2:
                    seeds_init.add((seed[0].lower(), seed[1].lower()))
            # print(seeds_init)
        self.seeds = seeds_init

    def generate_pattern_from_seeds(self):
        """
        Given seeds, generate patterns accordingly.
        :return:
        """
        logger.info('Start generating candidate patterns ...')
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
                variant_index_dict= self.get_index_of_varaint(defn_tokenized, seeds_dict[word])
                for sent_num, index_set in variant_index_dict.items():
                    defn_sent = defn_tokenized[sent_num]
                    for index in index_set:
                        variant = defn_sent[index]
                        lexico_context_before = defn_sent[:index]
                        lexico_context_after = defn_sent[index+1:]

                        lexico_pattern=[]
                        if enableAllContext:
                            lexico_pattern = lexico_context_before
                        elif usePreviousContext:
                            if len(lexico_context_before) >=CONTEXT_WINDOW_SIZE:
                                lexico_pattern = lexico_context_before[-CONTEXT_WINDOW_SIZE:]
                            else:
                                lexico_pattern = lexico_context_before
                        if len(lexico_pattern) > 0:
                            logger.info("Candidate pattern: %s" % lexico_pattern)
                            self.candidate_patterns.append(lexico_pattern)
            self.pattern_duplicate_removal()


    def get_index_of_varaint(self, defn_tokenized, variant_set):
        # k -> v:
        # sent_num: int -> index in each sent: set{}
        variant_index_dict = {}
        for sent_index, defn_sent in enumerate(defn_tokenized):
            variant_index_dict[sent_index] = []
            # collect all the variant occurrence
            for variant in variant_set:
                candidate_index_list = [i for i, tok in enumerate(defn_sent) if tok==variant]
            # if the variant occur once
            if len(candidate_index_list) == 1:
                variant_index_dict[sent_index].append(candidate_index_list[0])
            # variant appear multiple times, choose by the context quote symbol
            elif len(candidate_index_list) > 1:
                for index in candidate_index_list:
                    if defn_sent[index-1] in ('"', "'") and defn_sent[index+1] in ('"', "'"):
                        variant_index_dict[sent_index].append(candidate_index_list[0])
        return {k: v for k, v in variant_index_dict.items() if len(v)>0}

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
        pass

    # TODO
    def get_seed_from_pattern(self):
        # test
        # self.patterns = [['individuals', 'way', 'of', 'saying'],
        #                  ['moronic', 'abbreviation', 'for', '``']]
        logger.info('Start parsing candidate seeds ...')
        self.reset_generator()
        for i, chunk in enumerate(self.UD_data):
            # print(chunk)
            for index, row in chunk.iterrows():
                defn_tokenized = self.definition_tokenize(row['definition'])
                # print(defn_tokenized)
                for sent in defn_tokenized:
                    for sent_pattern in self.patterns:
                        var = self.simple_match_pattern(sent_pattern, sent)
                        if var is not None:
                            candidate_pair = (row['word'].lower(),var.lower())
                            self.candidate_seeds.append(candidate_pair)
                            print("matching pattern: {}".format(sent_pattern))
                            logger.info("Candidate pair: {}".format(candidate_pair))

    def simple_match_pattern(self, seed_pattern, definition):
        """
        simply match the pattern and
        :param seed_pattern: array, that contains 1 pattern
        :param definition: array, per definition sentence
        :return: candidate spelling variant if matched
        """
        len_pat = len(seed_pattern)
        for i in range(len(definition)-len_pat+1):
            if definition[i:i+len_pat] == seed_pattern:
                return definition[i+len_pat]


    # TODO: score candidate seeds
    def score_candidate_seed(self):
        pass


    def pattern_duplicate_removal(self):
        self.candidate_patterns = list(list(i) for i in set([tuple(t) for t in self.candidate_patterns]))

class Pattern(object):
    def __init__(self,seeds):
        self.seeds = seeds
        self.context_before = list()
        self.context_after = list()

    def _all_context(self):
        pass



if __name__ == "__main__":
    bootstrap_ie = BootstrapIE(chunksize=10000)
    seeds = bootstrap_ie.seeds
    print('-'*100)
    print("Candidate pattern list:", bootstrap_ie.candidate_patterns)
    print("Candidate seed list:", bootstrap_ie.candidate_seeds)
    # bootstrap_ie.get_seed_from_pattern()
    # target_dict = {}
    # for i, chunk in enumerate(bootstrap_ie.UD_data):
    #     print(chunk)
    #     for defid, word, definition in chunk.values:
    #         pass

