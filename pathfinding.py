from mapping import Location

walkable_directions = [Location(x=0, y=-1), Location(x=-1, y=0), Location(x=1, y=0), Location(x=0, y=1)]


def build_path_from_location_to_node(origin, node):
    path = []
    current = node
    while current.location is not origin:
        path.append(current.location)
        current = current.parent
    path.reverse()
    return path


class Node:
    def __init__(self, location):
        self.location = location
        self.known_cost_to_start = 0
        self.estimated_cost_to_end = 0
        self.parent = None

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.location == other.location

    def estimated_total_path_cost(self):
        return self.known_cost_to_start + self.estimated_cost_to_end


def update_open_node(parent, neighbor):
    cost_to_start = parent.known_cost_to_start + 1
    if cost_to_start < neighbor.known_cost_to_start:
        neighbor.known_cost_to_start = cost_to_start
        neighbor.parent = parent


class PathFinder:
    def __init__(self, map):
        self.game_map = map
        self.open_nodes = None
        self.closed_nodes = None

    def find_path(self, start, destination, close_enough=1):
        self.initialize_node_lists(start, destination)
        while len(self.open_nodes) > 0:
            node = self.dequeue_most_promising_open_node()
            if self.reached_destination(node.location, destination, close_enough):
                return build_path_from_location_to_node(start, node)
            for neighbor in self.walkable_neighbors(node):
                self.walk_neighbor(node, neighbor, destination)
        return None

    def initialize_node_lists(self, start, destination):
        self.open_nodes = []
        self.closed_nodes = []
        start = Node(start)
        start.known_cost_to_start = 0
        start.estimated_cost_to_end = self.game_map.calculate_estimated_distance(start.location, destination)
        self.open_nodes.append(start)

    def reached_destination(self, location, destination, close_enough):
        return self.game_map.calculate_estimated_distance(location, destination) <= close_enough

    def walk_neighbor(self, parent, node, destination):
        if node in self.open_nodes:
            self.update_open_node(parent, node)
        else:
            self.add_new_open_node(parent, node, destination)

    def update_open_node(self, parent, node):
        cost_to_start = parent.known_cost_to_start + 1
        if cost_to_start < node.known_cost_to_start:
            node.known_cost_to_start = cost_to_start
            node.parent = parent

    def add_new_open_node(self, parent, node, destination):
        node.known_cost_to_start = parent.known_cost_to_start + 1
        node.estimated_cost_to_end = self.game_map.calculate_estimated_distance(node.location, destination)
        node.parent = parent
        self.open_nodes.append(node)

    def dequeue_most_promising_open_node(self):
        self.open_nodes.sort(key=lambda node: node.estimated_total_path_cost())
        node = self.open_nodes.pop(0)
        self.closed_nodes.append(node)
        return node

    def walkable_neighbors(self, node):
        neighbors = [self.game_map.tile_at_offset(node.location, offset) for offset in walkable_directions]
        walkable_tiles = [neighbor for neighbor in neighbors if neighbor.is_walkable()]
        nodes = [Node(tile.location) for tile in walkable_tiles]
        return [node for node in nodes if node not in self.closed_nodes]

