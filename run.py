"""
    Snake game using curses for graphics and input
"""

import curses
import enum
import random
import time
from typing import List
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
class Point:
    """
        A 2D position in the game
    """
    x: int
    y: int


class Snake:
    """
        The snake that the player controls using the arrow keys
    """

    def __init__(self):
        self.head = Point(GAME_HEIGHT // 2, GAME_WIDTH // 2)

        # set initial direction to right
        self.prev_input = Direction.RIGHT
        self.cur_input = None

    def update(self, frame_count, inputs):
        """
            Update the snake's state
        """

        if frame_count % SNAKE_MOVE_DELAY == 0:
            # if the player didn't input anything, continue moving in the
            # same direction
            self.cur_input = None
            if len(inputs) == 0:
                self.cur_input = self.prev_input
            else:
                self.cur_input = inputs.pop(0)

            # apply the movement direction to the snake
            self.move(self.cur_input)
            self.prev_input = self.cur_input

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


class Apple:
    """
        Apple that the snake can eat to make its body longer
    """

    def __init__(self, snake: Snake):
        self.set_new_pos(snake)

    def set_new_pos(self, snake: Snake):
        """
            Place the apple in a new random position that doesn't
            overlap with the snake
        """
        self.pos = Point(
            random.randrange(0, GAME_WIDTH),
            random.randrange(0, GAME_HEIGHT)
        )

        # ensure the apple doesn't overlap the snake
        while self.pos == snake.head:
            self.pos = Point(
                random.randrange(0, GAME_WIDTH),
                random.randrange(0, GAME_HEIGHT)
            )

    def draw(self, screen):
        """
            Draw the apple to the screen
        """

        screen.attron(curses.color_pair(Colors.APPLE))
        screen.addstr(self.pos.y, self.pos.x * 2, "  ")
        screen.attroff(curses.color_pair(Colors.APPLE))


def clamp(num: int, lower: int, upper: int) -> int:
    """
        Clamp `num` between `lower` and `upper`
    """

    if num > upper:
        return upper

    if num < lower:
        return lower

    return num


def handle_input(k: int, inputs: List[Direction]) -> bool:
    """
        Handle the player's input, adding a direction to the
        input queue if necessary
    """

    # if the player presses q, close the game
    if k == ord("q"):
        return False

    # add the player input direction to the input queue
    if k == curses.KEY_UP:
        inputs.append(Direction.UP)
    elif k == curses.KEY_DOWN:
        inputs.append(Direction.DOWN)
    elif k == curses.KEY_LEFT:
        inputs.append(Direction.LEFT)
    elif k == curses.KEY_RIGHT:
        inputs.append(Direction.RIGHT)

    return True


def game_loop(screen):
    """
        Main game loop, handles all game updates and drawing to the screen
    """

    snake = Snake()
    apple = Apple(snake)

    # number of frames since the game started
    frame_count = 0

    inputs: List[Direction] = []

    running = True
    while running:
        frame_start = time.time()

        # clear the screen
        screen.clear()

        # read the player input
        k = screen.getch()
        running = handle_input(k, inputs)

        # update the snake and apple
        snake.update(frame_count, inputs)
        if snake.head == apple.pos:
            apple.set_new_pos(snake)

        # draw the snake and apple to the screen
        snake.draw(screen)
        apple.draw(screen)

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
    curses.init_pair(Colors.APPLE, curses.COLOR_RED, curses.COLOR_RED)

    # turn the cursor back on after the game ends
    try:
        game_loop(screen)
    finally:
        curses.curs_set(1)


if __name__ == "__main__":
    curses.wrapper(main)
