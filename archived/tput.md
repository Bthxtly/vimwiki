# tput

`tput`, a command used to manipulate our terminal. With it, we can change the color of text, apply effects, and generally brighten things up. More importantly, we can use tput to improve the human factors of our scripts. For example, we can use color and text effects to better present information to our users.

### Availability
`tput` is part of the `ncurses` package and is supplied with most Linux distributions.

### What is Does/How it Works
Ancient terminals all use different sequences of control characters to manage their screens and keyboards.
The terminal emulator sets the `TERM` environment variable with the name of a *terminal type* when starting a terminal session on Linux system. `xterm-kitty` on kitty for example(others are `linux` for the Linux console and `srceen` for terminal emulators like `screen` and `tmux`, and more and more). We can examine a typical terminfo entry using the `infocmp` command followed by a terminal type name:
```sh
infocmp xterm-kitty

#Reconstructed via infocmp from file: /usr/lib/kitty/terminfo/x/xterm-kitty
xterm-kitty|KovIdTTY,
am, ccc, hs, km, mc5i, mir, msgr, npc, xenl,
  ...
```
The values starting with `\E` (which represents the escape character) are sequences of control codes that cause the terminal to perform an action.

### Reading terminal Attributes
For the following capnames, tput outputs a value to stdout:

| Capname | Description                   |
|-------------|-----------------------------------|
| longname    | Full name of the terminal type    |
| lines       | Number of lines in the terminal   |
| cols        | Number of columns in the terminal |
| colors      | Number of colors available        |

### Controlling the Cursor
The capnames below output strings containing control codes that instruct the terminal to manipulate the cursor:

| Capname         | Description                                |
| --------        | ------------                               |
| sc              | Save the cursor position                   |
| rc              | Restore the cursor position                |
| home            | Move the cursor to upper left corner (0,0) |
| cup <row> <col> | Move the cursor to position (row,col)      |
| cud1            | Move the cursor down 1 line                |
| cuu1            | Move the cursor up 1 line                  |
| civis           | Set to cursor to be invisible              |
| cnorm           | Set the cursor to its normal state         |

### Text Effects
Like the capnames used for cursor manipulation, the following capnames output strings of control codes that affect the way our terminal displays text characters:

| Capname       | Description             |
| --------      | ------------            |
| bold          | Start bold text         |
| smul          | Start underline text    |
| rmul          | End underline text      |
| rev           | Start reverse video     |
| blink         | Start blinking text     |
| invis         | Start invisible text    |
| smso          | Start "standout" mode   |
| rmso          | End "standout" mode     |
| sgr0          | Turn off all attributes |
| setaf <value> | Set foreground color    |
| setaf <value> | Set background color    |

#### Text Color

| Value | Color                  |
| ----- | -----                  |
| 0     | Black                  |
| 1     | Red                    |
| 2     | Green                  |
| 3     | Yellow                 |
| 4     | Blue                   |
| 5     | Magenta                |
| 6     | Cyan                   |
| 7     | White                  |
| 8     | Not used               |
| 9     | Reset to default color |

### Clearing the Screen
These capnames allow us to selectively clear portions of the terminal display:

| Capname | Description                                        |
| ------- | -----------                                        |
| smcup   | Save screen contents                               |
| rmcup   | Restore screen contents                            |
| el      | Clear from the cursor to the end of the line       |
| el1     | Clear from the cursor to the beginning of the line |
| ed      | Clear from the cursor to the end of the screen     |
| clear   | Clear the entire screen and home the cursor        |

## Summing Up
Using `tput`, we can easily add visual enhancements to our scripts. While it’s important not to get carried away, lest we end up with a garish, blinking mess, adding text effects and color can increase the visual appeal of our work and improve the readability of information we present to our users.

<!---
Take notes from https://linuxcommand.org/lc3_adv_tput.php
vim:nospell
--->
