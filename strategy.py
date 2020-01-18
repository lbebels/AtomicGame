from strategies.explore import ExploreStrategy


class UnitStrategyFactory:
    def assign_strategy(self, unit, game_map, unit_manager):
        if unit.strategy is None:
            unit.strategy = self.build_strategy(unit, game_map, unit_manager)

    def build_strategy(self, unit, game_map, unit_manager):
        if unit.is_mobile():
            return self.build_explore_strategy(game_map, unit, unit_manager)
        else:
            return None

    @staticmethod
    def build_explore_strategy(game_map, unit, unit_manager):
        return ExploreStrategy(game_map, unit, unit_manager)


class AIStrategy:
    def __init__(self, unit_manager, game_map):
        self.unit_manager = unit_manager
        self.game_map = game_map

    def build_command_list(self):
        commands = [u.build_command() for u in self.unit_manager.units.values()]
        return [c for c in commands if c is not None]
