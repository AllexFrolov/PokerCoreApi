#include "shared/arrays.h"
#include "shared/evaluator.h"

const char* STR_RANKS = "23456789TJQKA";
const char* STR_SUITS = "cdhs";

void 
init_deck(int *deck)
{
    int n = 0, suit = 0x8000;

    for (int i = 0; i < 4; i++, suit >>= 1)
        for (int j = 0; j < 13; j++, n++)
            deck[n] = primes[j] | (j << 8) | suit | (1 << (16+j));
}


int 
find_card_helper(const int rank, const int suit, int *deck, const int work_deck_size)
{
    for (int i = 0; i < work_deck_size; i++)
    {
        int c = deck[i];
        if ((c & (CLUB >> suit)) && (RANK(c) == rank)) {
            return i;
        }
    }
    return -1;
}

void 
shuffle_deck(int *deck, int work_deck_size, int first_n) {
    for (int i = 0; i < first_n; ++i) {
        int randomIndex = rand() % work_deck_size;

        int temp = deck[i];
        deck[i] = deck[randomIndex];
        deck[randomIndex] = temp;
    }
}


int 
find_card(const char* card, int *deck, const int work_deck_size) 
{
    const char* rank_ptr = strchr(STR_RANKS, card[0]);
    const char* suit_ptr = strchr(STR_SUITS, card[1]);
    if (rank_ptr == NULL || suit_ptr == NULL) 
        return -1;

    int rank = (int)(rank_ptr - STR_RANKS);
    int suit = (int)(suit_ptr - STR_SUITS);
    return find_card_helper(rank, suit, deck, work_deck_size);
}


static unsigned 
find_fast(unsigned u)
{
    unsigned a, b, r;

    u += 0xe91aaa35;
    u ^= u >> 16;
    u += u << 8;
    u ^= u >> 4;
    b  = (u >> 8) & 0x1ff;
    a  = (u + (u << 2)) >> 19;
    r  = a ^ hash_adjust[b];
    return r;
}


static unsigned short 
eval_5cards(int c1, int c2, int c3, int c4, int c5)
{
    int q = (c1 | c2 | c3 | c4 | c5) >> 16;
    short s;

    if (c1 & c2 & c3 & c4 & c5 & 0xf000)
        return flushes[q];

    if ((s = unique5[q]))
        return s;

    q = (c1 & 0xff) * (c2 & 0xff) * (c3 & 0xff) * (c4 & 0xff) * (c5 & 0xff);
    return hash_values[find_fast(q)];
}


unsigned short
eval_5hand(int *hand)
{
    int c1 = *hand++;
    int c2 = *hand++;
    int c3 = *hand++;
    int c4 = *hand++;
    int c5 = *hand;

    return eval_5cards(c1, c2, c3, c4, c5);
}

unsigned short
eval_cards(int **cards, const int board_size)
{
    int subhand[5];
    unsigned short best = 9999;

    int permutations = 21;
    if (board_size == FLOP) 
        permutations = 1;
    else if (board_size == TURN)
        permutations = 6;
    

    for (int i = 0; i < permutations; i++)
    {
        for (int j = 0; j < 5; j++)
            subhand[j] = *(cards[ perm7[i][j] ]);
        unsigned short q = eval_5hand(subhand);
        if (q < best)
            best = q;
    }
    return best;
}

void
move_to_end(int *deck, const int idx, const int array_size)
{
    int temp_c = deck[idx];
    deck[idx] = deck[array_size];
    deck[array_size] = temp_c;
}



// Returns the hand rank of the given equivalence class value.
// Note: the parameter "val" should be in the range of 1-7462.
int
hand_rank(unsigned short val)
{
    if (val > 6185) return HIGH_CARD;        // 1277 high card
    if (val > 3325) return ONE_PAIR;         // 2860 one pair
    if (val > 2467) return TWO_PAIR;         //  858 two pair
    if (val > 1609) return THREE_OF_A_KIND;  //  858 three-kind
    if (val > 1599) return STRAIGHT;         //   10 straights
    if (val > 322)  return FLUSH;            // 1277 flushes
    if (val > 166)  return FULL_HOUSE;       //  156 full house
    if (val > 10)   return FOUR_OF_A_KIND;   //  156 four-kind
    return STRAIGHT_FLUSH;                   //   10 straight-flushes
}