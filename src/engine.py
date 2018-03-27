import tdl
import tcod
from consts import *
from handle_input import *
from unit import *
from windows import *
from message import Message


def main():

    running = True
    while not tdl.event.is_window_closed() and running:

        # Unit drawing
        Player.render()

        # Message Console drawing
        MesWin.draw()

        Root.blit(Con)

        tdl.flush()

        # Clear all sub consoles for next loop
        Player.clear()
        MesWin.clear()

        # Event handling/ Logic
        inpt = tdl.event.key_wait()
        action = handle_input(inpt)
        move = action.get("move")
        escape = action.get("exit")

        if move:
            Player.move(move)
        if escape:
            running = False

        # Grab messages from the last turn to draw
        MesWin.update(Player.output_messages())


if __name__ == "__main__":

    # Root console, DO NOT DRAW ONTO THIS, ONLY BLIT
    tdl.set_font(FONT_PATH, greyscale=True, altLayout=True)
    Root = tdl.init(SCREEN_X, SCREEN_Y, title=GAME_TITLE, fullscreen=True)

    # The console we actually draw onto
    Con = tdl.Console(SCREEN_X, SCREEN_Y)

    StartMessage = Message(STARTING_MESSAGE)
    # The console our messages are drawn onto
    MesWin = MessageWindow(SCREEN_X, SCREEN_Y, root=Con, current=[StartMessage])

    game_y = MesWin.y

    GWin = tdl.Window(Con, 0, game_y, None, None)

    # TODO: Replace this with player creation
    # Player character
    Player = Unit(x=CENTER_X, y=CENTER_Y, char='@', bg=None, fg=WHITE, window=GWin)

    main()


