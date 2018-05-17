from esper import World
from src.consts import *
from src.ecs.processors import *
from src.ecs.components import *


class Level(World):
    def __init__(self, size):
        super().__init__()
        self.width, self.height = self.size = size

    def process(self, **kwargs):
        if self._dead_entities:
            for entity in self._dead_entities:
                self.delete_entity(entity, immediate=True)
            self._dead_entities.clear()
        for processor in self._processors:
            processor.process(kwargs)

    def handle(self, command):
        self.process(command=command)

    def update(self):
        pass

    def create_processors(self):
        processors = []

        message_processor = MessageProcessor(START_MESSAGE)
        processors.append(message_processor)
        render_processor = RenderProcessor()
        processors.append(render_processor)
        position_processor = VelocityProcessor()
        processors.append(position_processor)
        action_processor = CommandProcessor()
        processors.append(action_processor)
        act_processor = ActivityProcessor()
        processors.append(act_processor)

        for i, processor in enumerate(processors):
            self.add_processor(processor, priority=i)

    def create_player(self):
        components = []

        player_position = (Positionable(0, 0))
        components.append(player_position)
        player_render = Renderable(char="@", fg=WHITE, priority=0)
        components.append(player_render)
        player_description = Describable("Player", "You", "A young Inquisitor with a freshly sealed writ.")
        components.append(player_description)
        player_controllable = Controllable()
        components.append(player_controllable)
        player_tick = Ticking()
        components.append(player_tick)
        player_vel = Velocity()
        components.append(player_vel)

        player = self.create_entity()
        for component in components:
            self.add_component(player, component)
