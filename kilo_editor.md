<!---
vim:foldmethod=syntax:nospell
--->
# Build Your Own Text Editor

This is a note about writing a kilo-like editor in C from scratch.
For more details, visit https://viewsourcecode.org/snaptoken/kilo/index.html .

## 1. Setup

*In this chapter, author discussed about how to install a C compiler on
multiple platforms and compile with make, which are totally basic.*

## 2. Entering raw mode

### read form standard input scream

Use `read(STDIN_FILENO, &c, 1)` function

### Press `q` to quit

`while (read( /*...*/ ) == 1 && c != 'q')`

### Edit some terminal's attributes

Set a terminal's attributes by (1) using `tcgetattr()` (from `<termios.h>`) to
read the current attributes into a structure, (2) modifying the scratch, and
(3) passing the modified structure to `tcsetattr()` to write the new terminal
attributes back out. We write a function named `void enableRawMode()` that
contains:
```c
struct termios raw;
tcgetattr(STDIN_FILENO, &raw);              // (1)
/* edit */                                  // (2)
tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);   // (3)
```

In `/* edit */` field, we use:
```c
raw.c_iflag &= ~BRKINT;     // carried by default, prevent break condition be sent like Ctrl-C
raw.c_iflag &= ~ICRNL;      // fix Ctrl-M, prevent the translation form '\r' to '\n' carried by terminal
raw.c_iflag &= ~INPCK;      // carried by default, disable parity checking
raw.c_iflag &= ~ISTRIP;     // carried by default, unstrip the 8th bit of each input byte
raw.c_iflag &= ~IXON;       // disable Ctrl-S and Ctrl-Q
raw.c_oflag &= ~OPOST;      // turn off output processing, '\n' to '\r\n' for example
                            // from now, '\r\n' should be used instead of '\n'
raw.c_cflag |= CS8;         // carried by default, set the character size to 8 bits pre byte
raw.c_lflag &= ~ECHO;       // turn off echoing
raw.c_lflag &= ~ICANON;     // turn off canonical mode and read input byte by byte
raw.c_lflag &= ~IEXTEN;     // disable Ctrl-V
raw.c_lflag &= ~ISIG;       // turn off Ctrl-C and Ctrl-Z signals
raw.c_cc[VMIN] = 0;         // read as soon as there is any input
raw.c_cc[VTIME] = 1;        // maximum read out time in tenths of a second
```

### Disable raw mode at exit

Save a copy of the termios structure in its original state and use `tcsetattr()`
to apply it to the terminal when the program exits.
```c
struct termios orig_termios;

void disableRawMode() {
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &orig_termios);
}

void enableRawMode() {
    tcgetattr(STDIN_FILENO, &orig_termios);
    atexit(disableRawMode);             // execute disableRawMode() at exit
    
    struct termios raw = orig_termios;
    ...
}
```

### Error handling

Add a `die()` function that prints an error message and exits the program
```c
void die(const char *s) {
        perror(s);
        exit(1);
}
```

Add `die` when `tcgetattr` (falls when given a text file or a pipe as the standard
input instead of the terminal) and `tcsetattr`, and modify the read line to
`if (read(STDIN_FILENO, &c, 1) == -1 && errno != EAGAIN) die("read"); `, where
`errno` and `EAGAIN` come from `<errno.h>`, which make it work in Cygwin.

## 3. Raw input and output

### Press `Ctrl-Q` to quit

***Letters modified by `Ctrl` map to bytes 1-26, so we can use this to detect `Ctrl`
key combinations and map them to different operations.*** For example, map `Ctrl-Q` to
the quit operation:
```c
#define CTRL_KEY(k) ((k) & 0x1ff)   // (k) & 00011111b

...
if (c == CTRL_KEY('q')) break;
```

### Refactor keyboard input

Separate read input and process input into two functions `editorReadKey`
and `editorProcessKeypress`

### Clear the screen

Write `\x1b[2J` into STDOUT_FILENO in the function `editorRefreshScreen`, which
`\x1b` is the escape character, or 27 in decimal, and followed by a `[` character
response to an ***escape sequence***. `J` command is used to clear the screen, `2` is the
argument that says clear the entire screen.

### Reposition the cursor

Write `\x1b[H` into STDOUT_FILENO in the function `editorRefreshScreen` to position
the cursor at the top right. Command `H` takes two arguments separated by `;` : the
row number and the column number, and the default arguments both happen to be `1`.

### Clear the screen on exit

Write 2 strings above in `die` function and when `Ctrl-Q` is pressed.

### Tildes

Draw a column of tildes (`~`) on the left hand side of the screen like **vim** does.

Write `~\r\n` for every line in function `editorDrawRows` , call the function and
write `\x1b[H` after the call.

### Global state

Set up a global structure `editorConfig` that contains our editor state like `orig_termios`.

### Window size

Set variables `screenrows` and `screencols` in `editorConfig`, and are initialized in the new function
`initEditor`, which is called in `main`. Define a function `getWindowSize` receiving two
arguments `int *rows` and `int *cols`, sign the rows and cols in two ways:
1) The easy way: call `ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws)` from `sys/ioctl.h`.
2) The hard way(in case `ioctl` doesn't work on some system): Firstly, move the cursor to
the bottom-right corner by writing `\x1b[999C\x1b[999B`. Then, use ``n`` with argument `6` to
ask for the cursor position, and read the reply (like `24;80R`, or similar) from the
standard input. Finally, `read` into a buffer and get the `rows` and `cols` using `sscanf`.

### Last line

Don't `write` `"\r\n"` at the last line

### Append buffer

Since making a whole bunch of small `write()` every time refresh the screen is not a good
idea, which may annoyed us with small unpredictable pauses. So we make a `abuf`
structure and combine all the commands into the buffer and write them at one time.
That is, define functions `abAppend` and `abFree`, replacing all the `write`
with `abAppend`, and place only one `write` and `abFree` at the end of `editorRefreshScreen`.

### Hide the cursor when repainting
