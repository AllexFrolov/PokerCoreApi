#include <stdio.h>
#include "shared/evaluator.h"

#define DECK_SIZE 52
#define HAND_SIZE 2
#define MAX_BOARD_SIZE 5
#define COMB_SIZE 7
#define ITERATIONS 1000000 // number of iterations of monte carlo


double calc_monte_carlo(char **hand, char **board, int board_size) {

    int deck[DECK_SIZE];
    init_deck(deck);
    int work_deck_size = DECK_SIZE;

    int *hero_idxs[COMB_SIZE];
    int *opp_idxs[COMB_SIZE];
    int hero_last_idx = 0;
    int opp_last_idx = 0; 


    // Saving hero cards
    for (int i = 0; i < HAND_SIZE; ++i, ++hero_last_idx) 
    {
        int c_idx = find_card(hand[i], deck);
        work_deck_size = move_to_end(deck, &c_idx, work_deck_size);
        hero_idxs[hero_last_idx] = deck + work_deck_size;
    }

    // Saving known table cards 
    for (int i = 0; i < board_size; ++i, ++hero_last_idx, ++opp_last_idx)
    {
        int c_idx = find_card(board[i], deck);
        work_deck_size = move_to_end(deck, &c_idx, work_deck_size);
        hero_idxs[hero_last_idx] = deck + work_deck_size;
        opp_idxs[opp_last_idx] = deck + work_deck_size;
    }

    int i = 0;
    while (hero_last_idx < COMB_SIZE || opp_last_idx < COMB_SIZE)
    {
        if (hero_last_idx < COMB_SIZE)
        {
            hero_idxs[hero_last_idx] = deck + i;
            hero_last_idx++;
        }
        if (opp_last_idx < COMB_SIZE)
        {
            opp_idxs[opp_last_idx] = deck + i;
            opp_last_idx++;
        }
        i++;
    }

    int hero_wins = 0;

    srand(time(NULL));
    for (int iter = 0; iter < ITERATIONS; ++iter)
    {
        shuffle_deck(deck, work_deck_size, COMB_SIZE);
        unsigned short h_score = eval_7cards(hero_idxs);
        unsigned short op_score = eval_7cards(opp_idxs);
        if (h_score < op_score)
            hero_wins++;
    }
    
    return (double)hero_wins / (double)ITERATIONS;
}
