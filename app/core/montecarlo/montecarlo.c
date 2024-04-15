#include <stdio.h>
#include "shared/evaluator.h"

#define DECK_SIZE 52

int calc_monte_carlo(char **hand, char **board, int board_size) {

    int deck[DECK_SIZE];
    init_deck(deck);

    int cards[7];
    int last_idx = 0;

    int actual_size = sizeof(deck) / sizeof(deck[0]);
    for (int i = 0; i < 2; i++, last_idx++) 
    {
        int c = find_card(hand[i], deck);
        move_to_end(deck, &c, &actual_size);
        cards[last_idx] = deck[actual_size];
    }

    for (int i = 0; i < board_size; i++, last_idx++)
    {
        int c = find_card(board[i], deck);
        move_to_end(deck, &c, &actual_size);
        cards[last_idx] = deck[actual_size];
    }

    shuffle_deck(deck, actual_size);
    
    int op_hand[2];

    // for (int i=0; i < 2; i++)
    // {

    // }

    return 0;
}
