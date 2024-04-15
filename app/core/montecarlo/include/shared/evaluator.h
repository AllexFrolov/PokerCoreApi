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
find_card_helper(const int rank, const int suit, int *deck);

int 
find_card(const char* card, int *deck);


/*Shuffle first_n card between work_deck_size
example:
deck = {0, 1, 2, 3, 4}
work_deck_size = 3
first_n = 2
means we do shuffle value 0 to random pose from 0 to 3 then
value from pose 1 to random pose from 0 to 3.
If you want to do full shuffle 
then work_deck_size = 4 and first_n = 4
*/
void
shuffle_deck(int *deck, int work_deck_size, int first_n);

void
print_hand(int *hand, int n);

int
hand_rank(unsigned short val);

unsigned short
eval_5hand(int *hand);

unsigned short
eval_5hand_fast(int *hand);

unsigned short
eval_7cards(int **cards);

/*Moves card from idx to array_size - 1, decrease array_size by 1 and return.*/
int
move_to_end(int *deck, const int *idx, int array_size); 

#ifdef __cplusplus
}
#endif

#endif