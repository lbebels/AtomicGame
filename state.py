import collections
from directions import cardinal_direction, random_direction


Location = collections.namedtuple('Location', 'x y')


class Unit:
    def __init__(self, update=None):
        self.update = update
        self.strategy = None
        self.path = None

    def id(self):
        return self.update.id

    def location(self):
        return Location(self.update.x, self.update.y)

    def is_tank(self):
        return self.is_type("tank")

    def is_scout(self):
        return self.is_type("scout")

    def is_worker(self):
        return self.is_type("worker")

    def is_base(self):
        return self.is_type("base")

    def is_idle(self):
        return self.has_status("idle")

    def is_alive(self):
        return not self.has_status("dead")

    def is_mobile(self):
        return self.is_tank() or self.is_scout() or self.is_worker()

    def is_carrying_resources(self):
        return self.available_resources() > 0

    def available_resources(self):
        return self.update.resource

    def can_attack(self):
        return self.update.can_attack

    def is_type(self, unit_type):
        return unit_type == self.update.type

    def has_status(self, status):
        return status == self.update.status

    def build_command(self):
        if self.is_idle() and self.strategy is not None:
            return self.strategy.build_command(self)
        else:
            return None

    def next_move(self):
        if self.path is not None:
            return cardinal_direction(self.location(), self.path.pop(0))
        else:
            return random_direction()

    def is_adjacent_to_resource(self, game_map):
        return game_map.has_resource_adjacent_to(self.location())


class Tile:
    def __init__(self, location):
        self.location = location
        self.update = None
        self.unknown = True

    def set_update(self, update):
        if self.update is None or update.visible:
            self.update = update
            self.unknown = False
        else:
            self.update.visible = False

    def is_visible(self):
        return self.update.visible

    def is_known(self):
        return not self.unknown

    def is_blocked(self):
        return self.update.blocked

    def is_walkable(self):
        return self.is_known() and not self.is_blocked()

    def has_resource(self):
        return (self.update
                and self.update.resource
                and self.update.resource.value > 0)

    def units(self):
        if self.update and self.update.units:
            return [Unit(unit) for unit in self.update.units]
        else:
            return []

    def has_enemy_base(self):
        return any(unit.is_base() for unit in self.units())

    def has_enemies(self):
        return any(unit.is_alive() for unit in self.units())


class UnitManager:
    def __init__(self, strategy_factory,  game_map):
        self.strategy_factory = strategy_factory
        self.game_map = game_map
        self.units = {}
        self.tank_info = None
        self.scout_info = None
        self.worker_info = None

    def update_unit_info(self, info):
        self.tank_info = info.tank
        self.scout_info = info.scout
        self.worker_info = info.worker

    def update_units(self, unit_updates):
        for update in unit_updates:
            unit = self.unit_for_id(update.id)
            unit.update = update
            self.update_strategy(unit)

    def unit_for_id(self, unit_id):
        if unit_id not in self.units:
            self.units[unit_id] = Unit()
        return self.units[unit_id]

    def update_strategy(self, unit):
        self.strategy_factory.assign_strategy(unit, self.game_map, self)

    def tank_count(self):
        return self.unit_count(lambda u: u.is_tank())

    def worker_count(self):
        return self.unit_count(lambda u: u.is_worker())

    def scout_count(self):
        return self.unit_count(lambda u: u.is_scout())

    def unit_count(self, selector):
        units = filter(selector, self.units.values())
        alive = filter(lambda u: u.is_alive(), units)
        return len(list(alive))

    def range(self, unit):
        if unit.is_tank():
            return self.tank_info.range
        elif unit.is_scout():
            return self.scout_info.range
        else:
            return self.worker_info.range


class GameStateManager:
    def __init__(self, unit_manager, game_map):
        self.unit_manager = unit_manager
        self.game_map = game_map

    def handle_game_update(self, update):
        if update.game_info:
            self.update_game_info(update.game_info)
        if update.unit_updates:
            self.unit_manager.update_units(update.unit_updates)
        if update.tile_updates:
            self.game_map.update_tiles(update.tile_updates)

    def update_game_info(self, game_info):
        self.game_map.set_size(game_info.map_width, game_info.map_height)
        self.unit_manager.update_unit_info(game_info.unit_info)
