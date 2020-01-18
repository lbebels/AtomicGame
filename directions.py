import random
from enum import Enum

Direction = Enum('Direction', 'NORTH SOUTH EAST WEST NONE')

cardinal_directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

turn_map = {
    Direction.NORTH: Direction.EAST,
    Direction.EAST: Direction.SOUTH,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.NORTH
}


def turn(direction):
    return turn_map[direction]


def random_direction():
    return random.choice(list(Direction))


def cardinal_direction(location, destination):
    if destination.y < location.y:
        return Direction.NORTH
    elif destination.y > location.y:
        return Direction.SOUTH
    elif destination.x > location.x:
        return Direction.EAST
    else:
        return Direction.WEST