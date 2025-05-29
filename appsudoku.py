from flask import Flask, render_template, request, redirect, url_for, session
import random
import copy
import time

app = Flask(__name__)
app.secret_key = "sudoku_secret_key"


MAX_ALT_SOLUTIONS = 10        # quantas soluções alternativas guardar




def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    for i in range(sr, sr + 3):
        for j in range(sc, sc + 3):
            if board[i][j] == num:
                return False
    return True


def enumerate_solutions(board, max_solutions=MAX_ALT_SOLUTIONS):
    """Coleta até max_solutions soluções diferentes."""
    solutions, attempts = [], 0
    start_ns = time.perf_counter_ns()

    def backtrack(idx=0):
        nonlocal attempts
        if len(solutions) >= max_solutions:
            return
        if idx == 81:
            solutions.append(copy.deepcopy(board))
            return
        r, c = divmod(idx, 9)
        if board[r][c] != 0:
            backtrack(idx + 1)
            return
        for num in range(1, 10):
            if is_valid(board, r, c, num):
                board[r][c] = num
                attempts += 1
                backtrack(idx + 1)
                board[r][c] = 0

    backtrack()
    elapsed_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
    return solutions, attempts, elapsed_ms



def solve(board):                              
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve(board):
                            return True
                        board[i][j] = 0
                return False
    return True


def fill_board(board):                         
    nums = list(range(1, 10))
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve(copy.deepcopy(board)) and fill_board(board):
                            return True
                        board[i][j] = 0
                return False
    return True


def remove_numbers(board, n):                  
    removed = 0
    while removed < n:
        r, c = random.randint(0, 8), random.randint(0, 8)
        if board[r][c] != 0:
            board[r][c] = 0
            removed += 1



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/manual')
def manual():
    session.setdefault('manual_board', [[0]*9 for _ in range(9)])
    return render_template('manual.html', board=session['manual_board'])


@app.route('/add_number', methods=['POST'])
def add_number():
    row, col = int(request.form['row'])-1, int(request.form['col'])-1
    val = int(request.form['value'])
    board = session.setdefault('manual_board', [[0]*9 for _ in range(9)])

    if 0 <= row < 9 and 0 <= col < 9 and 1 <= val <= 9:
        if is_valid(board, row, col, val):
            board[row][col] = val
            session['manual_board'] = board
        else:
            return render_template('manual.html', board=board,
                                   error="Número inválido nessa posição")
    return redirect(url_for('manual'))


@app.route('/solve_manual')
def solve_manual():
    board = copy.deepcopy(session.get(
        'manual_board', [[0]*9 for _ in range(9)]))
    sols, att, t_ms = enumerate_solutions(board, MAX_ALT_SOLUTIONS)

    if sols:
        session.update({
            "solutions":      sols,
            "solution_idx":   0,
            "board_snapshot": board,
            "attempts":       att,
            "runtime_ms":     f"{t_ms:.2f}"
        })
        return render_template('sudoku.html',
                               board=board,
                               solved=sols[0],
                               show_solution=True,
                               difficulty=None,
                               attempts=att,
                               runtime_ms=f"{t_ms:.2f}",
                               alt_solutions=len(sols),
                               solution_idx=0)
    return render_template('manual.html', board=board,
                           error="Esse Sudoku não tem solução",
                           attempts=att,
                           runtime_ms=f"{t_ms:.2f}")


@app.route('/generate', methods=['POST'])

@app.route('/generate', methods=['POST'])
def generate():
    
    diff = (request.form.get('difficulty') or session.get('difficulty') or 'medium').lower().strip()

    blanks_mapping = {
        'easy': 35,
        'medium': 45,
        'hard': 55,
        'veryhard': 60
    }
    blanks = blanks_mapping.get(diff, 45)
    diff_label = diff


    board = [[0]*9 for _ in range(9)]
    fill_board(board)
    solved_ref = copy.deepcopy(board)
    remove_numbers(board, blanks)

    session.clear()
    session.update({
        "generated":        board,
        "solved_reference": solved_ref,
        "difficulty":       diff_label
    })

    return render_template('sudoku.html',
                           board=board,
                           solved=solved_ref,
                           show_solution=False,
                           difficulty=diff_label,
                           attempts=None,
                           runtime_ms=None,
                           alt_solutions=0,
                           solution_idx=0)



@app.route('/solve', methods=['POST'])
def solve_from_input():
    base = session.get('generated') or session.get('manual_board') \
        or [[0]*9 for _ in range(9)]

    user_board = [[int(request.form.get(f'cell-{i}-{j}', '') or base[i][j])
                   for j in range(9)] for i in range(9)]

    sols, att, t_ms = enumerate_solutions(user_board, MAX_ALT_SOLUTIONS)
    if sols:
        session.update({
            "solutions":      sols,
            "solution_idx":   0,
            "board_snapshot": user_board,
            "attempts":       att,
            "runtime_ms":     f"{t_ms:.2f}"
        })
        return render_template('sudoku.html',
                               board=user_board,
                               solved=sols[0],
                               show_solution=True,
                               difficulty=session.get('difficulty'),
                               attempts=att,
                               runtime_ms=f"{t_ms:.2f}",
                               alt_solutions=len(sols),
                               solution_idx=0)

    return render_template('sudoku.html',
                           board=user_board,
                           solved=None,
                           show_solution=False,
                           difficulty=session.get('difficulty'),
                           error="Este Sudoku não tem solução.",
                           attempts=att,
                           runtime_ms=f"{t_ms:.2f}",
                           alt_solutions=0,
                           solution_idx=0)


@app.route('/next_solution')
def next_solution():
    sols = session.get('solutions')
    if not sols:
        return redirect(url_for('index'))

    idx = (session.get('solution_idx', 0) + 1) % len(sols)
    session['solution_idx'] = idx
    board_snapshot = session.get('board_snapshot',
                                 session.get('generated') or session.get('manual_board'))

    return render_template('sudoku.html',
                           board=board_snapshot,
                           solved=sols[idx],
                           show_solution=True,
                           difficulty=session.get('difficulty'),
                           attempts=session.get('attempts'),
                           runtime_ms=session.get('runtime_ms'),
                           alt_solutions=len(sols),
                           solution_idx=idx)


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
