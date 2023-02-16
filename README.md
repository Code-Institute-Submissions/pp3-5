# Snake

This is a version of the classic game Snake, built using the [TUI](https://en.wikipedia.org/wiki/Text-based_user_interface) library `curses`.
The game runs in a virtual terminal on this website, but can also run in any Unix terminal.
The site is aimed towards those who like to spend their free time playing games for fun.

![Responsive markup]()

## Features

- __Game window__
    - The interface is split up into multiple sub-windows for easy viewing, the game window being the main one.
      It contains the snake that the player controls using the arrow keys, as well as the apple that the snake wants to eat.
    - As the player presses the arrow keys, the snake will move around the window.
      When they collect an apple, the snake will get longer by one square.
      Its body will then follow behind its head.
    - The player must be careful not to run into the body as they're looking for the next apple, as this will end the game.
      Running into the walls of the game area will end the game as well.

![Game window]()

- __Score window__
    - The score window appears above the game window.
      It shows the player their current score, with a title to the left.
    - The player's score will be incremented by 1 for each apple they collect.
      If the game ends and the player chooses to retry, the player's score will be reset to 0.

![Score window]()
