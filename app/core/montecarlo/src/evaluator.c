#include "shared/arrays.h"
#include "shared/evaluator.h"

const char* STR_RANKS = "23456789TJQKA";
const char* STR_SUITS = "cdhs";

void srand48();
double drand48();

void init_deck(int *deck)
{
    int n = 0, suit = 0x8000;

    for (int i = 0; i < 4; i++, suit >>= 1)
        for (int j = 0; j < 13; j++, n++)
            deck[n] = primes[j] | (j << 8) | suit | (1 << (16+j));
}


int find_card_helper(int rank, int suit, int *deck)
{
    for (int i = 0; i < 52; i++)
    {
        int c = deck[i];
        if ((c & suit) && (RANK(c) == rank))
            return i;
    }
    return -1;
}


void shuffle_deck(int *deck)
{
    int n, temp[52];

    for (int i = 0; i < 52; i++)
        temp[i] = deck[i];

    for (int i = 0; i < 52; i++)
    {
        do {
            n = (int)(51.9999999 * drand48());
        } while (temp[n] == 0);
        deck[i] = temp[n];
        temp[n] = 0;
    }
}


int find_card(const char* card, int *deck) 
{
    const char* rank_ptr = strchr(STR_RANKS, card[0]);
    const char* suit_ptr = strchr(STR_SUITS, card[1]);
    if (rank_ptr == NULL || suit_ptr == NULL) 
        return -1;

    size_t rank = rank_ptr - STR_RANKS;
    size_t suit = suit_ptr - STR_SUITS;
    return find_card_helper(rank, suit, deck);
}


static unsigned find_fast(unsigned u)
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


static unsigned short eval_5cards(int c1, int c2, int c3, int c4, int c5)
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
eval_7hand(int *hand)
{
    int subhand[5];
    unsigned short best = 9999;

    for (int i = 0; i < 21; i++)
    {
        for (int j = 0; j < 5; j++)
            subhand[j] = hand[ perm7[i][j] ];
        unsigned short q = eval_5hand(subhand);
        if (q < best)
            best = q;
    }
    return best;
}