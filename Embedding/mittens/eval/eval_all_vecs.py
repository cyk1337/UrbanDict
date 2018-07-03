# import os
# import re
# import numpy as np
# import sys
# from collections import defaultdict
# from glove import Glove,metrics
# from scipy.stats.stats import pearsonr
#
# X = {}
# X["goog_sem"] = {}
# X["goog_syn"] = {}
# X["goog_tot"] = {}
# ydatavec = {}
# X["MEN"] = {}
# X["SCWS"] = {}
# X["RW"] = {}
# X["SIMLEX"] = {}
#
# rootdir = '/home/naomi/data/mittens/vectors'
# fileregex = re.compile(r"vectors_(.+)_5.it.*_*formal([01]\.[012468])00000_d300\.bin")
# lineregex = re.compile(r"Questions seen/total:.*" + "\n.*" +
#                        r"Semantic Accuracy: (\d+\.\d+)% .+" + "\n.*" +
#                        r"Syntactic Accuracy: (\d+\.\d+)% .+" + "\n.*" +
#                        r"Total Accuracy: (\d+\.\d+)% .+" + "\n")
# rankmax = 6
#
# def similarities_from_file(fh):
#     lines = fh.readlines()
#     similarities = [None for line in lines]
#     for (i, line) in enumerate(lines):
#         line = line.strip().split()
#         similarities[i] = (line[0], line[1], float(line[2]))
#     return similarities
#
# similarity_sets = {}
# with open("/home/naomi/data/mittens/analogy/MEN.txt") as fh:
#     similarity_sets["MEN"] = similarities_from_file(fh)
# with open("/home/naomi/data/mittens/analogy/simlex_simplified.txt") as fh:
#     similarity_sets["SIMLEX"] = similarities_from_file(fh)
# with open("/home/naomi/data/mittens/analogy/rw_simplified.txt") as fh:
#     similarity_sets["RW"] = similarities_from_file(fh)
# with open("/home/naomi/data/mittens/analogy/scws_simplified.txt") as fh:
#     similarity_sets["SCWS"] = similarities_from_file(fh)
#
# def normalized_vsm(word, model):
#     vsm = model.word_vectors[model.dictionary[word]]
#     return vsm / np.linalg.norm(vsm)
#
# def word_similarity(v1, v2, model):
#     return np.dot(normalized_vsm(v1, model), normalized_vsm(v2, model))
#
# def has_vocab_list(vocab, model):
#     for v in vocab:
#         if v not in model.dictionary:
#             return False
#     return True
#
# def evaluate_corr(testset, model):
#     sims_tmp = filter(lambda (v1,v2,simscore): has_vocab_list([v1, v2], model), similarity_sets[testset])
#     simscores_gold = [x[2] for x in sims_tmp]
#     simscores_test = [word_similarity(v1, v2, model) for (v1, v2, simscore) in sims_tmp]
#     return pearsonr(simscores_gold, simscores_test)[0]
#
# def score_top_ranks(ranks_, min_correct_rank=0):
#     ranks = np.hstack(ranks_)
#     return len(filter(lambda x: x <= min_correct_rank, ranks))/float(len(ranks))
#
# def evaluate_analogy_scores(prefix, results, model, analogy_dir):
#     syn_ranks = []
#     sem_ranks = []
#     sections = defaultdict(list)
#     for fname in os.listdir(analogy_dir):
#         with open(os.path.join(analogy_dir, fname)) as f:
#             for words in f.readlines():
#                 w = unicode(words).strip().split()
#                 assert(len(w)) == 4
#                 sections[fname].append(w) # TODO encode
#
#     for section, words in sections.items():
#         evaluation_ids = metrics.construct_analogy_test_set(words,
#                                                             model.dictionary,
#                                                             ignore_missing=True)
#
#         # Get the rank array.
#         ranks = metrics.analogy_rank_score(evaluation_ids, model.word_vectors,
#                                            no_threads=8) # TODO make arg
#
#         if section.startswith('gram'):
#             syn_ranks.append(ranks)
#         else:
#             sem_ranks.append(ranks)
#         # results['%s-%s' % (prefix, section)] = (ranks == 0).sum() / float(len(ranks))
#
#     results['%s-sem' % prefix] = score_top_ranks(sem_ranks)
#     results['%s-syn' % prefix] = score_top_ranks(syn_ranks)
#     results['%s-total' % prefix] = score_top_ranks(sem_ranks + syn_ranks)
#
# def run_all_evals(vecf, twitter_eval=True, keepmodel=False):
#     print >> sys.stderr, 'vector file: %s' % vecf
#     results = {}
#     ydata = Glove.load_stanford(vecf)
#
#     most_sim = ydata.most_similar('u', rankmax)
#     print most_sim
#
#     evaluate_analogy_scores('goog', results, ydata, 'eval/question-data')
#     evaluate_analogy_scores('goog.nohashtag', results, ydata, 'eval/nohashtag_filtered_question-data')
#     if twitter_eval:
#         evaluate_analogy_scores('goog.hashtag', results, ydata, 'eval/hashtag_filtered_question-data')
#
#     for testset in similarity_sets.keys():
#         results[testset] = "%f" % evaluate_corr(testset, ydata)
#
#     if keepmodel:
#         return (ydata, results)
#     else:
#         return (most_sim, results)
#
# #formal_baseline_fh = '/export/a13/nsaphra/coe_export/lower_glove/formal/'
# #twitter_baseline_fh = '/export/a13/nsaphra/coe_export/lower_glove/'
#
# #(formal_ydata, formal_X) = run_all_evals(os.path.join(formal_baseline_fh, 'vectors_d300.bin'),
# #                                         os.path.join(formal_baseline_fh, 'vocab.txt'))
# #(twitter_ydata, twitter_X) = run_all_evals(os.path.join(twitter_baseline_fh, 'vectors_d300.bin'),
# #                                         os.path.join(twitter_baseline_fh, 'vocab.txt'))
#
# def get_table_line(name, results_dict, ordered_keys=None):
#     if not ordered_keys:
#         ordered_keys = results_dict.keys()
#     norm_result = lambda x: x if x > 10 else x * 100
#     return name + " & " + " & ".join(["%.3g" % norm_result(float(results_dict[k])) for k in ordered_keys])
#
# def totable(xvals):
#     sims_length = lambda (testset, model): \
#         len(filter(lambda (v1,v2,simscore): \
#                        v1 in model.dictionary and v2 in model.dictionary,
#                    similarity_sets[testset]))
#     dflt_mode = X["T_sem"].keys()[0]
#     print("Corpus & Total" + " & ".join(["%f" % f for f in xvals]) + r"\\")
#     for testset in similarity_sets.keys():
#         recall1 = ["" for xval in xvals]
#         recall2 = ["" for xval in xvals]
#         for (i,xval) in enumerate(xvals):
#             l = sims_length((testset, ydatavec[dflt_mode][xval]))
#             recall1[i] = "%d" % l
#             recall2[i] = "(%.2g" % (float(l) * 100 / len(similarity_sets[testset])) + r"\%)"
#         print("%s & %d & " % (testset, len(similarity_sets[testset])) + " & ".join(recall1) + r"\\")
#         print(" &  & " + " & ".join(recall2) + r"\\")
#
# def totable_simple(results_dict, ordered_keys=None):
#     if not ordered_keys:
#         dict.items()[0][1]
#         ordered_keys = sampler.keys()
#     print "method & " + " & ".join(ordered_keys) + r"\\"
#     for (fname, d2) in results_dict.items():
#         print get_table_line(fname, d2, ordered_keys) + r"\\"
#
# def tochart(chartname, d):
#     cats = []
#     xs = []
#     ys = []
#     for (category,d2) in sorted(d.items()):
#         d2sort = sorted(d2.keys())
#         cats += ["\"%s\"" % category for x in d2sort]
#         xs += ["\"%.2g\"" % x for x in d2sort]
#         ys += [d2[x] for x in d2sort]
#     print("X[\"%s\"] = DataFrame(" % chartname)
#     print("    proportion = [" + ", ".join(xs) + "],")
#     print("    stats = [" + ", ".join(ys) + "],")
#     print("    mode = [" + ", ".join(cats) + "]")
#     print(");")
#
# def tohistogram(d, keepmodels=False):
#     modes = []
#     xs = []
#     ranks = []
#     for (mode,d2) in sorted(d.items()):
#         modes.append("\"%s\"" % mode)
#         xs.append("\"-0.1\"")
#         ranks.append("0")
#         for (proportion, model) in d2.items():
#             if keepmodels:
#                 most_sim = model.most_similar('u', rankmax)
#             else:
#                 most_sim = model
#             entries = filter(lambda x: x[0] == u'you', most_sim)
#             if len(entries) > 0:
#                 modes.append("\"%s\"" % mode)
#                 xs.append("\"%.2g\"" % proportion)
#                 ranks.append("%d" % most_sim.index(entries[0]))
#     print("hist = DataFrame(")
#     print("    proportion = [" + ", ".join(xs) + "],")
#     print("    stats = [" + ", ".join(ranks) + "],")
#     print("    mode = [" + ", ".join(modes) + "]")
#     print(");")
#
# def todict(name, d):
#     print("%s = {%s};" % (name, ", ".join(["\"%s\"=>%s" % (k,v) for (k,v) in d.items()])))
#
# def eval_all_files(regexp_str, twitter_eval=True, keepmodels=False):
#     regexp = re.compile(regexp_str)
#
#     vec_models = {}
#     results_dict = {}
#     for fname in os.listdir(rootdir):
#         if not regexp.match(fname):
#             continue
#         print fname
#
#         vecf = os.path.join(rootdir, fname)
#         (vec_models[fname], results_dict[fname]) = run_all_evals(vecf, twitter_eval, keepmodels)
#         print results_dict[fname]
#     return (vec_models, results_dict)
#
# def main():
#     xvals = set()
#     for fname in os.listdir(rootdir):
#         fmatch = fileregex.match(fname)
#         if not fmatch:
#             continue
#         mode = fmatch.group(1)
#         xval = float(fmatch.group(2))
#         xvals.add(xval)
#         vecf = os.path.join(rootdir, fname)
#         fname = fname.rstrip('.txt')
#         print fname
#         if mode not in X["goog_sem"]:
#             for k in X.keys():
#                 X[k][mode] = {}
#             ydatavec[mode] = {}
#         (ydatavec[mode][xval], results) = run_all_evals(vecf)
#         for testset in results.keys():
#             X[testset][mode][xval] = results[testset]
#     xvals = sorted(xvals)
#
#     print("X = Dict();")
#     for (k,v) in X.items():
#         tochart(k, v)
#     tohistogram(ydatavec)
# #    todict("baseline_twitter", twitter_X)
#     todict("baseline_formal", formal_X)
