import random
import js

GRID_SIZE = 9
BOX_SIZE = 3
CELL_SIZE = 43
EMPTY = 0

game = {
    "board": [],
    "original": [],
    "hint": [],
    "answer": [],
    "selected": None,
    "completed": False
}

#
# utils.py
#
def q(query):
    return js.document.querySelector(query)

def q_text(query, text):
    q(query).innerText = text
    
def set_timeout(f, ms):
    return js.setTimeout(f, ms)

#
# main.py
#

def game_start():
    global game
    
    board, answer_board = get_puzzle_data()
    
    game = {
        "selected": None,
        "completed": False,
        "board": board,
        "original": [row[:] for row in board],
        "hint": [[0] * GRID_SIZE for _ in range(GRID_SIZE)],
        "answer": answer_board
    }
    
    q_text("#title", "ナンバープレース")
    draw_board()
    
def get_puzzle_data():
    
    board = [
        [0, 0, 5, 0, 3, 0, 6, 0, 0],
        [8, 0, 0, 4, 0, 0, 3, 0, 0],
        [4, 0, 0, 0, 0, 9, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 6],
        [0, 0, 0, 1, 0, 0, 0, 8, 0],
        [7, 0, 0, 0, 0, 8, 0, 0, 0],
        [3, 0, 0, 5, 0, 0, 8, 0, 0],
        [2, 0, 1, 0, 7, 3, 0, 0, 0],
        [0, 9, 0, 0, 1, 2, 0, 0, 0]
    ]

    answer = [
        [9, 7, 5, 2, 3, 1, 6, 4, 8],
        [8, 1, 2, 4, 5, 6, 3, 9, 7],
        [4, 3, 6, 7, 8, 9, 1, 2, 5],
        [1, 8, 4, 3, 2, 5, 9, 7, 6],
        [6, 5, 9, 1, 4, 7, 2, 8, 3],
        [7, 2, 3, 9, 6, 8, 4, 5, 1],
        [3, 6, 7, 5, 9, 4, 8, 1, 2],
        [2, 4, 1, 8, 7, 3, 5, 6, 9],
        [5, 9, 8, 6, 1, 2, 7, 3, 4]
    ]
    
    gboard = generate_puzzle()
    if gboard is None:
        return board, answer
    ganswer = get_answer()
    
    return gboard, ganswer

def can_place_number(board, row, col, num):
    
    for c in range(GRID_SIZE):
        if board[row][c] == num:
            return False
        
    for r in range(GRID_SIZE):
        if board[r][col] == num:
            return False
        
    box_row = (row // BOX_SIZE) * BOX_SIZE
    box_col = (col // BOX_SIZE) * BOX_SIZE
    for r in range(box_row, box_row + BOX_SIZE):
        for c in range(box_col, box_col + BOX_SIZE):
            if board[r][c] == num:
                return False
    return True

def place_number(row, col, num):
    if game["completed"]:
        return
    if game["original"][row][col] != 0:
        return
    if can_place_number(game["board"], row, col, num):
        game["board"][row][col] = num
        if check_completion():
            game["completed"] = True
            q_text("#title", "おめでとう★ ナンバープレース完成！")
        else:
            q_text("#title", "ナンバープレース")
    else:
        q_text("#title", "その数字は置けません")
        set_timeout(lambda: q_text("#title", "ナンバープレース"), 1000)
        
def check_completion():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if game["board"][row][col] == 0:
                return False
    return True

#
# draw.py
#

canvas = q("#canvas")
context = canvas.getContext("2d")

def draw_board():
    draw_background()
    draw_grid()
    draw_numbers()

def draw_background():
    context.clearRect(0, 0, canvas.width, canvas.height)
    context.fillStyle = "#ffffff"
    context.fillRect(0, 0, canvas.width, canvas.height)
    if not game["selected"]:
        return
    
    sel_c = game["selected"][0]
    sel_r = game["selected"][1]
    xx = sel_r * CELL_SIZE
    yy = sel_c * CELL_SIZE
    context.fillStyle = "rgba(230, 230, 80, 0.1)"
    for row in range(GRID_SIZE):
        y = row * CELL_SIZE
        context.fillRect(xx, y, CELL_SIZE, CELL_SIZE)
    for col in range(GRID_SIZE):
        x = col * CELL_SIZE
        context.fillRect(x, yy, CELL_SIZE, CELL_SIZE)    
        
    context.fillStyle = "rgba(255, 255, 0, 0.5)"
    context.fillRect(xx, yy, CELL_SIZE, CELL_SIZE)
    
def draw_line(x1, y1, x2, y2, width=1, color="black"):
    context.strokeStyle = color
    context.lineWidth = width
    context.beginPath()
    context.moveTo(x1, y1)
    context.lineTo(x2, y2)
    context.stroke()
    
def draw_grid():
    for i in range(GRID_SIZE + 1):
        x = i * CELL_SIZE
        y = i * CELL_SIZE
        draw_line(x, 0, x, GRID_SIZE * CELL_SIZE, 1)
        draw_line(0, y, GRID_SIZE * CELL_SIZE, y, 1)
    for i in range(0, GRID_SIZE + 1, BOX_SIZE):
        x = i * CELL_SIZE
        y = i * CELL_SIZE
        draw_line(x, 0, x, GRID_SIZE * CELL_SIZE, 3)
        draw_line(0, y, GRID_SIZE * CELL_SIZE, y, 3)
        
def draw_numbers():
    context.textAlign = "center"
    context.textBaseline = "middle"
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = game["board"][row][col]
            if num == 0:
                continue
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            if game["original"][row][col] != 0:
                context.fillStyle = "#000000"
                context.font = "bold 20px Arial"
            elif game["hint"][row][col] != 0:
                context.fillStyle = "#FF3366"
                context.font = "bold 20px Arial"
            else:
                context.fillStyle = "#0066cc"
                context.font = "18px Arial"
            context.fillText(str(num), x, y)

#
# click.py
#

def canvas_on_click(event):
    if game["completed"]:
        return
    rect = canvas.getBoundingClientRect()
    x = int(event.clientX - rect.left)
    y = int(event.clientY - rect.top)
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    if row >= GRID_SIZE or col >= GRID_SIZE:
        return
    game["selected"] = (row, col)
    draw_board()
    
def num_button_on_click(num):
    if game["selected"] is None:
        q_text("#title", "先にセルを選択してください")
        set_timeout(lambda: q_text("#title", "ナンバープレース"), 1000)
        return
    row, col = game["selected"]
    place_number(row, col, num)
    draw_board()
    
def eraser_button_click(event):
    if game["selected"] is None:
        return
    row, col = game["selected"]
    if game["original"][row][col] != 0:
        return
    game["board"][row][col] = 0
    draw_board()

def answer_button_click(event):
    game["board"] = game["answer"]
    draw_board()
    
def hint_button_click(event):
    if game["selected"] is None:
        q_text("#title", "先にセルを選択してください")
        set_timeout(lambda: q_text("#title", "ナンバープレース"), 1000)
        return
    row, col = game["selected"]
    if game["original"][row][col] != EMPTY:
        return
    game["board"][row][col] = game["answer"][row][col]
    game["hint"][row][col] = game["answer"][row][col]
    draw_board()
    
def new_button_click(event):
    game_start()
    
canvas.addEventListener("click", canvas_on_click)
q("#eraser").addEventListener("click", eraser_button_click)
q("#hint").addEventListener("click", hint_button_click)
q("#answer").addEventListener("click", answer_button_click)
q("#new").addEventListener("click", new_button_click)
for i in range(1, 10):
    btn = q(f"#num{i}")
    btn.addEventListener("click", lambda e: num_button_on_click(int(e.target.textContent)))
        
#
# ui.py
#

def handle_key(event):
    key_handlers = {
        "1": num_button_on_click,
        "2": num_button_on_click,
        "3": num_button_on_click,
        "4": num_button_on_click,
        "5": num_button_on_click,
        "6": num_button_on_click,
        "7": num_button_on_click,
        "8": num_button_on_click,
        "9": num_button_on_click,
        "Backspace": eraser_button_click
    }
    
    if event.key in key_handlers:
        event.preventDefault()
        if event.key == "Backspace":
            key_handlers[event.key](event)
        else:
            key_handlers[event.key](int(event.key))
        
js.document.addEventListener("keydown", handle_key)    

#
# generate_puzzle.py
#
import copy

complete_flag = False
puzzle_board = []
answer_board = []

def generate_puzzle():
    global answer_board, puzzle_board, complete_flag
    
    answer_board = []
    puzzle_board = []
    complete_flag = False
    
    gboard = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    
    solve(gboard)
    
    if complete_flag:
        answer_board = copy.deepcopy(puzzle_board)
        blank_manyplace(puzzle_board)
        return puzzle_board
    
    return None

def get_answer():
    return answer_board
    
def blank_manyplace(board):
    show_count = random.choice([35, 36, 37, 38])
    
    selected = sample([n for n in range(GRID_SIZE * GRID_SIZE)], show_count)
    
    for i in range(GRID_SIZE * GRID_SIZE):
        if i in selected:
            continue
        r = i // GRID_SIZE
        c = i % GRID_SIZE
        board[r][c] = 0

def solve(board):
    original = copy.deepcopy(board)
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if complete_flag:
                break
            board = copy.deepcopy(original)
            if board[row][col] == 0:
                candidate = get_candidate(board, row, col)
                shuffle(candidate)
                for num in candidate:
                    search(board, row, col, num)
    
def search(board, row, col, num):
    global puzzle_board, complete_flag
    
    if not can_place_number(board, row, col, num):
       return 
       
    board[row][col] = num
       
    if check_generation_completion(board):
        puzzle_board = board
        complete_flag = True
        return
    
    result = get_best_candidate(board)
    if result is None:
        board[row][col] = 0
        return
    
    r, c, candidate = result
    
    shuffle(candidate)
  
    for num in candidate:
        search(board, r, c, num)
        if complete_flag:
            return
        continue
    
def get_candidate(board, row, col):
    
    candidate = []
    for num in range(1, 10):
        if can_place_number(board, row, col, num):
            candidate.append(num)
            
    return candidate

def get_best_candidate(board):
    
    candidate_dic = {}      
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                candidate = get_candidate(board, r, c)
                if len(candidate) > 0:
                    candidate_dic[f"{r}{c}"] = len(candidate)
            else:
                continue
    
    if not candidate_dic:
        return None
    
    min_value = min(candidate_dic.values())
    
    for key, value in candidate_dic.items():
        if value == min_value:
            r, c = int(key[0]), int(key[1])
            candidate = get_candidate(board, r, c)
            return (r, c, candidate)
        
    return None

def check_generation_completion(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                return False
    return True

def shuffle(l):
    for i in range(len(l) - 1, 0, -1):
        j = random.randrange(i + 1)
        l[i], l[j] = l[j], l[i]
        
def sample(l, k):
    temp = list(l)
    shuffle(temp)
    return temp[:k]
