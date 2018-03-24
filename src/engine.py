import tdl
import tcod
from consts import *
from handle_input import *
from unit import *
from message_console import *
from message import Message


def main():

    running = True
    while not tdl.event.is_window_closed() and running:

        # Unit drawing
        Player.draw()

        # Message Console drawing
        MesCon.draw()

        tdl.flush()

        # Clear all sub consoles for next loop
        Player.clear()
        MesCon.clear()

        # Event handling/ Logic
        input = tdl.event.key_wait()
        action = handle_input(input)
        move = action.get("move")
        escape = action.get("exit")

        if move:
            Player.move(move)
        if escape:
            running = False

        # Grab messages from the last turn to draw
        MesCon.update(Player.output_messages())


if __name__ == "__main__":

    # Root console, DO NOT DRAW ONTO THIS, ONLY BLIT
    tdl.set_font(FONT_PATH, greyscale=False, altLayout=True)
    Root = tdl.init(SCREEN_X, SCREEN_Y, title=GAME_TITLE, fullscreen=True)

    # The console we actually draw onto
    Con = tdl.Window(Root, 0, 0, None, None)

    StartMessage = Message(STARTING_MESSAGE)
    # The console our messages are drawn onto
    MesCon = MessageConsole(SCREEN_X, SCREEN_Y, root=Root, current=[StartMessage])

    # TODO: Replace this with player creation
    # Player character
    Player = Unit(x=CENTER_X, y=CENTER_Y, char='@', bg=None, fg=(255,255,255), console=Root)

    main()


