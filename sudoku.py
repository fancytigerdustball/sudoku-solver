''' Sudoku solver '''

matrix = []
while True:
    try:
        row = input('> ')
        if len(row) != 9 or not row.isnumeric():
            raise EOFError
        matrix.append(list(row))
    except (KeyboardInterrupt, EOFError):
        pass

    if len(matrix) == 9:
        break

str1to9 = list(map(str, range(1, 10)))

class Areas:
    ''' Stores matrix data '''
    lines, rows, squares, zeros, matrix = [], [], [], [], []
    def __init__(self):
        ''' Areas() -> object '''

        for yi, y in enumerate(matrix):
            for xi, x in enumerate(y):
                if x == '0':
                    self.zeros.append((yi, xi))

    def reset(self):
        ''' Initialize matrix data '''
        self.lines, self.rows = [], []
        self.squares = []
        self.matrix = []

        # Lines
        for y in num_matrix:
            self.lines.append(y)

        # Rows
        for i in range(9):
            row = []
            for line in self.lines:
                for n, x in enumerate(line):
                    if n == i:
                        row.append(x)
            self.rows.append(row)

        # Squares
        for y in range(0, 9, 3):
            for x in range(0, 9, 3):
                self.squares.append((
                    num_matrix[y][x: x + 3] +
                    num_matrix[y + 1][x: x + 3] + 
                    num_matrix[y + 2][x: x + 3]))

def is_solved():
    ''' Returns if the sudoku is solved or not '''

    for l in (areas.lines, areas.rows, areas.squares):
        for i in l:
            if sorted(map(lambda x: x.value, i)) != str1to9:
                return False
    return True

def print_matrix():
    ''' Prints the 2D matrix '''

    for y in num_matrix:
        for x in y:
            print(' ', end='')
            if not int(x.value):
                print('?', end='')
            else:
                print(x.value, end='')
        print()

class Number:
    ''' Class for holding number value, coordinates, and possibilities '''

    def __init__(self, value: str, x: int, y: int):
        ''' Number(value: str, x: int, y: int) -> object '''

        self.value = value
        self.x, self.y = x, y

    def init_allowed(self):
        ''' Initialize which numbers a blank space could be '''

        if not int(self.value):
            self.possible = str1to9[:]

            # Go through lines
            for line in areas.lines:
                if self in line:
                    for i in line:
                        if int(i.value) and i.value in self.possible:
                            self.possible.remove(i.value)
                    break

            # Go through rows
            for row in areas.rows:
                if self in row:
                    for i in row:
                        if int(i.value) and i.value in self.possible:
                            self.possible.remove(i.value)
                    break

            # Go through squares
            for square in areas.squares:
                if self in square:
                    for i in square:
                        if int(i.value) and i.value in self.possible:
                            self.possible.remove(i.value)
                    break

areas = Areas()

num_matrix = matrix[:]
for yi, y in enumerate(matrix):
    for xi, x in enumerate(y):
        num_matrix[yi][xi] = Number(x, xi, yi)

for y in num_matrix:
    for x in y:
        x.init_allowed()

areas.reset()

for y in num_matrix:
    for x in y:
        x.init_allowed()

try:
    while True:

        # Solve by elimination
        for i in str1to9:

            for line in areas.lines:
                inside = []
                possibles = []
                for s in line:
                    if hasattr(s, 'possible'):
                        for poss in s.possible:
                            possibles.append(poss)
                    else:
                        inside.append(s.value)
                if possibles.count(i) == 1 and i not in inside:
                    for s in line:
                        if i in getattr(s, 'possible', []):
                            number = Number(i, s.x, s.y)
                            num_matrix[s.y][s.x] = number
                            for y in num_matrix:
                                for x in y:
                                    x.init_allowed()
                            areas.reset() 

            for row in areas.rows:
                inside = []
                possibles = []
                for s in row:
                    if hasattr(s, 'possible'):
                        for poss in s.possible:
                            possibles.append(poss)
                    else:
                        inside.append(s.value)
                if possibles.count(i) == 1 and i not in inside:
                    for s in row:
                        if i in getattr(s, 'possible', []):
                            number = Number(i, s.x, s.y)
                            num_matrix[s.y][s.x] = number
                            for y in num_matrix:
                                for x in y:
                                    x.init_allowed()
                            areas.reset()    

            for square in areas.squares:
                inside = []
                possibles = []
                for s in square:
                    if hasattr(s, 'possible'):
                        for poss in s.possible:
                            possibles.append(poss)
                    else:
                        inside.append(s.value)
                if possibles.count(i) == 1 and i not in inside:
                    for s in square:
                        if i in getattr(s, 'possible', []):
                            number = Number(i, s.x, s.y)
                            num_matrix[s.y][s.x] = number
                            for y in num_matrix:
                                for x in y:
                                    x.init_allowed()
                            areas.reset()    

        if is_solved():
            break
except KeyboardInterrupt:
    pass

print_matrix()

while True:
    pass
