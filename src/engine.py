import tdl
import tcod
from consts import *
from handle_input import *
from unit import *
from message_console import *
from message import Message


def main():

    running = True
    while not tcod.console_is_window_closed() and running:

        # Unit drawing
        Player.draw(con)

        # Message Console drawing
        MesCon.draw()
        MesCon.blit(con)

        # Moving contents of con to root console
        tcod.console_blit(con, 0, 0, SCREEN_X + 1, SCREEN_Y, 0, 0, 0)
        tcod.console_flush()

        # Clear all sub consoles for next loop
        Player.clear(con)
        MesCon.clear()

        # Event handling/ Logic
        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)
        action = handle_keys(key)
        move = action.get("move")
        escape = action.get("exit")
        message_scroll = action.get("message_scroll")

        if move:
            Player.move(move)
        if escape:
            running = False
        if message_scroll:
            # Makes sure we only skip to the next game loop if we actually have to scroll
            if MesCon.scroll():
                continue

        # Grab messages from the last turn to draw
        MesCon.update(Player.output_messages())


if __name__ == "__main__":

    # Root console, DO NOT DRAW ONTO THIS, ONLY BLIT
    tcod.console_set_custom_font(FONT_PATH, tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GRAYSCALE)
    tcod.console_init_root(SCREEN_X, SCREEN_Y, GAME_TITLE, fullscreen=True)

    # The console we actually draw onto
    con = tcod.console_new(SCREEN_X, SCREEN_Y)
    tcod.console_set_default_foreground(0, tcod.white)

    StartMessage = Message(STARTING_MESSAGE)
    # The console our messages are drawn onto
    MesCon = MessageConsole(SCREEN_X, SCREEN_Y, current=[StartMessage])

    # TODO: Replace this with player creation
    # Player character
    Player = Unit(CENTER_X, CENTER_Y, T_PLAYER, text_color=tcod.green, text_priority=0)

    # Store last key / mouse action
    key = tcod.Key()
    mouse = tcod.Mouse()

    main()


