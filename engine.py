import tcod
from consts import *
from handle_keys import *
from object import *


def main():

    key = tcod.Key()
    mouse = tcod.Mouse()

    running = True
    while not tcod.console_is_window_closed() and running:

        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_put_char(con, player.x, player.y, player.char, tcod.BKGND_NONE)
        tcod.console_blit(con, 0, 0, SCREEN_X + 1, SCREEN_Y, 0, 0, 0)
        tcod.console_flush()
        tcod.console_put_char(con, player.x, player.y, 0, tcod.BKGND_NONE)

        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)
        action = handle_keys(key)
        move = action.get("move")
        exit = action.get("exit")

        if move:
            player.move(move)
        if exit:
            running = False
        # TODO: use handle_keys and dictionaries to parse and perform actions


if __name__ == "__main__":
    tcod.console_set_custom_font(FONT_PATH, tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GRAYSCALE)
    tcod.console_init_root(SCREEN_X, SCREEN_Y, GAME_TITLE)
    con = tcod.console_new(SCREEN_X, SCREEN_Y)

    player = Object(CENTER_X, CENTER_Y, T_PLAYER)

    main()


