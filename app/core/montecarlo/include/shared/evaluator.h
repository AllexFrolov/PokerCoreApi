#ifndef _EVALUATOR_H_
#define _EVALUATOR_H_
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef __cplusplus
extern "C" {
#endif

#define	RANK(x)  ((x >> 8) & 0xF)

static char *value_str[] = {
    "",
    "Straight Flush",
    "Four of a Kind",
    "Full House",
    "Flush",
    "Straight",
    "Three of a Kind",
    "Two Pair",
    "One Pair",
    "High Card"
};

#define CLUB    0x8000
#define DIAMOND 0x4000
#define HEART   0x2000
#define SPADE   0x1000

extern const char* STR_RANKS;
extern const char* STR_SUITS;

void
init_deck(int *deck);

int
find_card_helper(const int *rank, const int *suit, int *deck);

int 
find_card(const char* card, int *deck);

void
shuffle_deck(int *deck, int size);

void
print_hand(int *hand, int n);

int
hand_rank(unsigned short val);

unsigned short
eval_5hand(int *hand);

unsigned short
eval_5hand_fast(int *hand);

unsigned short
eval_7hand(int *hand);

void
move_to_end(int *deck, const int *idx, int *array_size);

#ifdef __cplusplus
}
#endif

#endif