"""
    Snake game using curses for graphics and input
"""

import curses
import enum
import time
from dataclasses import dataclass


FPS = 60
GAME_WIDTH = 20
GAME_HEIGHT = 20
SNAKE_MOVE_DELAY = 10


class Direction(enum.IntEnum):
    """
        Enum for the directions the snake can travel
    """

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Colors(enum.IntEnum):
    """
        Enum for colors to be used when drawing
    """

    TEXT = 1
    SNAKE = 2
    APPLE = 3


@dataclass
class Segment:
    """
        A segment/cell of the snake
    """
    x: int
    y: int


class Snake:
    """
        The snake that the player controls using the arrow keys
    """

    def __init__(self):
        self.head = Segment(GAME_HEIGHT // 2, GAME_WIDTH // 2)

    def move(self, direction: Direction):
        """
            Move the snake's head in a direction, and have its body follow it
        """

        if direction == Direction.UP:
            self.head.y -= 1
        elif direction == Direction.DOWN:
            self.head.y += 1
        elif direction == Direction.LEFT:
            self.head.x -= 1
        elif direction == Direction.RIGHT:
            self.head.x += 1

        # clamp snake position to stay within the game window
        self.head.x = clamp(self.head.x, 0, GAME_WIDTH - 1)
        self.head.y = clamp(self.head.y, 0, GAME_HEIGHT - 1)

    def draw(self, screen):
        """
            Draw the snake to the screen
        """

        screen.attron(curses.color_pair(Colors.SNAKE))
        screen.addstr(self.head.y, self.head.x * 2, "  ")
        screen.attroff(curses.color_pair(Colors.SNAKE))


def clamp(num: int, lower: int, upper: int) -> int:
    """
        Clamp `num` between `lower` and `upper`
    """

    if num > upper:
        return upper

    if num < lower:
        return lower

    return num


def game_loop(screen):
    """
        Main game loop, handles all game updates and drawing to the screen
    """

    snake = Snake()

    # set initial direction to right
    previous_input = Direction.RIGHT

    # number of frames since the game started
    frame_count = 0

    # pylint: disable=unsubscriptable-object
    inputs: list[Direction] = []

    running = True
    while running:
        frame_start = time.time()

        # clear the screen
        screen.clear()

        # read the player input
        current_input = None
        k = screen.getch()
        # if the player presses q, close the game
        if k == ord("q"):
            running = False
        # add the player input direction to the input queue
        elif k == curses.KEY_UP:
            inputs.append(Direction.UP)
        elif k == curses.KEY_DOWN:
            inputs.append(Direction.DOWN)
        elif k == curses.KEY_LEFT:
            inputs.append(Direction.LEFT)
        elif k == curses.KEY_RIGHT:
            inputs.append(Direction.RIGHT)

        if frame_count % SNAKE_MOVE_DELAY == 0:
            # if the player didn't input anything, continue moving in the
            # same direction
            if len(inputs) == 0:
                current_input = previous_input
            else:
                current_input = inputs.pop(0)

            # apply the movement direction to the snake
            snake.move(current_input)
            previous_input = current_input

        # draw the snake to the screen
        snake.draw(screen)

        # update the display with what has been drawn
        screen.refresh()

        # limit framerate to `FPS`
        frame_end = time.time()
        frame_delta = frame_end - frame_start
        if frame_delta < 1 / FPS:
            time.sleep(1 / FPS - frame_delta)

        frame_count += 1


def main(screen):
    """
        Main program entrypoint
    """

    # initialize the screen
    screen.clear()
    screen.refresh()

    # make `getch` non-blocking
    screen.nodelay(1)

    # turn off the cursor
    curses.curs_set(0)

    # initialize colors used for the game
    curses.init_pair(Colors.TEXT, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(Colors.SNAKE, curses.COLOR_GREEN, curses.COLOR_GREEN)

    # turn the cursor back on after the game ends
    try:
        game_loop(screen)
    finally:
        curses.curs_set(1)


if __name__ == "__main__":
    curses.wrapper(main)
