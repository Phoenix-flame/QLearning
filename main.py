from source.map import *
from source.game import *
from algorithms.qlearning import *

# This project has 3 parts, first part is the map, that defines agent's world.
# Second part is the game that the agent intracts with.
# And finally, the algoritm which is the agent's brain.


_map = Map('./maps/env1.map')
_game = Game(_map)
first_algorithm = QLearning(_game)
first_algorithm.run()

