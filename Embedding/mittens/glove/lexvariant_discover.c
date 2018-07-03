// Tool to discover words that are likely lexical variants of normalized words

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STRING_LENGTH 1000

typedef double real;
typedef struct cooccur_rec {
    int word1;
    int word2;
    real val;
} CREC;

int verbose = 2; // 0, 1, or 2
long long *keep_words; // which words will map to new words
char *inds_file, *input_file, *out_file;

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

/* Efficient string comparison */
int scmp( char *s1, char *s2 ) {
    while(*s1 != '\0' && *s1 == *s2) {s1++; s2++;}
    return(*s1 - *s2);
}

/* Levenshtein code taken from Wikibooks: http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#C */
#define MIN3(a, b, c) ((a) < (b) ? ((a) < (c) ? (a) : (c)) : ((b) < (c) ? (b) : (c)))

int levenshtein(char *s1, char *s2) {
    unsigned int x, y, s1len, s2len;
    s1len = strlen(s1);
    s2len = strlen(s2);
    unsigned int matrix[s2len+1][s1len+1];
    matrix[0][0] = 0;
    for (x = 1; x <= s2len; x++)
        matrix[x][0] = matrix[x-1][0] + 1;
    for (y = 1; y <= s1len; y++)
        matrix[0][y] = matrix[0][y-1] + 1;
    for (x = 1; x <= s2len; x++)
        for (y = 1; y <= s1len; y++)
            matrix[x][y] = MIN3(matrix[x-1][y] + 1, matrix[x][y-1] + 1, matrix[x-1][y-1] + (s1[y-1] == s2[x-1] ? 0 : 1));

    return(matrix[s2len][s1len]);
}

int filter_coocs() {
    CREC cr;
    CREC cr_new;
    FILE *fin = fopen(input_file, "rb");
    if(fin == NULL) {fprintf(stderr,"Unable to open cooccurrence file %s.\n",input_file); return 1;}

    FILE *fout = fopen(out_file, "wb");
    while (fread(&cr, sizeof(CREC), 1, fin) == 1) {
	if (keep_words[cr.word1] > 0 && keep_words[cr.word2] > 0) {
	    cr_new.word1 = keep_words[cr.word1];
	    cr_new.word2 = keep_words[cr.word2];
	    cr_new.val = cr.val;
	    fwrite(&cr_new, sizeof(CREC), 1, fout);
	}
    }
    fclose(fout);
}

int filter_words() {
    FILE *fid;
    long long i, b;
    char line[MAX_STRING_LENGTH];

    FILE *file_inds = fopen(inds_file, "r");
    if (file_inds == NULL) {
      fprintf(stderr, "Error opening file_inds\n");
      exit(0);
    }

    long long vocab_size = 0;
    fid = fopen(inds_file, "r");
    if(fid == NULL) {fprintf(stderr, "Unable to open vocab file %s.\n",inds_file); return 1;}
    while ((i = getc(fid)) != EOF) if (i == '\n') vocab_size++; // Count number of entries in vocab_file
    vocab_size++;
    fclose(fid);
    keep_words = malloc(sizeof(long long) * vocab_size);
    for (b = 0; b < vocab_size; b++) keep_words[b] = 0LL;

    // Remember: every index is shifted up by 1 for cooccurrences
    long long target_ind = 0;
    while (fgets(line, MAX_STRING_LENGTH, file_inds) != NULL) {
        target_ind++;
        if (line[0] != '\0' && line[0] != '\n') {
	    keep_words[target_ind] = atol(line);
        }
    }
    fclose(file_inds);
}

int main(int argc, char **argv) {
    int i;
    input_file = malloc(sizeof(char) * MAX_STRING_LENGTH);
    inds_file = malloc(sizeof(char) * MAX_STRING_LENGTH);
    out_file = malloc(sizeof(char) * MAX_STRING_LENGTH);

    if (argc == 1) {
        printf("Tool to extract top vocab from a cooccurrence list\n");
        printf("Usage options:\n");
        printf("\t-verbose <int>\n");
        printf("\t\tSet verbosity: 0, 1, or 2 (default)\n");
        return 0;
    }

    if ((i = find_arg((char *)"-verbose", argc, argv)) > 0) verbose = atoi(argv[i + 1]);
    if ((i = find_arg((char *)"-input-file", argc, argv)) > 0) strcpy(input_file, argv[i + 1]);
    else strcpy(input_file, (char *)"cooccurrence.shuf.bin");
    if ((i = find_arg((char *)"-inds-file", argc, argv)) > 0) strcpy(inds_file, argv[i + 1]);
    if ((i = find_arg((char *)"-out-file", argc, argv)) > 0) strcpy(out_file, argv[i + 1]);
    
    filter_words();
    filter_coocs();
}
