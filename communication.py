import json
import socketserver as ss
import sys
from mapping import Direction
from update import GameUpdate


serialize_map = {
    Direction.NORTH: "N",
    Direction.SOUTH: "S",
    Direction.EAST: "E",
    Direction.WEST: "W"
}


def serialize_direction(direction):
    return serialize_map[direction]


def build_move_command(unit, direction):
    if direction is Direction.NONE:
        return None
    serialized_direction = serialize_direction(direction)
    return {
        "command": 'MOVE',
        "unit": unit.id(),
        "dir": serialized_direction
    }


def build_shoot_command(unit, location):
    return {
        "command": 'SHOOT',
        "unit": unit.id(),
        "dx": location.x - unit.location().x,
        "dy": location.y - unit.location().y
    }


def build_unit_command(unit_type):
    return {
        "command": 'CREATE',
        "type": unit_type
    }


def build_gather_command(unit, direction):
    serialized_direction = serialize_direction(direction)
    return {
        "command": 'GATHER',
        "unit": unit.id(),
        "dir": serialized_direction
    }


class UpdateHandler:
    def __init__(self, state_manager, ai_strategy):
        self.state_manager = state_manager
        self.ai_strategy = ai_strategy

    def build_commands_for_update(self, update):
        self.state_manager.handle_game_update(update)
        return self.ai_strategy.build_command_list()


def network_handler_factory(update_handler):
    class NetworkHandler(ss.StreamRequestHandler):
        def __init__(self, *args, **kwargs):
            super(NetworkHandler, self).__init__(*args, **kwargs)
            self.update_handler = update_handler

        def handle(self):
            while True:
                update = self.read_update()
                commands = update_handler.build_commands_for_update(update)
                self.send_response(commands)

        def read_update(self):
            try:
                data = self.rfile.readline().decode().strip()
            except:
                sys.exit()
            if not data:
                sys.exit()
            json_data = json.loads(str(data))
            # uncomment the following line to see pretty-printed data
            # print("Read update:")
            # print(json.dumps(json_data, indent=4, sort_keys=True))
            return GameUpdate(json_data)

        def send_response(self, commands):
            command_list = {"commands": commands}
            response = json.dumps(command_list, separators=(',', ':')) + '\n'
            # print("Sending response:")
            # print(response)
            self.wfile.write(response.encode())

    return NetworkHandler


def accept_connections(host, port, handler):
    network_handler = network_handler_factory(handler)
    server = ss.TCPServer((host, port), network_handler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()
