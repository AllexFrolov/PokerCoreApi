#include <stdio.h>
#include "shared/evaluator.h"

int calc_monte_carlo(char *hand[], char *board[]) {
    int deck[52];
    init_deck(deck);
    shuffle_deck(deck);
    for (int i = 0; i < 2; i++) {
        int c = find_card(hand[i], deck);
        printf("%d\n", c);
    }
    return 0;
}
