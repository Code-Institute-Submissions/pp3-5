"""
    Snake game using curses for graphics and input
"""

import curses
import enum
import random
import time
from typing import List
from dataclasses import dataclass


# +----------------------------------------------------+
# |                     CONSTANTS                      |
# +----------------------------------------------------+


FPS = 60
GAME_WIDTH = 15
GAME_HEIGHT = 10
SNAKE_MOVE_DELAY = 10
BORDER_CHARS = ("|", "|", "-", "-", "+", "+", "+", "+")


# +----------------------------------------------------+
# |                  UTILITY CLASSES                   |
# +----------------------------------------------------+


class Direction(enum.IntEnum):
    """
        Enum for the directions the snake can travel
    """

    # opposite inputs add to 3
    UP = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3
    NONE = -1


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

    def copy(self) -> "Point":
        """
            Returns a shallow copy of this point
        """

        return Point(self.x, self.y)


class Segment:
    """
        A segment of the snake's body
    """

    def __init__(self, pos: Point):
        self.pos = pos

    def __eq__(self, other):
        return self.pos == other.pos

    def draw(self, window):
        """
            Draw the segment to the screen
        """

        draw_square(window, self.pos, Colors.SNAKE)


# +----------------------------------------------------+
# |                    MAIN CLASSES                    |
# +----------------------------------------------------+


class Game:
    """
        The whole game state. Controls the gameplay, graphics, etc.
    """

    def __init__(self, screen, game_win, score_win):
        self.screen = screen
        self.game_win = game_win
        self.score_win = score_win

        self.snake = Snake()
        self.apple = Apple(self.snake)

        # number of frames since the game started
        self.frame_count = 0
        self.score = 0
        self.inputs: List[Direction] = []

    def handle_input(self) -> bool:
        """
            Handle the player's input, adding a direction to the
            input queue if necessary
        """

        k = self.screen.getch()

        # if the player presses q, close the game
        if k == ord("q"):
            return False

        # add the player input direction to the input queue
        if k == curses.KEY_UP:
            self.inputs.append(Direction.UP)
        elif k == curses.KEY_DOWN:
            self.inputs.append(Direction.DOWN)
        elif k == curses.KEY_LEFT:
            self.inputs.append(Direction.LEFT)
        elif k == curses.KEY_RIGHT:
            self.inputs.append(Direction.RIGHT)

        return True

    def draw(self):
        """
            Update the game's graphics: the snake, apple, score, windows, etc.
        """

        # clear the screen
        self.game_win.erase()
        self.game_win.border(*BORDER_CHARS)
        self.score_win.erase()
        self.score_win.border(*BORDER_CHARS)

        # draw the snake and apple to the window
        self.snake.draw(self.game_win)
        self.apple.draw(self.game_win)

        # update the score
        draw_score(self.score_win, self.score)

        # update the display with what has been drawn
        self.game_win.refresh()
        self.score_win.refresh()

    def update(self) -> bool:
        """
            Update the game's state
        """

        frame_start = time.time()

        # read the player input
        running = self.handle_input()

        # update the snake and apple
        if not self.snake.is_dead:
            self.snake.update(self.frame_count, self.inputs)
            if self.snake.head.pos == self.apple.pos:
                self.apple.set_new_pos(self.snake)
                self.snake.add_segment(self.snake.head)
                self.score += 1

        self.draw()

        # limit framerate to `FPS`
        frame_end = time.time()
        frame_delta = frame_end - frame_start
        if frame_delta < 1 / FPS:
            time.sleep(1 / FPS - frame_delta)

        self.frame_count += 1

        return running


class Snake:
    """
        The snake that the player controls using the arrow keys
    """

    def __init__(self):
        self.head = Segment(Point(GAME_HEIGHT // 2, GAME_WIDTH // 2))
        self.body_segments: List[Segment] = [self.head]
        self.is_dead = False

        # leave the snake stationary at the start
        self.prev_input = Direction.NONE
        self.cur_input = None

    def update(self, frame_count, inputs):
        """
            Update the snake's state based on the inputs
        """

        if frame_count % SNAKE_MOVE_DELAY == 0:
            # if the player didn't input anything, continue moving in the
            # same direction
            self.cur_input = None
            if len(inputs) == 0:
                self.cur_input = self.prev_input
            else:
                self.cur_input = inputs.pop(0)

            # don't change direction if the snake would turn back on itself
            if self.cur_input + self.prev_input == 3:
                self.cur_input = self.prev_input

            # apply the movement direction to the snake
            self.move(self.cur_input)
            self.prev_input = self.cur_input

    def move(self, direction: Direction):
        """
            Move the snake's head in a direction, and have its body follow it
        """

        prev_head = self.head.pos.copy()

        # move head based on direction passed in
        if direction == Direction.UP:
            self.head.pos.y -= 1
        elif direction == Direction.DOWN:
            self.head.pos.y += 1
        elif direction == Direction.LEFT:
            self.head.pos.x -= 1
        elif direction == Direction.RIGHT:
            self.head.pos.x += 1

        # clamp snake position to stay within the game window
        self.head.pos.x = clamp(self.head.pos.x, 0, GAME_WIDTH - 1)
        self.head.pos.y = clamp(self.head.pos.y, 0, GAME_HEIGHT - 1)

        # the snake dies if it hits a wall (if the above clamps succeed)
        if self.head.pos == prev_head and direction != Direction.NONE:
            self.is_dead = True
            return

        # the snake dies if it crashes into itself
        if self.head in self.body_segments[1:-1]:
            self.is_dead = True
            return

        # body follows after head by moving the last segment to the head's
        # position on the previous frame
        if len(self.body_segments) > 1:
            tail = self.body_segments.pop()
            tail.pos.x = prev_head.x
            tail.pos.y = prev_head.y
            self.body_segments.insert(1, tail)

    def draw(self, window):
        """
            Draw the snake to the window
        """

        self.head.draw(window)
        for segment in self.body_segments:
            segment.draw(window)

    def add_segment(self, segment: Segment):
        """
            Add a segment to the snake's body
        """

        pos = segment.pos.copy()
        self.body_segments.append(Segment(pos))

    def check_overlap(self, pos: Point) -> bool:
        """
            Check if a point `pos` overlaps with the snake's body
        """

        for segment in self.body_segments:
            if segment.pos == pos:
                return True

        return False


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
        while snake.check_overlap(self.pos):
            self.pos = Point(
                random.randrange(0, GAME_WIDTH),
                random.randrange(0, GAME_HEIGHT)
            )

    def draw(self, window):
        """
            Draw the apple to the window
        """

        draw_square(window, self.pos, Colors.APPLE)


# +----------------------------------------------------+
# |                 UTILITY FUNCTIONS                  |
# +----------------------------------------------------+


def clamp(num: int, lower: int, upper: int) -> int:
    """
        Clamp `num` between `lower` and `upper`
    """

    if num > upper:
        return upper

    if num < lower:
        return lower

    return num


# +----------------------------------------------------+
# |                  MAIN FUNCTIONS                    |
# +----------------------------------------------------+


def draw_square(window, pos: Point, color: Colors):
    """
        Draw a square in `window` at `pos` with `color`
    """

    window.attron(curses.color_pair(color))
    window.addstr(pos.y + 1, pos.x * 2 + 1, "  ")
    window.attroff(curses.color_pair(color))


def draw_score(score_win, score: int):
    """
        Write the player's score in the score subwindow

        Example:
        +--------------------+
        |  SCORE   |   13    |
        +--------------------+
    """

    _y, x = score_win.getmaxyx()
    center = x // 2

    score_win.attron(curses.color_pair(Colors.TEXT))

    # write the word "SCORE" in the left half, center aligned
    score_win.addstr(1, 1, f"{'SCORE': ^{center - 1}}")

    # write a pipe character in the middle as a separator
    score_win.addstr(1, center, "|")

    # write the score in the right half, center aligned
    score_win.addstr(1, center + 1, f"{score: ^{center - 2}}")

    score_win.attroff(curses.color_pair(Colors.TEXT))


# +----------------------------------------------------+
# |                PROGRAM ENTRYPOINT                  |
# +----------------------------------------------------+


def main(screen):
    """
        Main program entrypoint
    """

    # initialize the screen
    screen.erase()
    screen.refresh()

    # make `getch` non-blocking
    screen.nodelay(1)

    # turn off the cursor
    curses.curs_set(0)

    # initialize colors used for the game
    curses.init_pair(Colors.TEXT, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(Colors.SNAKE, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(Colors.APPLE, curses.COLOR_RED, curses.COLOR_RED)

    # get screen size
    screen_height, screen_width = screen.getmaxyx()

    # initialize game subwindow with border
    game_h = GAME_HEIGHT + 2
    game_w = GAME_WIDTH * 2 + 2
    game_y = screen_height // 2 - GAME_HEIGHT // 2
    game_x = screen_width // 2 - GAME_WIDTH
    game_win = screen.subwin(game_h, game_w, game_y, game_x)

    # initialize score subwindow with border
    score_h = 3
    score_w = game_w
    score_y = game_y - 2
    score_x = game_x
    score_win = screen.subwin(score_h, score_w, score_y, score_x)

    game = Game(screen, game_win, score_win)

    try:
        # update the game until the player quits
        while game.update():
            pass
    finally:
        # turn the cursor back on after the game ends
        curses.curs_set(1)


if __name__ == "__main__":
    curses.wrapper(main)
