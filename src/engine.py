import tdl
import esper
from consts import *
from handle_input import *
from unit import *
from windows import *
from ecs.ecs_processors import *


def main():

    running = True
    while running and not tdl.event.is_window_closed():

        World.process()

        # Message Console drawing
        MesWin.draw()

        Root.blit(Con)

        tdl.flush()

        # Event handling/ Logic
        button = tdl.event.key_wait()
        action = handle_input(button)
        move = action.get("move")
        escape = action.get("exit")

        if move:
            x = move[0]
            y = move[1]
            PCMovingComp.x = x
            PCMovingComp.y = y
        if escape:
            running = False

        # Grab messages from the last turn to draw
        #MesWin.process(Player.output_messages())

        World.process()


if __name__ == "__main__":

    # Root console
    tdl.set_font(FONT_PATH, greyscale=True, altLayout=True)
    Root = tdl.init(SCREEN_X, SCREEN_Y, title=GAME_TITLE, fullscreen=True)

    # The console we create windows from
    Con = tdl.Console(SCREEN_X, SCREEN_Y)

    # The window our messages are drawn onto
    StartMessage = [START_MESSAGE]
    MesWin = MessageWindow(SCREEN_X, SCREEN_Y, root=Con, current=StartMessage)

    GWin = tdl.Window(Con, 0, MesWin.y, None, None)

    World = esper.World()

    Player = World.create_entity()
    World.add_component(Player, Moving(x=0, y=0))
    World.add_component(Player, Renderable(0, 0, "@"))
    World.add_component(Player, Logging())
    PCMovingComp = World.component_for_entity(Player, Moving)

    render_processor = RenderProcessor(GWin)
    World.add_processor(render_processor)

    movement_processor = MovementProcessor(SCREEN_X, SCREEN_Y)
    World.add_processor(movement_processor)

    looping_processor = LoopingProcessor(GWin)
    World.add_processor(looping_processor)

    logging_processor = LoggingProcessor(MesWin)
    World.add_processor(logging_processor)

    main()


