import random

from esper import World
from src.game.processors.processors import *
from src.game.event_manager import EventManager
from src.game.event import MessageEvent
from src.consts import *
from src.game.components import *


class Level(World):
    def __init__(self, size):
        super().__init__()
        self.width, self.height = self.size = size
        self.message_board = EventManager(self)
        self.i = 0

    def process(self, command):
        self.clear_dead_entities()
        for processor in self._processors:
            processor.process(command)
        return command

    def handle(self, command):
        command = self.process(command)
        return command

    def send_logs(self):
        control = self.get_processor(CommandProcessor)
        logs = self.create_logs()
        if not control.player_turn:
            return []
        try:
            text = logs[self.i]
            self.i += 1
        except IndexError:
            text = logs[-1]

        log = MessageEvent(text, random.choice([WHITE, P_L_GREEN]))

        return [log]

    def clear_dead_entities(self):
        if self._dead_entities:
            for entity in self._dead_entities:
                self.delete_entity(entity, immediate=True)
            self._dead_entities.clear()

    @staticmethod
    def create_logs():
        logs = list()
        logs.append("Welcome to Puzzler!")
        logs.append("There's not much to do as of right now.")
        logs.append("But you can take some and explore this world.")
        logs.append("There's nothing interesting to uncover.")
        logs.append("Nothing to do.")
        logs.append("No one here but you.")
        logs.append("And me, I guess.")
        logs.append("Pretty sure the game might crash at any moment.")
        logs.append("If it does, be sure to tell me what caused it.")
        logs.append("But considering only eight buttons work right now.")
        logs.append("You probably walked off the screen.")
        logs.append("There was a scrolling camera in the game, for a very brief period")
        logs.append("It was bug ridden, so I just deleted it.")
        logs.append("Who knows, maybe you're having fun.")
        logs.append("Modern living tends to get busy.")
        logs.append("Isn't it nice to find a place where you can't do anything.")
        logs.append("You can just sit back, and relax.")
        logs.append("While I keep myself busy with wrangling this project in.")
        logs.append("If you're playing this, you have access to this code.")
        logs.append("If you have any tips, pointers, or suggestions.")
        logs.append("Please contact me at elmi.anas@gmail.com")
        return logs

    def create_processors(self):
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
            self.add_processor(processor, priority=i)

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

        player = self.create_entity()
        for component in components:
            self.add_component(player, component)
