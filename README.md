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

- __High score window__
    - The high score window appears to the right of the game and score windows.
      It shows the player's high scores, i.e. the scores in each game they've played since starting, sorted from highest to lowest.
    - Only the player's top 10 scores can be shown due to the height of the window; the rest will be cut off.

![High score window]()

- __Message window__
    - The message window serves a double purpose: it shows the game's controls to the player, and it presents them with a congratulatory message when the game ends.
    - The congratulatory message varies depending on the player's score when the game ended.
    - The controls shown are Q to quit, and R to retry.
      - Note that retrying is only allowed after the game has ended, not in the middle of a game.
      - Also note that the lack of a pause feature is an intentional game design choice.
      If the player could pause, they could gain an unfair advantage in that they could see the current state of the game and plan ahead for which directions to turn.
      This is contrary to the spirit of the game, as it's design to require the player to think on their feet, not take time to strategize and plan out movements.

![Message window]()

### Features left to implement

- A main menu
- A difficulty setting (setting the snake's speed, game size, number of apples, etc.)
- More readable characters to represent the snake's body than just blocks
