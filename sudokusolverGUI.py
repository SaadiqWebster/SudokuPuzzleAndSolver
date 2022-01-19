from sudokusolver import *
import tkinter as tk
import time

puzzle = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]
puzzle_original = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]

window = tk.Tk()
window.title("Sudoku Puzzle and Solver")
window.wm_attributes('-toolwindow', 'True')
window.resizable(False, False)

instructions = tk.Label(text="Fill the board with digits between 1 and 9", fg="blue", bg="white", anchor="w")
instructions.pack(fill=tk.BOTH, expand=True)

GigaFrame = tk.Frame(bg="black")
GigaFrame.pack(fill=tk.BOTH, expand=True)

entries = {}
selected_entry_x = -1
selected_entry_y = -1

mode_setup = True
mode_solve = False
mode_play = False

def mouse_click(event):
    global selected_entry_x, selected_entry_y
    
    if mode_setup:
        if selected_entry_x != -1:
            entries[(selected_entry_x, selected_entry_y)].configure(bg="white", fg="black")
        idx = list(entries.values()).index(event.widget)
        selected_entry_x, selected_entry_y = list(entries.keys())[idx]
        entries[(selected_entry_x, selected_entry_y)].configure(bg="grey", fg="black")
    
    elif mode_play:
        prev_i = selected_entry_x
        prev_j = selected_entry_y
        idx = list(entries.values()).index(event.widget)
        selected_entry_x, selected_entry_y = list(entries.keys())[idx]
        
        if puzzle_original[selected_entry_x][selected_entry_y] != 1:
            if prev_i != -1: 
                entries[(prev_i, prev_j)].configure(bg="white", fg="blue")
            entries[(selected_entry_x, selected_entry_y)].configure(bg="#A0B4FF", fg="blue")
        else:
            selected_entry_x = prev_i
            selected_entry_y = prev_j

def makeEntryGrid(row, col):
    Frame = tk.Frame(master=GigaFrame, bg="black")
    for i in range(3):
        for j in range(3):
            numberEntry = tk.Entry(master=Frame, width=5, borderwidth=0, justify="center", insertontime=0)
            numberEntry.bind("<Button-1>", mouse_click)
            numberEntry.grid(row=i, column=j, padx=1, pady=1, ipady=5, sticky="nsew")
            entries[(row+i, col+j)] = numberEntry

    return Frame

def makePlayableBoard():
    for i in range(3):
            for j in range(3):
                MegaFrame = makeEntryGrid(i*3, j*3)
                pad_x = 2
                pad_y = 2

                if j != 0:
                    pad_x = (0,pad_x)
                if i != 0:
                    pad_y = (0,pad_y)
                
                MegaFrame.grid(row=i, column=j, padx=pad_x, pady=pad_y)
makePlayableBoard()

def setOriginalPuzzle():
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                puzzle_original[i][j] = 1

def buttonPressClear():
    global mode_setup, mode_solve, mode_play
    if not mode_solve:
        instructions.configure(text="Fill the board with digits between 1 to 9", fg="blue")
        for i in range(9):
            for j in range(9):
                puzzle[i][j] = 0
                puzzle_original[i][j] = 0
                entries[(i, j)].configure(fg="black", bg="white")
                entries[(i, j)].delete(0,"end")
        mode_setup = True
        mode_play = False
        play_button.configure(text="Play", command=buttonPressPlay)

def identifyErrors(possible_errs):
    err_present = False

    for err in possible_errs:
        if not isValid(puzzle, puzzle[err[0][0]][err[0][1]], err[0][0], err[0][1]):
            err[1].configure(fg="red", bg="#FFB1A0")
            instructions.configure(text="This puzzle is not valid", fg="red")
            err_present = True

    return err_present

def updateEntries():
    global selected_entry_x, selected_entry_y
    
    selected_entry_x = -1
    selected_entry_y = -1
    possible_errs = []

    for i in range(9):
        for j in range(9):
            entries[(i, j)].configure(fg="black", bg="white")
            if entries[(i, j)].get() == "" or entries[(i, j)].get() == "0" or not entries[(i, j)].get().isnumeric():
                entries[(i, j)].delete(0,tk.END)
                puzzle[i][j] = 0
            else:
                puzzle[i][j] = int(entries[(i, j)].get())

            if not isValid(puzzle, puzzle[i][j], i, j):
                possible_errs.append( ((i, j), entries[(i, j)]) )

    print(possible_errs)
    return not identifyErrors(possible_errs)

def buttonPressSolve():
        global mode_setup, mode_solve, mode_play
        
        if isSolvedBoard(puzzle): return
        if mode_play: return
        if not updateEntries(): return
        
        setOriginalPuzzle()

        mode_setup = False
        mode_solve = True
        mode_play = False
        instructions.configure(text="Solving...", fg="grey")
        print('Original Puzzle: ')
        printPuzzle(puzzle)

        tic = time.perf_counter()
        autoSolver(puzzle)
        toc = time.perf_counter()
    
        print('Solution: ')
        printPuzzle(puzzle)

        for i in range(9):
            for j in range(9):
                if puzzle_original[i][j] != 1:
                    entries[(i, j)].configure(fg="green")
                    entries[(i, j)].insert(0, str(puzzle[i][j]))

        instructions.configure(text=f"Solved in {(toc-tic)*1000:04f}ms. Press Clear to reset", fg="purple")
        mode_solve = False

def buttonPressPlay():
    global mode_setup, mode_solve, mode_play

    if not isSolvedBoard(puzzle):
        if not updateEntries(): return
        
        mode_setup = False
        mode_solve = False
        mode_play = True
        setOriginalPuzzle()
        instructions.configure(text="Press Check to test answers or Clear to reset", fg="grey")
        play_button.configure(text="Check", command=buttonPressCheck)

def buttonPressCheck():
    global selected_entry_x, selected_entry_y
    solved_board = True
    selected_entry_x = -1
    selected_entry_y = -1
    possible_errs = []

    for i in range(9):
        for j in range(9):
            entries[(i, j)].configure(bg="white")
            if puzzle_original[i][j] == 1:
                entries[(i, j)].configure(fg="black")
                entries[(i, j)].delete(0,tk.END)
                entries[(i, j)].insert(0, str(puzzle[i][j]))
            else:
                entries[(i, j)].configure(fg="blue")

                if entries[(i, j)].get() == "" or entries[(i, j)].get() == "0" or not entries[(i, j)].get().isnumeric():
                    entries[(i, j)].delete(0,tk.END)
                    puzzle[i][j] = 0
                else:
                    puzzle[i][j] = int(entries[(i, j)].get())

                if puzzle[i][j] == 0:
                    entries[(i, j)].configure(fg="red", bg="#FFB1A0")
                    instructions.configure(text="This puzzle is not solved", fg="red")
                    solved_board = False
                elif not isValid(puzzle, puzzle[i][j], i, j):
                    possible_errs.append( ((i, j), entries[(i, j)]) )
    
    if identifyErrors(possible_errs):
        instructions.configure(text="This puzzle is not solved", fg="red")
        solved_board = False

    printPuzzle(puzzle)

    if solved_board:
        instructions.configure(text="This puzzle is solved! Press Clear to reset", fg="green")
        play_button.configure(text="Play", command=buttonPressPlay)

ButtonFrame = tk.Frame(bg="white")
ButtonFrame.pack(fill=tk.BOTH, expand=True)

play_button = tk.Button(master=ButtonFrame, text="Play", command=buttonPressPlay)
play_button.grid(row=0, column=0, padx=5, pady=5)

solve_button = tk.Button(master=ButtonFrame, text="Auto-Solve", command=buttonPressSolve)
solve_button.grid(row=0, column=1, padx=5, pady=5)

clear_button = tk.Button(master=ButtonFrame, text="Clear", command=buttonPressClear)
clear_button.grid(row=0, column=2, padx=5, pady=5)

window.mainloop()