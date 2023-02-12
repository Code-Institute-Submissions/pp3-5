"""Module providing TUI (text user interface) functionality"""
import curses
import time


FPS = 60


def game_loop(screen):
    """
        Main game loop, handles all game updates and drawing to the screen
    """

    cursor_x, cursor_y = 0, 0

    running = True
    while running:
        frame_start = time.time()

        screen.clear()
        height, width = screen.getmaxyx()

        k = screen.getch()
        if k == ord("q"):
            running = False
        elif k == curses.KEY_DOWN:
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

        # limit framerate to `FPS`
        frame_end = time.time()
        frame_delta = frame_end - frame_start
        if frame_delta < 1 / FPS:
            time.sleep(1 / FPS - frame_delta)


def main(screen):
    """
        Main program entrypoint
    """

    screen.clear()
    screen.refresh()
    screen.nodelay(1)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)

    game_loop(screen)


if __name__ == "__main__":
    curses.wrapper(main)
