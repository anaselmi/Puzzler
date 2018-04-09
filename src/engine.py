import esper
import tdl
from consts import *
from ecs.ecs_processors import *
from windows import *
from handle_button import *


def main():

    running = True
    while running and not tdl.event.is_window_closed():

        World.process()

        MesWin.draw()

        Root.blit(Con)

        tdl.flush()

        # Event handling/ Logic
        button = tdl.event.key_wait()
        action, value = ButtonMan.process(button)
        state = ButtonMan.state

        if action == "quit_game":
            running = False

        elif state is None:
            if action == "move":
                x = value[0]
                y = value[1]
                PlayerVelocityComp.x = x
                PlayerVelocityComp.y = y

        elif state == "look":
            if action == "change_state":
                CursorRenderableComp.active = True
            if action == "move_cursor":
                x = value[0]
                y = value[1]
                CursorVelocityComp.x = x
                CursorVelocityComp.y = y

        MesWin.clear()
        World.process()


if __name__ == "__main__":

    # Root console
    tdl.set_font(FONT_PATH, greyscale=True, altLayout=True)
    Root = tdl.init(SCREEN_X, SCREEN_Y, title=GAME_TITLE, fullscreen=True)

    # The console we create windows from
    Con = tdl.Console(SCREEN_X, SCREEN_Y)

    # The window our messages are drawn onto
    MesWin = MessageWindow(SCREEN_X, SCREEN_Y, con=Con)

    GWin = tdl.Window(Con, 0, MesWin.y, None, None)

    ButtonMan = HandleButton()

    World = esper.World()

    Player = World.create_entity()
    World.add_component(Player, Velocity())
    World.add_component(Player, Renderable(CENTER_X, CENTER_Y, "@"))
    World.add_component(Player, Describable("Player", "You", "lost Assembler with a freshly minted Royal Seal."))
    World.add_component(Player, Playable())
    PlayerVelocityComp = World.component_for_entity(Player, Velocity)

    Gleamer = World.create_entity()
    World.add_component(Gleamer, Velocity())
    World.add_component(Gleamer, Renderable(30, 30, "g", fg=RED))
    World.add_component(Gleamer, Describable("Kazaram", "The Gleamer", "hunchbacked monstrosity with piercing eyes."))

    Cursor = World.create_entity()
    World.add_component(Cursor, Velocity())
    World.add_component(Cursor, Renderable(20, 20, ".", fg=GREEN, active=False))
    CursorVelocityComp = World.component_for_entity(Cursor, Velocity)
    CursorRenderableComp = World.component_for_entity(Cursor, Renderable)

    render_processor = RenderProcessor(GWin)
    World.add_processor(render_processor)

    movement_processor = MovementProcessor(SCREEN_X, SCREEN_Y)
    World.add_processor(movement_processor)

    looping_processor = LoopingProcessor(GWin)
    World.add_processor(looping_processor)

    logging_processor = LoggingProcessor(MesWin)
    World.add_processor(logging_processor)
    logging_processor.add_messages(START_MESSAGE)

    main()
