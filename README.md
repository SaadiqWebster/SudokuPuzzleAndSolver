# Sudoku Puzzle And Solver
made in Python, GUI with Tkinter. 
requires both sudokusolver.py and sudokusolverGUI.py, but only need to run the gui.

Begins in Setup Mode.
In Setup Mode, you must click a cell to enter a value.
These values will be the base board and cannot be changed while solving.
When the board is complete there are two options for solving: Play and Auto-Solve.

Switch to Play Mode by pressing the Play button. 
In Play Mode, you enter values in empty cells in an attempt to complete the given base board.
To check if your answers are correct, you must press the Check button, which replaces the Play button.
If a value does not follow the rule of Sudoku, then the cell will be highlighted in red.

Switch to Auto-Solve Mode by pressing the Auto-Solve button.
The program will attempt to solve the board using the Backtracking algorithm.
When the board is complete, it will display the answer as well as the time it took to complete in milliseconds.

To reset the puzzle and begin a new one, press the Clear button. It will switch back to Setup Mode.
You cannot switch to Auto-Solve Mode while in Play Mode and vice versa.

Have fun and enjoy the challenge!


Rules of Sudoku:
1.  All cells must filled with a number between 1 and 9
2.  Each row in the board can only contain each number (1-9) once
3.  Each column in the board can only contain each number (1-9) once
4.  Each 3x3 grid box in the board can only contain each number (1-9) once

The puzzle is complete when all empty cells are filled with numbers that satisfy the above conditions.
