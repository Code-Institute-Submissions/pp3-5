"""Module providing TUI (text user interface) functionality"""
import curses


def draw_menu(screen):
    k = 0
    cursor_x, cursor_y = 0, 0

    screen.clear()
    screen.refresh()

    while k != ord("q"):
        screen.clear()
        height, width = screen.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y += 1
        elif k == curses.KEY_UP:
            cursor_y -= 1
        elif k == curses.KEY_RIGHT:
            cursor_x += 1
        elif k == curses.KEY_LEFT:
            cursor_x -= 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width - 1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height - 1, cursor_y)

        screen.move(cursor_y, cursor_x)

        screen.refresh()

        k = screen.getch()


def main():
    """Main program entrypoint"""
    curses.wrapper(draw_menu)


if __name__ == "__main__":
    main()
