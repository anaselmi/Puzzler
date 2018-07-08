import logging
from esper import World

from logic.processors import *
from consts import *
from commands import update_result
from logging_tools import init_sized_object
from logic.event_manager import EventManager

logger = logging.getLogger(__name__)


class Level:
    def __init__(self, size):
        super().__init__()
        self.width, self.height = self.size = size
        init_sized_object("level", self.size, logger)
        self._world = World()
        logger.debug("New world created.")
        self.events = EventManager(self)
        self.add_processors()
        self.create_player()

    @update_result
    def handle(self, command):
        pass

    def update(self, command):
        self._world.process(command)

    # TODO
    def send_logs(self):
        return [f"This is a test. You need to finish{self.send_logs.__name__}."]

    def add_processors(self):
        processors = []

        message_processor = LoggingProcessor()
        processors.append(message_processor)
        render_processor = RenderProcessor()
        processors.append(render_processor)
        position_processor = VelocityProcessor()
        processors.append(position_processor)
        action_processor = CommandProcessor()
        processors.append(action_processor)
        turn_processor = TurnProcessor()
        processors.append(turn_processor)

        for i, processor in enumerate(processors):
            self._world.add_processor(processor, priority=i)
        print(f"{len(processors)} processor(s) added to the world.")

    # TODO: Move this outside of level.
    def create_player(self):
        components = []

        player_position = (Positionable(0, 0))
        components.append(player_position)
        player_render = Renderable(char="@", fg=WHITE, priority=0)
        components.append(player_render)
        player_description = Describable("Player", "You", "A young Inquisitor with a freshly sealed writ.")
        components.append(player_description)
        player_controllable = Controllable(player=True)
        components.append(player_controllable)
        player_tick = Ticking()
        components.append(player_tick)
        player_vel = Velocity()
        components.append(player_vel)
        player_mes = Logging(START_MESSAGE)
        components.append(player_mes)
        player_act = Active()
        components.append(player_act)

        player = self._world.create_entity()
        for component in components:
            self._world.add_component(player, component)
