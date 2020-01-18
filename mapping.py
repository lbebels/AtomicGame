from state import Tile, Location
from directions import Direction, cardinal_directions


offset_map = {
    Direction.NORTH: Location(x=0, y=-1),
    Direction.EAST: Location(x=1, y=0),
    Direction.SOUTH: Location(x=0, y=1),
    Direction.WEST: Location(x=-1, y=0),
    Direction.NONE: Location(0, 0)
}


def offset_for_direction(direction):
    return offset_map[direction]


class Map:
    def __init__(self):
        self.width = None
        self.height = None
        self.tiles = {}

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def update_tiles(self, updates):
        for update in updates:
            location = Location(update.x, update.y)
            self.tile_at(location).set_update(update)

    def tile_at(self, location):
        if location not in self.tiles:
            self.tiles[location] = Tile(location)
        return self.tiles[location]

    def tile_at_offset(self, target, offset):
        return self.tile_at(Location(x=target.x + offset.x, y=target.y + offset.y))

    @staticmethod
    def build_locations_for_range(x, y_range):
        return [Location(x, y) for y in range(-y_range, y_range + 1)]

    def build_neighbor_location_list(self, neighbor_range):
        grid = [self.build_locations_for_range(x, neighbor_range) for x in range(-neighbor_range, neighbor_range + 1)]
        flattened = [location for row in grid for location in row]
        return [location for location in flattened if location.x != 0 or location.y != 0]

    def neighbors(self, target, neighbor_range=1):
        return [self.tile_at_offset(target, offset) for offset in self.build_neighbor_location_list(neighbor_range)]

    @staticmethod
    def calculate_estimated_distance(start, destination): #calculates heuristic distance remainder
        return abs(destination.x - start.x) + abs(destination.y - start.y)

    def has_unknown_neighbors(self, location, max_range=1):
        return any(tile.unknown for tile in self.neighbors(location, max_range))

    def can_move(self, location, direction):
        return self.neighbor_in_direction(location, direction).is_walkable()

    def neighbor_in_direction(self, location, direction):
        return self.tile_at_offset(location, offset_for_direction(direction))

    def resource_in_direction(self, location, direction):
        return self.neighbor_in_direction(location, direction).has_resource()

    def direction_to_adjacent_resource(self, location):
        return next((d for d in cardinal_directions if self.resource_in_direction(location, d)), Direction.NONE)

    def has_resource_adjacent_to(self, location):
        return self.direction_to_adjacent_resource(location) is not Direction.NONE

    def has_resources(self):
        return any(tile.has_resource() for tile in self.tiles.values())

    def all_resource_tiles(self):
        return [t for t in self.tiles.values() if t.has_resource()]

    def resource_locations_nearest(self, location):
        resource_tiles = self.all_resource_tiles()
        resource_tiles.sort(key=(lambda t: self.calculate_estimated_distance(location, t.location)))
        return [t.location for t in resource_tiles]

    @staticmethod
    def home_base_location():
        return Location(x=0, y=0)

    def enemy_base_location(self):
        return next((t.location for t in self.tiles.values() if t.has_enemy_base()), None)

    def has_enemies(self):
        return any(tile.has_enemies() for tile in self.tiles.values())

    def enemy_base_found(self):
        return self.enemy_base_location() is not None

    @staticmethod
    def is_location_within_range(start, end, max_range):
        return abs(end.x - start.x) <= max_range and abs(end.y - start.y) <= max_range

    def neighbors_with_enemies(self, start, neighbor_range):
        return [t for t in self.neighbors(start, neighbor_range) if t.is_visible() and t.has_enemies()]

    def enemy_locations_in_range(self, start, neighbor_range):
        return [t.location for t in self.neighbors_with_enemies(start, neighbor_range)]
