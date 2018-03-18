import tcod
from consts import *
from handle_input import *
from unit import *
from message_console import *


def main():

    running = True
    while not tcod.console_is_window_closed() and running:

        Player.draw(con)

        MesCon.update_new(Player.get_messages())
        MesCon.draw()
        MesCon.blit(con)

        # Moving contents of con to root console
        tcod.console_blit(con, 0, 0, SCREEN_X + 1, SCREEN_Y, 0, 0, 0)
        tcod.console_flush()

        Player.clear(con)
        MesCon.clear()

        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)
        action = handle_keys(key)
        move = action.get("move")
        escape = action.get("exit")

        if move:
            Player.move(move)
        if escape:
            running = False


if __name__ == "__main__":

    # Root console, DO NOT DRAW ONTO THIS, ONLY BLIT
    tcod.console_set_custom_font(FONT_PATH, tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GRAYSCALE)
    tcod.console_init_root(SCREEN_X, SCREEN_Y, GAME_TITLE, fullscreen=True)

    # The console we actually draw onto
    con = tcod.console_new(SCREEN_X, SCREEN_Y)
    tcod.console_set_default_foreground(0, tcod.white)

    MesCon = MessageConsole(SCREEN_X, SCREEN_Y)

    # TODO: Replace this with player creation
    Player = Unit(CENTER_X, CENTER_Y, T_PLAYER)

    key = tcod.Key()
    mouse = tcod.Mouse()

    main()


