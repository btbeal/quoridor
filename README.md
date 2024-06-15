
# Quoridor RL


### Project Deets

This project is a passion project to both develop the game Quoridor and subsequently employ reinforcement learning (Deep Q Learning)
to teach an agent to play.

To try for yourself, the current state requires the modification of `main.py` to the players required: (AIPlayer or Player). The AIPlayer
currently has no saved model to leverage, which is to come.

### To play

To play a friend or an AI, you can open `main.py`
and modify the players to be either the `Player` or `AIPlayer` class. The `Player` class representing a human
player. Then:

```
python main.py
```
Notably, the AIPlayer is currently untrained and will simply select random moves.

To make moves as a human player:
1. **Move the pawn by:** using directional arrows. In some cases, one can jump an opponent. To do so, simply select the direction
   you want to move as you otherwise would and a jump will be made if legal. In other cases, it may be legal to move to the side of
   the opponent's pawn in front of you. If this move is available, and legal, you may hold **A** and select the direction around the
   opponent that you would like to move. For example, if the opponent is directly above me, I may [**A** + RIGHT] or [**A** + LEFT] to move
   to the node left or right of them.
2. **Place a wall by:** hovering the mouse over the eligible wall spaces. Note
   that the highlighted wall will represent the upper-most or left-most part of the wall, which will
   take up two total segments when placed. So, none of the furthest right, or lowest walls are eligible, ever.

### To take a shot at training the AI

The AI player's settings for training can be found in the `AIPlayer` class in `src/player.py`. The player must be provided a "brain," or
a model. This is currently done in the `QuoridorGym` class where we pass the DQN models from `src/dqn.py`. You may define any
architecture you like and pass them as I've done. The idea is that the Player should really just implement moves, while Quoridor
provisions a "brain" and helps it train. Then, one can pass the models around as they wish. To run the training, one may modify
`gym.py`. Note that the default is to output the model specs to `agent_0.pth` and `agent_1.pth`. If these already exists, the model
will be loaded from those sources. If that is not desired behavior, either delete those paths (which will then be created anew) or
specify different paths. 
