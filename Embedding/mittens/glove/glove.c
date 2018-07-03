//  GloVe: Global Vectors for Word Representation
//
//  Copyright (c) 2014 The Board of Trustees of
//  The Leland Stanford Junior University. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//
//
//  For more information, bug reports, fixes, contact:
//    Jeffrey Pennington (jpennin@stanford.edu)
//    GlobalVectors@googlegroups.com
//    http://www-nlp.stanford.edu/projects/glove/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
#include <stdbool.h>

#define _FILE_OFFSET_BITS 64
#define MAX_STRING_LENGTH 1000

typedef double real;

typedef struct cooccur_rec {
    int word1;
    int word2;
    real val;
} CREC;

int verbose = 2; // 0, 1, or 2
int num_threads = 8; // pthreads
int num_iter = 25; // Number of full passes through cooccurrence matrix
int vector_size = 50; // Word vector size
int save_gradsq = 0; // By default don't save squared gradient values
int use_binary = 1; // 0: save as text files; 1: save as binary; 2: both. For binary, save both word and context word vectors.
int relative_iter = 0;
int model = 2; // For text file output only. 0: concatenate word and context vectors (and biases) i.e. save everything; 1: Just save word vectors (no bias); 2: Save (word + context word) vectors (no biases)
real eta = 0.05; // Initial learning rate
real alpha = 0.75, x_max = 100.0; // Weighting function parameters, not extremely sensitive to corpus, though may need adjustment for very small or very large corpora
real lambda1 = 0.1, lambda2 = 0.1; // Used for soft constraint legrange multipliers
real *W, *gradsq, *cost, *source_W, *target_W, *target_norms;
long long num_lines, *lines_per_thread, vocab_size;
char *vocab_file, *input_file, *save_W_file, *save_gradsq_file;
char *ind_map_file, *source_save_file, *target_save_file;
bool *source_vecs_exist;
int adaptation_mode = 0;
real (*glove_step)(CREC);

/* Efficient string comparison */
int scmp( char *s1, char *s2 ) {
    while(*s1 != '\0' && *s1 == *s2) {s1++; s2++;}
    return(*s1 - *s2);
}

void initialize_parameters() {
    long long a, b;
    vector_size++; // Temporarily increment to allocate space for bias

    /* Allocate space for word vectors and context word vectors, and correspodning gradsq */
    a = posix_memalign((void **)&W, 128, 2 * vocab_size * vector_size * sizeof(real)); // Might perform better than malloc
    if (W == NULL) {
        fprintf(stderr, "Error allocating memory for W\n");
        exit(1);
    }
    a = posix_memalign((void **)&source_W, 128, 2 * vocab_size * vector_size * sizeof(real)); // Might perform better than malloc
    if (source_W == NULL) {
        fprintf(stderr, "Error allocating memory for W\n");
        exit(1);
    }
    a = posix_memalign((void **)&target_W, 128, 2 * vocab_size * vector_size * sizeof(real)); // Might perform better than malloc
    if (target_W == NULL) {
        fprintf(stderr, "Error allocating memory for W\n");
        exit(1);
    }
    a = posix_memalign((void **)&gradsq, 128, 2 * vocab_size * vector_size * sizeof(real)); // Might perform better than malloc
    if (gradsq == NULL) {
        fprintf(stderr, "Error allocating memory for gradsq\n");
        exit(1);
    }
    a = posix_memalign((void **)&source_vecs_exist, 128, vocab_size * sizeof(bool)); // Might perform better than malloc
    if (source_vecs_exist == NULL) {
        fprintf(stderr, "Error allocating memory for source_vecs_exist\n");
        exit(1);
    }
    for (a = 0; a < vocab_size; a++) source_vecs_exist[a] = false;
    for (b = 0; b < vector_size; b++) for (a = 0; a < 2 * vocab_size; a++) W[a * vector_size + b] = (rand() / (real)RAND_MAX - 0.5) / vector_size;
    for (b = 0; b < vector_size; b++) for (a = 0; a < 2 * vocab_size; a++) gradsq[a * vector_size + b] = 1.0; // So initial value of eta is equal to initial learning rate
    vector_size--;
}

/* Update from an observed cooccurrence */

// 2,1 operator norm proximal updates
real glove_step_proximal(CREC cr) {
    // Remember lambda = lambda * eta already
    long long b;
    real diff, fdiff, temp1, temp2, norm1 = 0.0, norm2 = 0.0;
    real W_tmp1[vector_size], W_tmp2[vector_size]; // holds the new vectors before projection

    // cr word indices start at 1
    long long word1 = cr.word1 - 1LL;
    long long word2 = cr.word2 - 1LL;

    /* Get location of words in W & gradsq */
    long long l1 = word1 * (vector_size + 1);
    long long l2 = (word2 + vocab_size) * (vector_size + 1); // shift by vocab_size to get separate vectors for context words

    /* Calculate cost, save diff for gradients */
    diff = 0;
    for(b = 0; b < vector_size; b++) diff += W[b + l1] * W[b + l2]; // dot product of word and context word vector
    diff += W[vector_size + l1] + W[vector_size + l2] - log(cr.val); // add separate bias for each word
    fdiff = (cr.val > x_max) ? diff : pow(cr.val / x_max, alpha) * diff; // multiply weighting function (f) with diff
    real step_cost = 0.5 * fdiff * diff; // weighted squared error

    /* Adaptive gradient updates */
    fdiff *= eta; // for ease in calculating gradient

    // First compute the norms for vectors with proximal updates
    if (source_vecs_exist[word1]) {
        norm1 = 0.0;
        for(b = 0; b < vector_size; b++) {
            // for thresholding, we want the norm to be divided by the step size
            W_tmp1[b] = W[b + l1] - source_W[b + l1] - fdiff * W[b + l2] / sqrt(gradsq[b + l1]);
            norm1 += gradsq[b + l1] * (W_tmp1[b] * W_tmp1[b]);
        }
        if (sqrt(norm1) > lambda1) {
            norm1 = 0.0;
            // for scaling, no longer want norm to incorporate step size
            for(b = 0; b < vector_size; b++) {
                norm1 += W_tmp1[b] * W_tmp1[b];
            }
            norm1 = lambda1 / sqrt(norm1);
        } else {
            norm1 = -1.0;  // skip this update
        }
    }
    if (source_vecs_exist[word2]) {
        norm2 = 0.0;
        for(b = 0; b < vector_size; b++) {
            // for thresholding, we want the norm to be divided by the step size
            W_tmp2[b] = W[b + l2] - source_W[b + l2] - fdiff * W[b + l1] / sqrt(gradsq[b + l2]);
            norm2 += gradsq[b + l2] * (W_tmp2[b] * W_tmp2[b]);
        }
        if (sqrt(norm2) > lambda2) {
            norm2 = 0.0;
            // for scaling, no longer want norm to incorporate step size
            for(b = 0; b < vector_size; b++) {
                norm2 += W_tmp2[b] * W_tmp2[b];
            }
            norm2 = lambda2 / sqrt(norm2);
        } else {
            norm1 = -1.0;
        }
    }

    // TODO try skipping the accumulator step if the gradient doesn't shift
    for(b = 0; b < vector_size; b++) {
        temp1 = 0.0;
        temp2 = 0.0;
        if (source_vecs_exist[word1]) {
            if (norm1 > 0) {
                temp1 = fdiff * W[b + l2] + norm1 * W_tmp1[b];
            } else {
		W[b + l1] = source_W[b + l1];
	    }
        } else {
            temp1 = fdiff * W[b + l2];
        }
        if (source_vecs_exist[word2]) {
            if (norm2 > 0) {
                temp2 = fdiff * W[b + l1] + norm2 * W_tmp2[b];
            } else {
		W[b + l2] = source_W[b + l2];
	    }
        } else {
            temp2 = fdiff * W[b + l1];
        }
        W[b + l1] -= temp1 / sqrt(gradsq[b + l1]);
        W[b + l2] -= temp2 / sqrt(gradsq[b + l2]);
        gradsq[b + l1] += temp1 * temp1;
        gradsq[b + l2] += temp2 * temp2;
    }
    // updates for bias terms
    W[vector_size + l1] -= fdiff / sqrt(gradsq[vector_size + l1]);
    W[vector_size + l2] -= fdiff / sqrt(gradsq[vector_size + l2]);
    fdiff *= fdiff;
    gradsq[vector_size + l1] += fdiff;
    gradsq[vector_size + l2] += fdiff;
    return step_cost;
}

real glove_step_soft(CREC cr) {
    // Remember lambda = lambda * eta already
    long long b;
    real diff, fdiff, temp1, temp2;

    // cr word indices start at 1
    long long word1 = cr.word1 - 1LL;
    long long word2 = cr.word2 - 1LL;

    /* Get location of words in W & gradsq */
    long long l1 = word1 * (vector_size + 1);
    long long l2 = (word2 + vocab_size) * (vector_size + 1); // shift by vocab_size to get separate vectors for context words

    /* Calculate cost, save diff for gradients */
    diff = 0;
    for(b = 0; b < vector_size; b++) diff += W[b + l1] * W[b + l2]; // dot product of word and context word vector
    diff += W[vector_size + l1] + W[vector_size + l2] - log(cr.val); // add separate bias for each word
    fdiff = (cr.val > x_max) ? diff : pow(cr.val / x_max, alpha) * diff; // multiply weighting function (f) with diff
    real step_cost = 0.5 * fdiff * diff; // weighted squared error

    /* Adaptive gradient updates */
    fdiff *= eta; // for ease in calculating gradient
    for(b = 0; b < vector_size; b++) {
        // learning rate times gradient for word vectors
        // TODO How should we adapt adagrad to the fixed-size setup?
        // adaptive updates
        temp1 = fdiff * W[b + l2];
        if (source_vecs_exist[word1])
            temp1 += lambda1 * (W[b + l1] - source_W[b + l1]);
        temp2 = fdiff * W[b + l1];
        if (source_vecs_exist[word2])
            temp2 += lambda2 * (W[b + l2] - source_W[b + l2]);
        W[b + l1] -= temp1 / sqrt(gradsq[b + l1]);
        W[b + l2] -= temp2 / sqrt(gradsq[b + l2]);
        gradsq[b + l1] += temp1 * temp1;
        gradsq[b + l2] += temp2 * temp2;
    }
    // updates for bias terms
    W[vector_size + l1] -= fdiff / sqrt(gradsq[vector_size + l1]);
    W[vector_size + l2] -= fdiff / sqrt(gradsq[vector_size + l2]);
    fdiff *= fdiff;
    gradsq[vector_size + l1] += fdiff;
    gradsq[vector_size + l2] += fdiff;
    return step_cost;
}

// For the first few iterations, want to learn relative to the previous vecs
real glove_step_relative(CREC cr) {
    long long b;
    real diff, fdiff, temp1, temp2;

    // cr word indices start at 1
    long long word1 = cr.word1 - 1LL;
    long long word2 = cr.word2 - 1LL;

    /* Get location of words in W & gradsq */
    long long l1 = word1 * (vector_size + 1);
    long long l2 = (word2 + vocab_size) * (vector_size + 1); // shift by vocab_size to get separate vectors for context words

    /* Calculate cost, save diff for gradients */
    diff = 0;
    for(b = 0; b < vector_size; b++) diff += W[b + l1] * W[b + l2]; // dot product of word and context word vector
    diff += W[vector_size + l1] + W[vector_size + l2] - log(cr.val); // add separate bias for each word
    fdiff = (cr.val > x_max) ? diff : pow(cr.val / x_max, alpha) * diff; // multiply weighting function (f) with diff
    real step_cost = 0.5 * fdiff * diff; // weighted squared error

    /* Adaptive gradient updates */
    fdiff *= eta; // for ease in calculating gradient
    if (source_vecs_exist[word1]) {
        if (source_vecs_exist[word2]) {
            // both vectors are fixed
            return step_cost;
        }
        for(b = 0; b < vector_size; b++) {
            // learning rate times gradient for word vectors
            temp2 = fdiff * W[b + l1];
            // TODO How should we adapt adagrad to the fixed-size setup?
            // adaptive updates
            W[b + l2] -= temp2 / sqrt(gradsq[b + l2]);
            gradsq[b + l2] += temp2 * temp2;
        }
    } else if (source_vecs_exist[word2]) {
        for(b = 0; b < vector_size; b++) {
            // learning rate times gradient for word vectors
            temp1 = fdiff * W[b + l2];
            // TODO How should we adapt adagrad to the fixed-size setup?
            // adaptive updates
            W[b + l1] -= temp1 / sqrt(gradsq[b + l1]);
            gradsq[b + l1] += temp1 * temp1;
        }
    } else {
        return step_cost;
    }
    // don't need to update bias terms for first few iterations
    W[vector_size + l1] -= fdiff / sqrt(gradsq[vector_size + l1]);
    W[vector_size + l2] -= fdiff / sqrt(gradsq[vector_size + l2]);
    fdiff *= fdiff;
    gradsq[vector_size + l1] += fdiff;
    gradsq[vector_size + l2] += fdiff;
    return step_cost;
}

real glove_step_fixed(CREC cr) {
    long long b;
    real diff, fdiff, temp1, temp2;

    // cr word indices start at 1
    long long word1 = cr.word1 - 1LL;
    long long word2 = cr.word2 - 1LL;

    /* Get location of words in W & gradsq */
    long long l1 = word1 * (vector_size + 1);
    long long l2 = (word2 + vocab_size) * (vector_size + 1); // shift by vocab_size to get separate vectors for context words

    /* Calculate cost, save diff for gradients */
    diff = 0;
    for(b = 0; b < vector_size; b++) diff += W[b + l1] * W[b + l2]; // dot product of word and context word vector
    diff += W[vector_size + l1] + W[vector_size + l2] - log(cr.val); // add separate bias for each word
    fdiff = (cr.val > x_max) ? diff : pow(cr.val / x_max, alpha) * diff; // multiply weighting function (f) with diff
    real step_cost = 0.5 * fdiff * diff; // weighted squared error

    /* Adaptive gradient updates */
    fdiff *= eta; // for ease in calculating gradient
    for(b = 0; b < vector_size; b++) {
        // learning rate times gradient for word vectors
        temp1 = fdiff * W[b + l2];
        temp2 = fdiff * W[b + l1];
        // TODO How should we adapt adagrad to the fixed-size setup?
        // adaptive updates
        if (!source_vecs_exist[word1]) W[b + l1] -= temp1 / sqrt(gradsq[b + l1]);
        if (!source_vecs_exist[word2]) W[b + l2] -= temp2 / sqrt(gradsq[b + l2]);
        gradsq[b + l1] += temp1 * temp1;
        gradsq[b + l2] += temp2 * temp2;
    }
    // updates for bias terms
    // TODO Do we want to update b even if we don't update w?
    W[vector_size + l1] -= fdiff / sqrt(gradsq[vector_size + l1]);
    W[vector_size + l2] -= fdiff / sqrt(gradsq[vector_size + l2]);
    fdiff *= fdiff;
    gradsq[vector_size + l1] += fdiff;
    gradsq[vector_size + l2] += fdiff;
    return step_cost;
}

real glove_step_vanilla(CREC cr) {
    long long b;
    real diff, fdiff, temp1, temp2;

    // cr word indices start at 1
    long long word1 = cr.word1 - 1LL;
    long long word2 = cr.word2 - 1LL;

    /* Get location of words in W & gradsq */
    long long l1 = word1 * (vector_size + 1);
    long long l2 = (word2 + vocab_size) * (vector_size + 1); // shift by vocab_size to get separate vectors for context words

    /* Calculate cost, save diff for gradients */
    diff = 0;
    for(b = 0; b < vector_size; b++) diff += W[b + l1] * W[b + l2]; // dot product of word and context word vector
    diff += W[vector_size + l1] + W[vector_size + l2] - log(cr.val); // add separate bias for each word
    fdiff = (cr.val > x_max) ? diff : pow(cr.val / x_max, alpha) * diff; // multiply weighting function (f) with diff
    real step_cost = 0.5 * fdiff * diff; // weighted squared error

    /* Adaptive gradient updates */
    fdiff *= eta; // for ease in calculating gradient
    for(b = 0; b < vector_size; b++) {
        // learning rate times gradient for word vectors
        temp1 = fdiff * W[b + l2];
        temp2 = fdiff * W[b + l1];
        // adaptive updates
        W[b + l1] -= temp1 / sqrt(gradsq[b + l1]);
        W[b + l2] -= temp2 / sqrt(gradsq[b + l2]);
        gradsq[b + l1] += temp1 * temp1;
        gradsq[b + l2] += temp2 * temp2;
    }
    // updates for bias terms
    W[vector_size + l1] -= fdiff / sqrt(gradsq[vector_size + l1]);
    W[vector_size + l2] -= fdiff / sqrt(gradsq[vector_size + l2]);
    fdiff *= fdiff;
    gradsq[vector_size + l1] += fdiff;
    gradsq[vector_size + l2] += fdiff;
    return step_cost;
}

/* Train the GloVe model */
void *glove_thread(void *vid) {
    long long a;
    long long id = (long long) vid;
    CREC cr;
    FILE *fin;
    fin = fopen(input_file, "rb");
    fseeko(fin, (num_lines / num_threads * id) * (sizeof(CREC)), SEEK_SET); //Threads spaced roughly equally throughout file
    cost[id] = 0;

    for(a = 0; a < lines_per_thread[id]; a++) {
        fread(&cr, sizeof(CREC), 1, fin);
        if(feof(fin)) break;

        cost[id] += glove_step(cr);
    }

    fclose(fin);
    pthread_exit(NULL);
}

/* Save params to file */
int save_params() {
    long long a, b;
    char format[20];
    char output_file[MAX_STRING_LENGTH], output_file_gsq[MAX_STRING_LENGTH];
    char *word = malloc(sizeof(char) * MAX_STRING_LENGTH);
    FILE *fid, *fout, *fgs;

    if(use_binary > 0) { // Save parameters in binary file
        sprintf(output_file,"%s.bin",save_W_file);
        fout = fopen(output_file,"wb");
        if(fout == NULL) {fprintf(stderr, "Unable to open file %s.\n",save_W_file); return 1;}
        for(a = 0; a < 2 * (long long)vocab_size * (vector_size + 1); a++) fwrite(&W[a], sizeof(real), 1,fout);
        fclose(fout);
        if(save_gradsq > 0) {
            sprintf(output_file_gsq,"%s.bin",save_gradsq_file);
            fgs = fopen(output_file_gsq,"wb");
            if(fgs == NULL) {fprintf(stderr, "Unable to open file %s.\n",save_gradsq_file); return 1;}
            for(a = 0; a < 2 * (long long)vocab_size * (vector_size + 1); a++) fwrite(&gradsq[a], sizeof(real), 1,fgs);
            fclose(fgs);
        }
    }
    if(use_binary != 1) { // Save parameters in text file
        sprintf(output_file,"%s.txt",save_W_file);
        if(save_gradsq > 0) {
            sprintf(output_file_gsq,"%s.txt",save_gradsq_file);
            fgs = fopen(output_file_gsq,"wb");
            if(fgs == NULL) {fprintf(stderr, "Unable to open file %s.\n",save_gradsq_file); return 1;}
        }
        fout = fopen(output_file,"wb");
        if(fout == NULL) {fprintf(stderr, "Unable to open file %s.\n",save_W_file); return 1;}
        fid = fopen(vocab_file, "r");
        sprintf(format,"%%%ds",MAX_STRING_LENGTH);
        if(fid == NULL) {fprintf(stderr, "Unable to open file %s.\n",vocab_file); return 1;}
        for(a = 0; a < vocab_size; a++) {
            if(fscanf(fid,format,word) == 0) return 1;
            fprintf(fout, "%s",word);
            if(model == 0) { // Save all parameters (including bias)
                for(b = 0; b < (vector_size + 1); b++) fprintf(fout," %lf", W[a * (vector_size + 1) + b]);
                for(b = 0; b < (vector_size + 1); b++) fprintf(fout," %lf", W[(vocab_size + a) * (vector_size + 1) + b]);
            }
            if(model == 1) // Save only "word" vectors (without bias)
                for(b = 0; b < vector_size; b++) fprintf(fout," %lf", W[a * (vector_size + 1) + b]);
            if(model == 2) // Save "word + context word" vectors (without bias)
                for(b = 0; b < vector_size; b++) fprintf(fout," %lf", W[a * (vector_size + 1) + b] + W[(vocab_size + a) * (vector_size + 1) + b]);
            fprintf(fout,"\n");
            if(save_gradsq > 0) { // Save gradsq
                fprintf(fgs, "%s",word);
                for(b = 0; b < (vector_size + 1); b++) fprintf(fgs," %lf", gradsq[a * (vector_size + 1) + b]);
                for(b = 0; b < (vector_size + 1); b++) fprintf(fgs," %lf", gradsq[(vocab_size + a) * (vector_size + 1) + b]);
                fprintf(fgs,"\n");
            }
            if(fscanf(fid,format,word) == 0) return 1; // Eat irrelevant frequency entry
        }
        fclose(fid);
        fclose(fout);
        if(save_gradsq > 0) fclose(fgs);
    }
    return 0;
}

void load_source_vectors() {
    // TODO more efficient if old -> new rather than new -> old mapping
    long long i, b, l1, l2, target_ind;
    long long source_l1, source_ind, context_offset;
    char line[MAX_STRING_LENGTH];
    vector_size++; // temporarily increment to allow space for bias

    FILE *file_inds = fopen(ind_map_file, "r");
    if (file_inds == NULL) {
      fprintf(stderr, "Error opening file_inds\n");
      exit(0);
    }
    FILE *file_source = fopen(source_save_file, "rb");
    if (file_source == NULL) {
      fprintf(stderr, "Error opening file_source\n");
      exit(0);
    }

    fseeko(file_source, 0L, SEEK_END);
    context_offset = ftell(file_source) / 2;
    fprintf(stderr, "Source vocab size: %llu\n", context_offset / (sizeof(real) * vector_size));

    fprintf(stderr, "Loading in old source vectors...");
    target_ind = -1;
    while (fgets(line, MAX_STRING_LENGTH, file_inds) != NULL) {
        target_ind++;
        for (i = 0; i < MAX_STRING_LENGTH; i++) {
            if (line[i] == '\n' || line[i] == '\0') {
                line[i] = '\0';
                break;
            }
        }
        if (line[0] == '\0') {
            continue;  // no corresponding old vocab
        }

        source_ind = atoi(line);
        source_vecs_exist[target_ind] = true;

        l1 = target_ind * vector_size;
        l2 = (target_ind + vocab_size) * vector_size;
        source_l1 = source_ind * vector_size * sizeof(real);

        // Read the source vectors, both word and context
        fseeko(file_source, source_l1, SEEK_SET);
        fread((void *)(&source_W[l1]), sizeof(real), vector_size, file_source);
        fseeko(file_source, source_l1 + context_offset, SEEK_SET);
        fread((void *)(&source_W[l2]), sizeof(real), vector_size, file_source);

        switch (adaptation_mode) {
            case 0: // no break ... initialize as old vecs
            case 1:
            case 2:
            case 4:
                memcpy((void *)&W[l1], (void *)&source_W[l1],
                       sizeof(real) * vector_size);
                memcpy((void *)&W[l2], (void *)&source_W[l2],
                       sizeof(real) * vector_size);
                break;
            default:
                break;
        }
    }
    fprintf(stderr, " done\n");

    fclose(file_inds);
    fclose(file_source);
    vector_size--;
}

void load_target_vectors() {
    long long i;

    FILE *file_target = fopen(target_save_file, "rb");
    if (file_target == NULL) {
        fprintf(stderr, "Error opening file_target\n");
        exit(0);
    }
    fprintf(stderr, "Loading in old target vectors...");
    fread((void *)(target_W), sizeof(real), 2 * vocab_size * (vector_size + 1), file_target);

    memcpy((void *)W, (void *)target_W,
	   sizeof(real) * 2 * vocab_size * (vector_size + 1));
    fprintf(stderr, " done\n");
    fclose(file_target);
}

/* Train model */
int train_glove() {
    long long a, file_size;
    int b;
    FILE *fin;
    real total_cost = 0;
    fprintf(stderr, "TRAINING MODEL\n");

    fin = fopen(input_file, "rb");
    if(fin == NULL) {fprintf(stderr,"Unable to open cooccurrence file %s.\n",input_file); return 1;}
    fseeko(fin, 0L, SEEK_END);
    file_size = ftello(fin);
    num_lines = file_size/(sizeof(CREC)); // Assuming the file isn't corrupt and consists only of CREC's
    fclose(fin);
    fprintf(stderr,"Read %lld lines.\n", num_lines);
    if(verbose > 1) fprintf(stderr,"Initializing parameters...");
    initialize_parameters();
    if(verbose > 1) fprintf(stderr,"done.\n");
    if (source_save_file[0] != '\0' && ind_map_file[0] != '\0') {
        load_source_vectors();
    }
    if (target_save_file[0] != '\0') {
        load_target_vectors();
    }
    if(verbose > 0) fprintf(stderr,"vector size: %d\n", vector_size);
    if(verbose > 0) fprintf(stderr,"vocab size: %lld\n", vocab_size);
    if(verbose > 0) fprintf(stderr,"x_max: %lf\n", x_max);
    if(verbose > 0) fprintf(stderr,"alpha: %lf\n", alpha);
    pthread_t *pt = (pthread_t *)malloc(num_threads * sizeof(pthread_t));
    lines_per_thread = (long long *) malloc(num_threads * sizeof(long long));

    if (!pt || !lines_per_thread) {
        fprintf(stderr, "Error allocating memory for thread arrays.\n");
	exit(0);
    }

    // Run a few iterations of SGD just relative to the formally trained vecs ...
    real (*glove_step_tmp)(CREC) = glove_step;
    for (b = 0; b < relative_iter; b++) {
        glove_step = &glove_step_relative;
        total_cost = 0;
        for (a = 0; a < num_threads - 1; a++) lines_per_thread[a] = num_lines / num_threads;
        lines_per_thread[a] = num_lines / num_threads + num_lines % num_threads;
        for (a = 0; a < num_threads; a++) pthread_create(&pt[a], NULL, glove_thread, (void *)a);
        for (a = 0; a < num_threads; a++) pthread_join(pt[a], NULL);
        for (a = 0; a < num_threads; a++) total_cost += cost[a];
        fprintf(stderr,"iter: %03d, cost: %lf\n", b+1, total_cost/num_lines);
    }
    for (b = 0; b < vector_size; b++) for (a = 0; a < 2 * vocab_size; a++) gradsq[a * vector_size + b] = 1.0; // So initial value of eta is equal to initial learning rate
    glove_step = glove_step_tmp;

    if(verbose > 0) fprintf(stderr,"Initialized matrices...\n");

    // Lock-free asynchronous SGD
    for(b = 0; b < num_iter; b++) {
        total_cost = 0;
        for (a = 0; a < num_threads - 1; a++) lines_per_thread[a] = num_lines / num_threads;
        lines_per_thread[a] = num_lines / num_threads + num_lines % num_threads;
        for (a = 0; a < num_threads; a++) pthread_create(&pt[a], NULL, glove_thread, (void *)a);
        for (a = 0; a < num_threads; a++) pthread_join(pt[a], NULL);
        for (a = 0; a < num_threads; a++) total_cost += cost[a];
        fprintf(stderr,"iter: %03d, cost: %lf\n", b+1, total_cost/num_lines);
    }
    return save_params();
}

int find_arg(char *str, int argc, char **argv) {
    int i;
    for (i = 1; i < argc; i++) {
        if(!scmp(str, argv[i])) {
            if (i == argc - 1) {
                printf("No argument given for %s\n", str);
                exit(1);
            }
            return i;
        }
    }
    return -1;
}

int main(int argc, char **argv) {
    int i;
    FILE *fid;
    vocab_file = malloc(sizeof(char) * MAX_STRING_LENGTH);
    input_file = malloc(sizeof(char) * MAX_STRING_LENGTH);
    save_W_file = malloc(sizeof(char) * MAX_STRING_LENGTH);
    save_gradsq_file = malloc(sizeof(char) * MAX_STRING_LENGTH);
    ind_map_file = malloc(sizeof(char) * MAX_STRING_LENGTH);
    source_save_file = malloc(sizeof(char) * MAX_STRING_LENGTH);
    target_save_file = malloc(sizeof(char) * MAX_STRING_LENGTH);
    source_save_file[0] = '\0';
    target_save_file[0] = '\0';

    if (argc == 1) {
        printf("GloVe: Global Vectors for Word Representation, v0.2\n");
        printf("Author: Jeffrey Pennington (jpennin@stanford.edu)\n\n");
        printf("Usage options:\n");
        printf("\t-verbose <int>\n");
        printf("\t\tSet verbosity: 0, 1, or 2 (default)\n");
        printf("\t-vector-size <int>\n");
        printf("\t\tDimension of word vector representations (excluding bias term); default 50\n");
        printf("\t-threads <int>\n");
        printf("\t\tNumber of threads; default 8\n");
        printf("\t-iter <int>\n");
        printf("\t\tNumber of training iterations; default 25\n");
        printf("\t-eta <float>\n");
        printf("\t\tInitial learning rate; default 0.05\n");
        printf("\t-alpha <float>\n");
        printf("\t\tParameter in exponent of weighting function; default 0.75\n");
        printf("\t-x-max <float>\n");
        printf("\t\tParameter specifying cutoff in weighting function; default 100.0\n");
        printf("\t-binary <int>\n");
        printf("\t\tSave output in binary format (0: text, 1: binary, 2: both); default 0\n");
        printf("\t-model <int>\n");
        printf("\t\tModel for word vector output (for text output only); default 2\n");
        printf("\t\t   0: output all data, for both word and context word vectors, including bias terms\n");
        printf("\t\t   1: output word vectors, excluding bias terms\n");
        printf("\t\t   2: output word vectors + context word vectors, excluding bias terms\n");
        printf("\t-input-file <file>\n");
        printf("\t\tBinary input file of shuffled cooccurrence data (produced by 'cooccur' and 'shuffle'); default cooccurrence.shuf.bin\n");
        printf("\t-vocab-file <file>\n");
        printf("\t\tFile containing vocabulary (truncated unigram counts, produced by 'vocab_count'); default vocab.txt\n");
        printf("\t-save-file <file>\n");
        printf("\t\tFilename, excluding extension, for word vector output; default vectors\n");
        printf("\t-gradsq-file <file>\n");
        printf("\t\tFilename, excluding extension, for squared gradient output; default gradsq\n");
        printf("\t-save-gradsq <int>\n");
        printf("\t\tSave accumulated squared gradients; default 0 (off); ignored if gradsq-file is specified\n");
        printf("\t-source-save-file <file>\n");
        printf("\t\tPreviously learned word vectors to incorporate as old domain during training\n");
        printf("\t-ind-map-file <file>\n");
        printf("\t\tFile containing previous domain's vocabulary indices for each target vocab line\n");
        printf("\t-target-save-file <file>\n");
        printf("\t\tPreviously learned word vectors for target domain without adaptation\n");
        printf("\t-adaptation-mode <int>\n");
        printf("\t\t0: No adaptation in step, 1: Fixed old vectors\n");
        printf("\t-lambda1 <float>\n");
        printf("\t-lambda2 <float>\n");
        printf("\nExample usage:\n");
        printf("./glove -input-file cooccurrence.shuf.bin -vocab-file vocab.txt -save-file vectors -gradsq-file gradsq -verbose 2 -vector-size 100 -threads 16 -alpha 0.75 -x-max 100.0 -eta 0.05 -binary 2 -model 2\n\n");
        return 0;
    }


    if ((i = find_arg((char *)"-verbose", argc, argv)) > 0) verbose = atoi(argv[i + 1]);
    if ((i = find_arg((char *)"-vector-size", argc, argv)) > 0) vector_size = atoi(argv[i + 1]);
    if ((i = find_arg((char *)"-iter", argc, argv)) > 0) num_iter = atoi(argv[i + 1]);
    if ((i = find_arg((char *)"-threads", argc, argv)) > 0) num_threads = atoi(argv[i + 1]);
    cost = malloc(sizeof(real) * num_threads);
    if ((i = find_arg((char *)"-alpha", argc, argv)) > 0) alpha = atof(argv[i + 1]);
    if ((i = find_arg((char *)"-x-max", argc, argv)) > 0) x_max = atof(argv[i + 1]);
    if ((i = find_arg((char *)"-eta", argc, argv)) > 0) eta = atof(argv[i + 1]);
    if ((i = find_arg((char *)"-binary", argc, argv)) > 0) use_binary = atoi(argv[i + 1]);
    if ((i = find_arg((char *)"-model", argc, argv)) > 0) model = atoi(argv[i + 1]);
    if(model != 0 && model != 1) model = 2;
    if ((i = find_arg((char *)"-save-gradsq", argc, argv)) > 0) save_gradsq = atoi(argv[i + 1]);
    if ((i = find_arg((char *)"-vocab-file", argc, argv)) > 0) strcpy(vocab_file, argv[i + 1]);
    else strcpy(vocab_file, (char *)"vocab.txt");
    if ((i = find_arg((char *)"-save-file", argc, argv)) > 0) strcpy(save_W_file, argv[i + 1]);
    else strcpy(save_W_file, (char *)"vectors");
    if ((i = find_arg((char *)"-adaptation-mode", argc, argv)) > 0) adaptation_mode = atoi(argv[i + 1]);
    if ((i = find_arg((char *)"-gradsq-file", argc, argv)) > 0) {
        strcpy(save_gradsq_file, argv[i + 1]);
        save_gradsq = 1;
    }
    else if(save_gradsq > 0) strcpy(save_gradsq_file, (char *)"gradsq");
    if ((i = find_arg((char *)"-input-file", argc, argv)) > 0) strcpy(input_file, argv[i + 1]);
    else strcpy(input_file, (char *)"cooccurrence.shuf.bin");
    if ((i = find_arg((char *)"-source-save-file", argc, argv)) > 0) strcpy(source_save_file, argv[i + 1]);
    if ((i = find_arg((char *)"-ind-map-file", argc, argv)) > 0) strcpy(ind_map_file, argv[i + 1]);
    if ((i = find_arg((char *)"-target-save-file", argc, argv)) > 0) strcpy(target_save_file, argv[i + 1]);
    if ((i = find_arg((char *)"-lambda1", argc, argv)) > 0) lambda1 = eta*atof(argv[i + 1]);
    if ((i = find_arg((char *)"-lambda2", argc, argv)) > 0) lambda2 = eta*atof(argv[i + 1]);
    if ((i = find_arg((char *)"-relative-iter", argc, argv)) > 0) relative_iter = atoi(argv[i + 1]);
    vocab_size = 0;
    fid = fopen(vocab_file, "r");
    if(fid == NULL) {fprintf(stderr, "Unable to open vocab file %s.\n",vocab_file); return 1;}
    while ((i = getc(fid)) != EOF) if (i == '\n') vocab_size++; // Count number of entries in vocab_file
    fclose(fid);

    switch (adaptation_mode) {
        case 0:
            glove_step = &glove_step_vanilla;
            break;
        case 1:
            glove_step = &glove_step_fixed;
            break;
        case 2:
            glove_step = &glove_step_soft;
            break;
        case 4:
            glove_step = &glove_step_proximal;
            break;
    }

    return train_glove();
}
