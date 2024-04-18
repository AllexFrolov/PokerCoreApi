#include <stdio.h>
#include "shared/evaluator.h"

#define DECK_SIZE 52
#define HAND_SIZE 2
#define MAX_BOARD_SIZE 5
#define COMB_SIZE 7

#ifdef __cplusplus
extern "C" {
#endif

int 
calc_montecarlo(
    int **deck,
    char **hero_idxs,
    char **opp_idxs,
    int residual_cards,
    int work_deck_size,
    unsigned iterations) 
{
   
    int i = 0;
    while (residual_cards < COMB_SIZE)
    {
        hero_idxs[residual_cards] = deck + i;
        opp_idxs[residual_cards] = deck + i;
        residual_cards++;
        i++;
    }

    int hero_wins = 0;

    srand(time(NULL));
    for (int iter = 0; iter < iterations; ++iter)
    {
        shuffle_deck(deck, work_deck_size, COMB_SIZE);
        unsigned short h_score = eval_7cards(hero_idxs);
        unsigned short op_score = eval_7cards(opp_idxs);
        if (h_score < op_score)
            hero_wins++;
    }
    
    return hero_wins;
}


double hero_vs_range(
    char **hero_hand,
    char ***opp_range,
    int range_size,
    char **board,
    int board_size,
    unsigned iterations)
{
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
        int c_idx = find_card(hero_hand[i], deck, work_deck_size);

        work_deck_size--;
        move_to_end(deck, c_idx, work_deck_size);
        hero_idxs[hero_last_idx] = deck + work_deck_size;
    } 

    // Saving known table cards 
    for (int i = 0; i < board_size; ++i, ++hero_last_idx, ++opp_last_idx)
    {
        int c_idx = find_card(board[i], deck, work_deck_size);
        move_to_end(deck, c_idx, --work_deck_size);

        hero_idxs[hero_last_idx] = deck + work_deck_size;
        opp_idxs[opp_last_idx] = deck + work_deck_size;
    }

    int valid_hands = 0;
    int win_sum = 0;
    for (int hand_id=0; hand_id < range_size; ++hand_id)
    {
        char **opp_hand = opp_range[hand_id];
        int step_deck_size = work_deck_size;
        int step_opp_last_idx = opp_last_idx;
        char have_card = 1;

        // Saving opponent cards
        for (int i = 0; i < HAND_SIZE; ++i, ++step_opp_last_idx) 
        {
            int c_idx = find_card(opp_hand[i], deck, step_deck_size);
            if (c_idx == -1) 
            {   
                have_card = 0;
                break;
            }
            move_to_end(deck, c_idx, --step_deck_size);
            opp_idxs[step_opp_last_idx] = deck + step_deck_size;
        }
        
        if (!have_card) continue;
        win_sum += calc_montecarlo(deck, hero_idxs, opp_idxs, step_opp_last_idx, step_deck_size, iterations);
        ++valid_hands; 
    }
    return (double)win_sum / (double)(valid_hands * iterations);
}


#ifdef __cplusplus
}
#endif