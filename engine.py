import tcod
from consts import *
from handle_keys import *
from object import *


def main():

    while not tcod.console_is_window_closed():
        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_put_char(con, player.X, player.Y, player.char, tcod.BKGND_NONE)
        tcod.console_blit(con, 0, 0, SCREEN_X + 1, SCREEN_Y, 0, 0, 0)
        tcod.console_flush()
        tcod.console_put_char(con, player.X, player.Y, '', tcod.BKGND_NONE)

        action = handle_keys()

        if action in PLAYER_ACTION:
            player.act(action)
        elif action in GAME_ACTION:
            pass


if __name__ == "__main__":
    tcod.console_set_custom_font(FONT_PATH, tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GRAYSCALE)
    tcod.console_init_root(SCREEN_X, SCREEN_Y, GAME_TITLE)
    con = tcod.console_new(SCREEN_X, SCREEN_Y)

    player_x, player_y = SCREEN_X // 2, SCREEN_Y // 2
    player = Object(player_x, player_y, "C")

    main()

