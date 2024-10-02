#!/usr/local/bin/python3
# /usr/bin/python3
# Set the path to your python3 above


import cProfile
import numpy as np
import random
from a2  import CommandInterface

def play_a1_games() -> None:
    player = CommandInterface()
    play_games(player)



def play_games(player) -> None:
    """
    play 100 self-play games on 7x7 for profiling.
    """

    

    for _ in range(100):  # play 100 games
        boardsize = 15
        player.game([boardsize, boardsize])
        while not player.profile_winner([]):
            player.genmove([])

random.seed(1)
np.random.seed(1)
cProfile.run("play_a1_games()")



# 0          ----        1
# (1)        -----       (2)
# player 0  just played 
# now player = 1

# winner: prints (2)


