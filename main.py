#!/usr/bin/python
import sys
from communication import UpdateHandler, accept_connections
from mapping import Map
from state import UnitManager, GameStateManager
from strategy import UnitStrategyFactory, AIStrategy


if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 9090 #check if cl arguments include port
                                                                             #otherwise default 9090
    host = ''

    game_map = Map()
    unitManager = UnitManager(UnitStrategyFactory(), game_map)
    stateManager = GameStateManager(unitManager, game_map)
    gameStrategy = AIStrategy(unitManager, game_map)
    handler = UpdateHandler(stateManager, gameStrategy)
    accept_connections(host, port, handler)
