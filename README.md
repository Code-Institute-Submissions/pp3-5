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

## Testing/Development

At first when coding the graphics system, the terminal would flicker constantly.
I found [this StackOverflow post](https://stackoverflow.com/a/24966639) which helped me figure out that changing my `clear` calls to `erase` would fix the problem.

As well as this, initially the terminal cursor, which is used internally by `curses` to handle all of the graphics, could be seen flashing around the screen all the time.
I found out that typically people using `curses` will set the cursor to be invisible throughout the program, and this worked in my testing.
However, this functionality is terminal-dependent, and doesn't appear to work on the virtual terminal provided to me for this project.
I tried my best to find some workaround for this, like maybe giving the cursor a `display: none` property in CSS, but the terminal runs inside a HTML `<canvas>` so this wasn't possible, and I ultimately couldn't find a fix for it.
I did still allow for terminals that support invisible cursors to hide the cursor, using a `try` block.

I didn't want the game to run incredibly quickly, as I wanted the snake to move at a consistent speed.
The way I saw to do this was by limiting the framerate of the game, by calculating the time spent updating and displaying the game, and `time.sleep`ing for the remaining time in the frame.
I could then set the snake up to move after a consistent number of frames, rather than having to calculate and keep track of the time between each movement.
That would be using what's known as "delta time", which I'm less familiar with.
However, something to note is that delta time would account for any lag experienced by the terminal so that the snake moves after a consistent amount of *time*, rather than a consistent number of *frames*.
The virtual terminal provided does unfortunately experience a little bit of lag sometimes, so if I was remaking this project I would keep this in mind, instead of only finding out when I went to deploy the project. 

Most of my free time is spent reverse engineering my favorite game, [Super Mario Odyssey](https://en.wikipedia.org/wiki/Super_Mario_Odyssey).
This game uses "nerves" to assign each object in the scene a particular state each frame, along with a frame counter for how long it has been in that state.
It also allows them to move between these states depending on different conditions.
I took inspiration from this system when I added states to the snake.
This was a relatively easy way to handle the snake dying and coming back to life when the player wants to retry.

I ran into problems when trying to deploy my project.
When trying to sign up to Heroku, it would consistently show me an error page that I couldn't find a way around.
I contacted a tutor and they said the best course of action would probably be to use another host, such as Render.
To figure this out, I followed [this guide](https://code-institute-students.github.io/deployment-docs/10-pp3/).
