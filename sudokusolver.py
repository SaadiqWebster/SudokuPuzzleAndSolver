
def isValid(puzzle, val, cor_x, cor_y):
    if val != 0:
        if val < 0 or val > 9: return False
        
        for i in range(9):
            if puzzle[cor_x][i] == val and i != cor_y:
                return False

        for i in range(9):
            if puzzle[i][cor_y] == val and i != cor_x:
                return False

        box_x = cor_x // 3
        box_y = cor_y // 3
        for i in range(box_x*3, (box_x*3)+3):
            for j in range(box_y*3, (box_y*3)+3):
                if puzzle[i][j] == val and i != cor_x and j != cor_y:
                    return False

    return True

def isSolvedBoard(puzzle):
    for i in range(9):
        for j in range(9):
            if not isValid(puzzle, puzzle[i][j], i, j) or puzzle[i][j] == 0:
                return False
    
    return True

def autoSolver(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                for x in range(1,10):
                    if isValid(puzzle, x, i, j):
                        puzzle[i][j] = x
                        
                        if autoSolver(puzzle):
                            return True

                        puzzle[i][j] = 0
                return False
    return True


def printPuzzle(puzzle):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print('| ----- + ----- + ----- |')

        print('|', end=' ')

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print('|', end=' ')

            if puzzle[i][j] == 0:
                print('*', end=' ')
            else:
                print(puzzle[i][j], end=' ')

        print('|')
    print()
