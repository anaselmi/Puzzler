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
        state_switch = False

        if action == "quit_game":
            running = False
            continue

        if state is None:
            if action == "move":
                x = value[0]
                y = value[1]
                PlayerVelocityComp.x = x
                PlayerVelocityComp.y = y

        elif state == "look":
            if action == "change_state":
                CursorRenderableComp.active = True
                CursorRenderableComp.x = PlayerRenderableComp.x
                CursorRenderableComp.y = PlayerRenderableComp.y
            if action == "move_cursor":
                x = value[0]
                y = value[1]
                CursorVelocityComp.x = x
                CursorVelocityComp.y = y
            if action == "look":
                target_x = CursorRenderableComp.x
                target_y = CursorRenderableComp.y

            if action == "change_back" and value is None:
                state_switch = True

            if state_switch:
                CursorRenderableComp.active = False
                ButtonMan.state = None

        MesWin.clear()
        World.process()


if __name__ == "__main__":

    # Root console
    tdl.set_font(FONT_PATH, greyscale=True, altLayout=True)
    Root = tdl.init(SCREEN_X, SCREEN_Y, title=GAME_TITLE, fullscreen=True)

    # The console we create windows from
    Con = tdl.Console(SCREEN_X, SCREEN_Y)

    # The window we draw onto drawn onto
    MesWin = MessageWindow(SCREEN_X, SCREEN_Y, con=Con)
    GWin = tdl.Window(Con, 0, MesWin.y, None, None)

    ButtonMan = HandleButton()

    World = esper.World()

    GMap = GameMap(GWin.width, GWin.height, World)

    Player = World.create_entity()
    World.add_component(Player, Renderable("@", priority=2))
    World.add_component(Player, Positionable(CENTER_X, CENTER_Y))
    World.add_component(Player, Velocity())
    World.add_component(Player, Describable("Player", "You", "lost Assembler with a freshly minted Royal Seal."))
    World.add_component(Player, Playable())
    PlayerVelocityComp = World.component_for_entity(Player, Velocity)
    PlayerRenderableComp = World.component_for_entity(Player, Renderable)

    Gleamer = World.create_entity()
    World.add_component(Gleamer, Renderable("g", fg=RED))
    World.add_component(Gleamer, Positionable(30, 30, pathable=False))
    World.add_component(Gleamer, Velocity())
    World.add_component(Gleamer, Describable("Kazaram", "The Gleamer", "hunchbacked monstrosity with piercing eyes."))

    Cursor = World.create_entity()
    World.add_component(Cursor, Renderable(".", fg=GREEN, active=False, priority=3))
    World.add_component(Cursor, Positionable(0, 0, tangible=False))
    World.add_component(Cursor, Velocity())
    CursorVelocityComp = World.component_for_entity(Cursor, Velocity)
    CursorRenderableComp = World.component_for_entity(Cursor, Renderable)

    render_processor = RenderProcessor(GWin)
    World.add_processor(render_processor)

    position_processor = PositionProcessor(GWin, GMap)
    World.add_processor(position_processor, priority=1)

    logging_processor = LoggingProcessor(MesWin)
    World.add_processor(logging_processor)
    logging_processor.add_messages(START_MESSAGE)

    main()
