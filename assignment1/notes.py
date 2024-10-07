# win on an OR node: (My/Current-player turn/perspective)
    # https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/slides/lecture8.pdf 
    # slide 26
    # win(n) = win(c1) or win(c2) or ... or win(ck )
    # return the first child that is a win
        # wc all moves are loss, or only last child win. cause need to compute all.
        # best case About b^(d/2) nodes searched as your moves have b=1 (winning move)

# win on an AND node: (Opponent wins on their turn)
    # https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/slides/lecture8.pdf 
    # slide 27
    # win(n) = win(c1) and win(c2) and ... and win(ck )
    # stop game, declare opponent victor on first child that leads to a loss. 
        # best case first child is loss, save compute

# Slide 45: MT question
 # best case on your turn u have 1 node in proof tree (simplicity/efficient lookup)
 # opponent always has >= b nodes (all their moves has to be considered) 



# // Basic Minimax with boolean outcomes 
# // Each MinimaxBooleanOR / AND game evaluation is in perspective of current player and does not change
# However in negamax the evaluation perspective is adjusted
# bool MinimaxBooleanOR(GameState state)
    # if (state.IsTerminal())
    # return state.StaticallyEvaluate()     
    # foreach successor s of state       # For each of my moves # for each child, c1 c2 , ... , ck of our state
        # if (MinimaxBooleanAND(s))      # if WE/Current-player win no matter what opponent plays
            # return true                   # Exit early and denote winning strategy
    # return false

# // Basic Minimax with boolean outcomes
# bool MinimaxBooleanAND(GameState state)
    # Also written in perspettive of WE/CURRENT player.
    # if (state.IsTerminal())
        # return state.StaticallyEvaluate()
    # foreach successor s of state       # For each of my opponent's moves
        # if (NOT MinimaxBooleanOR(s))   # If we/current-player cannot find a single winning strategy to a given move from opponen. I.e.  I lose after any of their moves, 
           # return false                # we/current-player loses
    # return true             # We/Current Player always finds a winning strategy to each of my opponents moves


# // Negamax, boolean outcomes
# bool NegamaxBoolean(GameState state)
    # if (state.IsTerminal())
    # return state.StaticallyEvaluateForToPlay() # adjusting for evaluation perspective
        # foreach legal move m from state
            # state.Execute(m)
            # bool isWin = NOT NegamaxBoolean(state) # Evaluation perspective shift to opposing player
            # state.Undo()
            # if (isWin)
                # return true
    # return false