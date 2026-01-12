import turtle
import random
import copy
import time

CELL_SIZE = 50
OFFSET_X = -225
OFFSET_Y = 225
FONT_SIZE = 18

board = []
fixed_cells = set()
cursor_pos = [0, 0]
start_time = 0
elapsed_time = 0
is_paused = False
game_won = False

drawer = turtle.Turtle()
timer_drawer = turtle.Turtle()
pause_drawer = turtle.Turtle()

BASE_SOLVED_BOARD = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8], [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3], [4, 2, 6, 8, 5, 3, 7, 9, 1], [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4], [2, 8, 7, 4, 1, 9, 6, 3, 5], [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

def get_coords(r, c):
    return OFFSET_X + c * CELL_SIZE, OFFSET_Y - r * CELL_SIZE

def is_safe(row, col, num):
    if num == 0: return True
    for i in range(9):
        if (i != col and board[row][i] == num) or (i != row and board[i][col] == num):
            return False
    sr, sc = (row // 3) * 3, (col // 3) * 3
    for r in range(sr, sr + 3):
        for c in range(sc, sc + 3):
            if (r, c) != (row, col) and board[r][c] == num:
                return False
    return True

def generate_level(diff):
    new_board = copy.deepcopy(BASE_SOLVED_BOARD)
    nums = list(range(1, 10))
    random.shuffle(nums)
    mapping = {i+1: nums[i] for i in range(9)}
    for r in range(9):
        for c in range(9):
            new_board[r][c] = mapping[new_board[r][c]]
    keep = {1: 45, 2: 35, 3: 25}[diff]
    to_remove = 81 - keep
    while to_remove > 0:
        r, c = random.randint(0, 8), random.randint(0, 8)
        if new_board[r][c] != 0:
            new_board[r][c] = 0
            to_remove -= 1
    return new_board

def update_timer():
    global elapsed_time
    if not is_paused and not game_won:
        elapsed_time = int(time.time() - start_time)
        timer_drawer.clear()
        timer_drawer.penup()
        timer_drawer.goto(130, 260)
        timer_drawer.color("black")
        timer_drawer.write(f"Time: {elapsed_time // 60:02d}:{elapsed_time % 60:02d}", font=("Arial", 16, "bold"))
    turtle.Screen().ontimer(update_timer, 1000)

def toggle_pause():
    global is_paused, start_time
    if game_won: return
    is_paused = not is_paused
    if is_paused:
        pause_drawer.penup()
        pause_drawer.goto(OFFSET_X - 10, OFFSET_Y + 10)
        pause_drawer.color("black")
        pause_drawer.begin_fill()
        for _ in range(2):
            pause_drawer.forward(470)
            pause_drawer.right(90)
            pause_drawer.forward(470)
            pause_drawer.right(90)
        pause_drawer.end_fill()
        pause_drawer.goto(0, -20)
        pause_drawer.color("white")
        pause_drawer.write("PAUSED", align="center", font=("Arial", 30, "bold"))
    else:
        pause_drawer.clear()
        start_time = time.time() - elapsed_time
        draw_board()
    turtle.update()

def draw_board():
    if is_paused: return
    drawer.clear()
    cx, cy = get_coords(*cursor_pos)
    drawer.penup()
    drawer.goto(cx, cy)
    drawer.color("#FFFFA0")
    drawer.begin_fill()
    for _ in range(4):
        drawer.forward(CELL_SIZE); drawer.right(90)
    drawer.end_fill()
    for i in range(10):
        drawer.width(3 if i % 3 == 0 else 1)
        drawer.color("black" if i % 3 == 0 else "gray")
        drawer.penup()
        drawer.goto(OFFSET_X, OFFSET_Y - i * CELL_SIZE)
        drawer.pendown()
        drawer.goto(OFFSET_X + 9 * CELL_SIZE, OFFSET_Y - i * CELL_SIZE)
        drawer.penup()
        drawer.goto(OFFSET_X + i * CELL_SIZE, OFFSET_Y)
        drawer.pendown()
        drawer.goto(OFFSET_X + i * CELL_SIZE, OFFSET_Y - 9 * CELL_SIZE)
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val != 0:
                x, y = get_coords(r, c)
                drawer.penup()
                drawer.goto(x + CELL_SIZE/2, y - CELL_SIZE + 10)
                drawer.color("black" if (r, c) in fixed_cells else ("blue" if is_safe(r, c, val) else "red"))
                drawer.write(val, align="center", font=("Arial", FONT_SIZE, "bold"))
    turtle.update()

def move(dr, dc):
    if is_paused or game_won: return
    nr, nc = cursor_pos[0] + dr, cursor_pos[1] + dc
    if 0 <= nr < 9 and 0 <= nc < 9:
        cursor_pos[0], cursor_pos[1] = nr, nc
        draw_board()

def set_num(n):
    global game_won
    if is_paused or game_won: return
    r, c = cursor_pos
    if (r, c) not in fixed_cells:
        board[r][c] = n
        draw_board()
        if n != 0 and all(all(is_safe(r, c, board[r][c]) and board[r][c] != 0 for c in range(9)) for r in range(9)):
            game_won = True
            drawer.penup()
            drawer.goto(0, 0)
            drawer.color("green")
            drawer.write("VICTORY!", align="center", font=("Arial", 50, "bold"))

def main():
    global board, start_time
    screen = turtle.Screen()
    screen.setup(600, 700)
    screen.tracer(0)
    for t in [drawer, timer_drawer, pause_drawer]:
        t.hideturtle()
        t.speed(0)
    diff = turtle.numinput("Sudoku", "1-Easy, 2-Medium, 3-Hard", default=1, minval=1, maxval=3)
    if not diff: return
    board = generate_level(int(diff))
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0: fixed_cells.add((r, c))
    start_time = time.time()
    screen.listen()
    screen.onkey(lambda: move(-1, 0), "Up")
    screen.onkey(lambda: move(1, 0), "Down")
    screen.onkey(lambda: move(0, -1), "Left")
    screen.onkey(lambda: move(0, 1), "Right")
    screen.onkey(toggle_pause, "p")
    for i in range(10):
        screen.onkey(lambda x=i: set_num(x), str(i))
    pause_drawer.penup()
    pause_drawer.goto(-230, 260)
    pause_drawer.color("red")
    pause_drawer.write("Press 'P' to Pause/Play", font=("Arial", 12, "bold"))
    update_timer()
    draw_board()
    turtle.done()

if __name__ == "__main__":
    main()