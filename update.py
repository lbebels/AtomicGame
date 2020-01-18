
class UnitInfo:
    def __init__(self, data):
        self.hp = data.get("hp")
        self.range = data.get("range")
        self.cost = data.get("cost")
        self.speed = data.get("speed")
        self.attack_damage = data.get("attack_damage")
        self.attack_type = data.get("attack_type")
        self.attack_cooldown_duration = data.get("attack_cooldown_duration")
        self.can_carry = data.get("can_carry")
        self.create_time = data.get("create_time")


class UnitInfos:
    def __init__(self, data):
        self.scout = UnitInfo(data["scout"]) if "scout" in data else None
        self.tank = UnitInfo(data["tank"]) if "tank" in data else None
        self.worker = UnitInfo(data["worker"]) if "worker" in data else None
        self.base = UnitInfo(data["base"]) if "base" in data else None


class GameInfo:
    def __init__(self, data):
        self.game_duration = data.get("game_duration")
        self.map_height = data.get("map_height")
        self.map_width = data.get("map_width")
        self.turn_duration = data.get("turn_duration")
        self.unit_info = UnitInfos(data.get("unit_info", {}))


class ResourceUpdate:
    def __init__(self, data):
        self.id = data.get("id")
        self.type = data.get("type")
        self.total = data.get("total")
        self.value = data.get("value")


class TileUpdate:
    def __init__(self, data):
        self.visible = data.get("visible")
        self.blocked = data.get("blocked")
        self.x = data.get("x")
        self.y = data.get("y")
        if "resources" in data and data["resources"] is not None:
            self.resource = ResourceUpdate(data["resources"])
        else:
            self.resource = None
        self.units = [UnitUpdate(unit) for unit in data.get("units", [])]


class UnitUpdate:
    def __init__(self, data):
        self.id = data.get("id")
        self.x = data.get("x")
        self.y = data.get("y")
        self.resource = data.get("resource")
        self.health = data.get("health")
        self.player_id = data.get("player_id")
        self.type = data.get("type")
        self.can_attack = data.get("can_attack")
        self.attack_damage = data.get("attack_damage")
        self.attack_cooldown_duration = data.get("attack_cooldown_duration")
        self.attack_cooldown = data.get("attack_cooldown")
        self.attack_type = data.get("attack_type")
        self.status = data.get("status")
        self.range = data.get("range")
        self.speed = data.get("speed")


class GameUpdate:
    def __init__(self, data):
        self.player = data.get("player")
        self.time = data.get("time")
        self.turn = data.get("turn")
        self.game_info = GameInfo(data.get("game_info")) if "game_info" in data else None
        self.tile_updates = [TileUpdate(tile) for tile in data.get("tile_updates", [])]
        self.unit_updates = [UnitUpdate(unit) for unit in data.get("unit_updates", [])]


