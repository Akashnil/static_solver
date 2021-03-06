# Poker Bot
This python script allows the user to play a simplified game similar to Heads-up No Limit poker vs a fixed computer strategy. The goal of this project is to find out how well humans can perform vs the bot from a sample of hands.

# Rules of the Game
- Players start each hand with a stack of 81 chips and antes 1 chip each before cards are dealt.
- Players are dealt a card uniformly at random from 1 to 100. Higher card wins at showdown.
- Betting proceeds in 3 streets: flop, turn, and river
- No community cards are dealt in between the streets. But showdown happens only on the river.
- All bets must be equal to the size of the pot. Raises are also pot-sized.
- Since stack size is 81, the 4th bet / raise in a hand is size all-in. No more than 4 bet/raise is possible.
- Since all bets raises are pot sized, 1st, 2nd, 3rd, 4th bet in a hand are always of size 2, 6, 18, 54.

Example:

    Starting hand #154
    Hole-card: 30       History: _               Pot size:  2        Your Action(V/B):   v
    Hole-card: 30       History: _CC_            Pot size:  2        Your Action(V/B):   v
    Hole-card: 30       History: _CC_CC_         Pot size:  2        Your Action(V/B):   v
    Hole-card: 30       History: _CC_CC_CB       Pot size:  2+2      Your Action(F/C/R): f
    Opponent : 75       History: _CC_CC_CBF      Result  : -1        Net won  : -1       
    Starting hand #155
    Hole-card: 16       History: _               Pot size:  2        Your Action(V/B):   v
    Hole-card: 16       History: _CC_            Pot size:  2        Your Action(V/B):   v
    Hole-card: 16       History: _CC_CB          Pot size:  2+2      Your Action(F/C/R): r
    Opponent : 11       History: _CC_CBBF        Result  : +3        Net won  : +2       
    Starting hand #156
    Hole-card: 90       History: _C              Pot size:  2        Your Action(V/B):   v
    Hole-card: 90       History: _CC_C           Pot size:  2        Your Action(V/B):   v
    Hole-card: 90       History: _CC_CC_C        Pot size:  2        Your Action(V/B):   b
    Opponent : 63       History: _CC_CC_CBC_     Result  : +3        Net won  : +5

(In the hand-history section `C` denotes check/call, `B` denotes bet/raise, `F` denotes fold.)

# Controls
To play with the script, on each prompt, type one of the following letters and press enter:

``V`` Check

``F`` Fold

``C`` Call

``B`` Bet

``R`` Raise

``Q`` Quit game

All of the hand histories are saved in a file named `histories.txt`:

    0	-1	1	28	78	_CC_CC_CBF
    1	9	2	90	90	_CC_BC_BBF
    2	3	1	56	16	_CBC_CC_CC_

The columns in this file are respectively:

`hand_id`, `result`, `human = p1/p2`, `p1's card`, `p2's card`, `actions_history`

# Setup
- Download the repository (static_poker_player.py and strat.pickle should be in the same directory)
- Have python installed (any version 2.7+ or 3.x should work)
- From command line, run ``python static_poker_player.py``
- If you wish to reduce or increase the time taken by the computer to think, run the program with optional argument
``python static_poker_player.py [TIME_FACTOR]``. Default value is 1.0 Set it to 0.0 to eliminate thinking time. Setting time_factor will not affect the computer's stratgy, time taken is purely cosmetic.
