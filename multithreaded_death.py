from Queue import Queue
from threading import Thread
import random
import copy
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameStateRequest(BaseModel):
    board: list # [[0..2][0..2]0..3]
    turn: str # WHITE, BLACK

class GameState():
    board: list # [[0..2][0..2]0..3]
    turn: str # WHITE, BLACK
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

class Move():
    player: str # WHITE, BLACK
    stone_quadrant: int # 0..3
    row: int # 0..2
    col: int # 0..2
    rot_quadrant: int # 0..3
    direction: str # CLOCKWISE, ANTICLOCKWISE
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)


def do_stuff(q):
  while True:
    print(q.get())
    q.task_done()

@app.post("/state")
async def root(state: GameStateRequest):
    state = state.dict()
    depth = 3
    
    # state['turn'] = 'BLACK' if state['turn'] == 'WHITE' else 'WHITE' # switch player for next turn
    #state["board"][2][0][1] = 'WHITE' if state['turn'] == 'WHITE' else 'BLACK'

    move = Move() # @todo Useless ?
    move, eval = best_move(state, depth, self_called=False) # PARAMETRE DU LEVEL DE L'I3
    print("My move is worth: " + str(eval))
    print("---------------------------")
    print("I land my " + move["player"] + " stone in quadrant " + str(move["stone_quadrant"]) + ", row " + str(move["row"]) + ", col " + str(move["col"]))
    print("Then I rotate quadrant " + str(move["rot_quadrant"]) + " " + move["direction"])

    next_state = GameState()
    next_state["turn"] = 'WHITE' if state["turn"] == 'BLACK' else 'BLACK'
    next_state["board"] = state["board"]
    next_state["board"][move["stone_quadrant"]][move["row"]][move["col"]] = move["player"]
    next_state["board"] = rotate(next_state["board"], move["rot_quadrant"], move["direction"])

    if evaluate(state["board"]) == 100:
        next_state['winner'] = 'WHITE'
    if evaluate(state["board"]) == -100:
        next_state['winner'] = 'BLACK'
    return next_state

def rotate(board: list, quadrant: int, direction: str): # renvoie le board avec un quart de tour sur le quadrant dans la direction
    if direction == 'CLOCKWISE':
        board[quadrant] = [
            [board[quadrant][2][0], board[quadrant][1][0], board[quadrant][0][0]],
            [board[quadrant][2][1], board[quadrant][1][1], board[quadrant][0][1]],
            [board[quadrant][2][2], board[quadrant][1][2], board[quadrant][0][2]]
        ]
    else:
        board[quadrant] = [
            [board[quadrant][0][2], board[quadrant][1][2], board[quadrant][2][2]],
            [board[quadrant][0][1], board[quadrant][1][1], board[quadrant][2][1]],
            [board[quadrant][0][0], board[quadrant][1][0], board[quadrant][2][0]]
        ]
    return board

def evaluate(board: list): # renvoie l'évaluation de la position du board (100 si blanc gagne, -100 si noir gagne, sinon 0 => A AMELIORER POUR LEVEL UP L'IA)
    # si white aligne 5 billes horizontales
    if board[0][0][0] == 'WHITE' and board[0][0][1] == 'WHITE' and board[0][0][2] == 'WHITE' and board[1][0][0] == 'WHITE' and board[1][0][1] == 'WHITE': return 100
    if board[0][0][1] == 'WHITE' and board[0][0][2] == 'WHITE' and board[1][0][0] == 'WHITE' and board[1][0][1] == 'WHITE' and board[1][0][2] == 'WHITE': return 100
    if board[0][1][0] == 'WHITE' and board[0][1][1] == 'WHITE' and board[0][1][2] == 'WHITE' and board[1][1][0] == 'WHITE' and board[1][1][1] == 'WHITE': return 100
    if board[0][1][1] == 'WHITE' and board[0][1][2] == 'WHITE' and board[1][1][0] == 'WHITE' and board[1][1][1] == 'WHITE' and board[1][1][2] == 'WHITE': return 100
    if board[0][2][0] == 'WHITE' and board[0][2][1] == 'WHITE' and board[0][2][2] == 'WHITE' and board[1][2][0] == 'WHITE' and board[1][2][1] == 'WHITE': return 100
    if board[0][2][1] == 'WHITE' and board[0][2][2] == 'WHITE' and board[1][2][0] == 'WHITE' and board[1][2][1] == 'WHITE' and board[1][2][2] == 'WHITE': return 100
    if board[2][0][0] == 'WHITE' and board[2][0][1] == 'WHITE' and board[2][0][2] == 'WHITE' and board[3][0][0] == 'WHITE' and board[3][0][1] == 'WHITE': return 100
    if board[2][0][1] == 'WHITE' and board[2][0][2] == 'WHITE' and board[3][0][0] == 'WHITE' and board[3][0][1] == 'WHITE' and board[3][0][2] == 'WHITE': return 100
    if board[2][1][0] == 'WHITE' and board[2][1][1] == 'WHITE' and board[2][1][2] == 'WHITE' and board[3][1][0] == 'WHITE' and board[3][1][1] == 'WHITE': return 100
    if board[2][1][1] == 'WHITE' and board[2][1][2] == 'WHITE' and board[3][1][0] == 'WHITE' and board[3][1][1] == 'WHITE' and board[3][1][2] == 'WHITE': return 100
    if board[2][2][0] == 'WHITE' and board[2][2][1] == 'WHITE' and board[2][2][2] == 'WHITE' and board[3][2][0] == 'WHITE' and board[3][2][1] == 'WHITE': return 100
    if board[2][2][1] == 'WHITE' and board[2][2][2] == 'WHITE' and board[3][2][0] == 'WHITE' and board[3][2][1] == 'WHITE' and board[3][2][2] == 'WHITE': return 100
    # si black aligne 5 billes horizontales
    if board[0][0][0] == 'BLACK' and board[0][0][1] == 'BLACK' and board[0][0][2] == 'BLACK' and board[1][0][0] == 'BLACK' and board[1][0][1] == 'BLACK': return -100
    if board[0][0][1] == 'BLACK' and board[0][0][2] == 'BLACK' and board[1][0][0] == 'BLACK' and board[1][0][1] == 'BLACK' and board[1][0][2] == 'BLACK': return -100
    if board[0][1][0] == 'BLACK' and board[0][1][1] == 'BLACK' and board[0][1][2] == 'BLACK' and board[1][1][0] == 'BLACK' and board[1][1][1] == 'BLACK': return -100
    if board[0][1][1] == 'BLACK' and board[0][1][2] == 'BLACK' and board[1][1][0] == 'BLACK' and board[1][1][1] == 'BLACK' and board[1][1][2] == 'BLACK': return -100
    if board[0][2][0] == 'BLACK' and board[0][2][1] == 'BLACK' and board[0][2][2] == 'BLACK' and board[1][2][0] == 'BLACK' and board[1][2][1] == 'BLACK': return -100
    if board[0][2][1] == 'BLACK' and board[0][2][2] == 'BLACK' and board[1][2][0] == 'BLACK' and board[1][2][1] == 'BLACK' and board[1][2][2] == 'BLACK': return -100
    if board[2][0][0] == 'BLACK' and board[2][0][1] == 'BLACK' and board[2][0][2] == 'BLACK' and board[3][0][0] == 'BLACK' and board[3][0][1] == 'BLACK': return -100
    if board[2][0][1] == 'BLACK' and board[2][0][2] == 'BLACK' and board[3][0][0] == 'BLACK' and board[3][0][1] == 'BLACK' and board[3][0][2] == 'BLACK': return -100
    if board[2][1][0] == 'BLACK' and board[2][1][1] == 'BLACK' and board[2][1][2] == 'BLACK' and board[3][1][0] == 'BLACK' and board[3][1][1] == 'BLACK': return -100
    if board[2][1][1] == 'BLACK' and board[2][1][2] == 'BLACK' and board[3][1][0] == 'BLACK' and board[3][1][1] == 'BLACK' and board[3][1][2] == 'BLACK': return -100
    if board[2][2][0] == 'BLACK' and board[2][2][1] == 'BLACK' and board[2][2][2] == 'BLACK' and board[3][2][0] == 'BLACK' and board[3][2][1] == 'BLACK': return -100
    if board[2][2][1] == 'BLACK' and board[2][2][2] == 'BLACK' and board[3][2][0] == 'BLACK' and board[3][2][1] == 'BLACK' and board[3][2][2] == 'BLACK': return -100
    # si white aligne 5 billes verticales
    if board[0][0][0] == 'WHITE' and board[0][1][0] == 'WHITE' and board[0][2][0] == 'WHITE' and board[2][0][0] == 'WHITE' and board[2][1][0] == 'WHITE': return 100
    if board[0][1][0] == 'WHITE' and board[0][2][0] == 'WHITE' and board[2][0][0] == 'WHITE' and board[2][1][0] == 'WHITE' and board[2][2][0] == 'WHITE': return 100
    if board[0][0][1] == 'WHITE' and board[0][1][1] == 'WHITE' and board[0][2][1] == 'WHITE' and board[2][0][1] == 'WHITE' and board[2][1][1] == 'WHITE': return 100
    if board[0][1][1] == 'WHITE' and board[0][2][1] == 'WHITE' and board[2][0][1] == 'WHITE' and board[2][1][1] == 'WHITE' and board[2][2][1] == 'WHITE': return 100
    if board[0][1][2] == 'WHITE' and board[0][2][2] == 'WHITE' and board[2][0][2] == 'WHITE' and board[2][1][2] == 'WHITE' and board[2][2][2] == 'WHITE': return 100
    if board[0][0][2] == 'WHITE' and board[0][1][2] == 'WHITE' and board[0][2][2] == 'WHITE' and board[2][0][2] == 'WHITE' and board[2][1][2] == 'WHITE': return 100
    if board[1][0][0] == 'WHITE' and board[1][1][0] == 'WHITE' and board[1][2][0] == 'WHITE' and board[3][0][0] == 'WHITE' and board[3][1][0] == 'WHITE': return 100
    if board[1][1][0] == 'WHITE' and board[1][2][0] == 'WHITE' and board[3][0][0] == 'WHITE' and board[3][1][0] == 'WHITE' and board[3][2][0] == 'WHITE': return 100
    if board[1][0][1] == 'WHITE' and board[1][1][1] == 'WHITE' and board[1][2][1] == 'WHITE' and board[1][0][1] == 'WHITE' and board[1][1][1] == 'WHITE': return 100
    if board[1][1][1] == 'WHITE' and board[1][2][1] == 'WHITE' and board[3][0][1] == 'WHITE' and board[3][1][1] == 'WHITE' and board[3][2][1] == 'WHITE': return 100
    if board[1][0][2] == 'WHITE' and board[1][1][2] == 'WHITE' and board[2][2][2] == 'WHITE' and board[3][0][2] == 'WHITE' and board[3][1][2] == 'WHITE': return 100
    if board[1][1][2] == 'WHITE' and board[1][2][2] == 'WHITE' and board[3][0][2] == 'WHITE' and board[3][1][2] == 'WHITE' and board[3][2][2] == 'WHITE': return 100
    # si black aligne 5 billes verticales
    if board[0][0][0] == 'BLACK' and board[0][1][0] == 'BLACK' and board[0][2][0] == 'BLACK' and board[2][0][0] == 'BLACK' and board[2][1][0] == 'BLACK': return -100
    if board[0][1][0] == 'BLACK' and board[0][2][0] == 'BLACK' and board[2][0][0] == 'BLACK' and board[2][1][0] == 'BLACK' and board[2][2][0] == 'BLACK': return -100
    if board[0][0][1] == 'BLACK' and board[0][1][1] == 'BLACK' and board[0][2][1] == 'BLACK' and board[2][0][1] == 'BLACK' and board[2][1][1] == 'BLACK': return -100
    if board[0][1][1] == 'BLACK' and board[0][2][1] == 'BLACK' and board[2][0][1] == 'BLACK' and board[2][1][1] == 'BLACK' and board[2][2][1] == 'BLACK': return -100
    if board[0][1][2] == 'BLACK' and board[0][2][2] == 'BLACK' and board[2][0][2] == 'BLACK' and board[2][1][2] == 'BLACK' and board[2][2][2] == 'BLACK': return -100
    if board[0][0][2] == 'BLACK' and board[0][1][2] == 'BLACK' and board[0][2][2] == 'BLACK' and board[2][0][2] == 'BLACK' and board[2][1][2] == 'BLACK': return -100
    if board[1][0][0] == 'BLACK' and board[1][1][0] == 'BLACK' and board[1][2][0] == 'BLACK' and board[3][0][0] == 'BLACK' and board[3][1][0] == 'BLACK': return -100
    if board[1][1][0] == 'BLACK' and board[1][2][0] == 'BLACK' and board[3][0][0] == 'BLACK' and board[3][1][0] == 'BLACK' and board[3][2][0] == 'BLACK': return -100
    if board[1][0][1] == 'BLACK' and board[1][1][1] == 'BLACK' and board[1][2][1] == 'BLACK' and board[1][0][1] == 'BLACK' and board[1][1][1] == 'BLACK': return -100
    if board[1][1][1] == 'BLACK' and board[1][2][1] == 'BLACK' and board[3][0][1] == 'BLACK' and board[3][1][1] == 'BLACK' and board[3][2][1] == 'BLACK': return -100
    if board[1][0][2] == 'BLACK' and board[1][1][2] == 'BLACK' and board[2][2][2] == 'BLACK' and board[3][0][2] == 'BLACK' and board[3][1][2] == 'BLACK': return -100
    if board[1][1][2] == 'BLACK' and board[1][2][2] == 'BLACK' and board[3][0][2] == 'BLACK' and board[3][1][2] == 'BLACK' and board[3][2][2] == 'BLACK': return -100
    # si white aligne 5 billes diagonales up
    if board[2][1][0] == 'WHITE' and board[2][0][1] == 'WHITE' and board[0][2][2] == 'WHITE' and board[1][1][0] == 'WHITE' and board[1][0][1] == 'WHITE': return 100
    if board[2][2][0] == 'WHITE' and board[2][1][1] == 'WHITE' and board[2][0][2] == 'WHITE' and board[1][2][0] == 'WHITE' and board[1][1][1] == 'WHITE': return 100
    if board[2][1][1] == 'WHITE' and board[2][0][2] == 'WHITE' and board[1][2][0] == 'WHITE' and board[1][1][1] == 'WHITE' and board[1][0][2] == 'WHITE': return 100
    if board[2][2][1] == 'WHITE' and board[2][1][2] == 'WHITE' and board[3][0][0] == 'WHITE' and board[1][2][1] == 'WHITE' and board[1][1][2] == 'WHITE': return 100
    # si black aligne 5 billes diagonales up
    if board[2][1][0] == 'BLACK' and board[2][0][1] == 'BLACK' and board[0][2][2] == 'BLACK' and board[1][1][0] == 'BLACK' and board[1][0][1] == 'BLACK': return -100
    if board[2][2][0] == 'BLACK' and board[2][1][1] == 'BLACK' and board[2][0][2] == 'BLACK' and board[1][2][0] == 'BLACK' and board[1][1][1] == 'BLACK': return -100
    if board[2][1][1] == 'BLACK' and board[2][0][2] == 'BLACK' and board[1][2][0] == 'BLACK' and board[1][1][1] == 'BLACK' and board[1][0][2] == 'BLACK': return -100
    if board[2][2][1] == 'BLACK' and board[2][1][2] == 'BLACK' and board[3][0][0] == 'BLACK' and board[1][2][1] == 'BLACK' and board[1][1][2] == 'BLACK': return -100
    # si white aligne 5 billes diagonales down
    if board[0][0][1] == 'WHITE' and board[0][1][2] == 'WHITE' and board[1][2][0] == 'WHITE' and board[3][0][1] == 'WHITE' and board[3][1][2] == 'WHITE': return 100
    if board[0][0][0] == 'WHITE' and board[0][1][1] == 'WHITE' and board[0][2][2] == 'WHITE' and board[3][0][0] == 'WHITE' and board[3][1][1] == 'WHITE': return 100
    if board[0][1][1] == 'WHITE' and board[0][2][2] == 'WHITE' and board[3][0][0] == 'WHITE' and board[3][1][1] == 'WHITE' and board[3][2][2] == 'WHITE': return 100
    if board[0][1][0] == 'WHITE' and board[0][2][1] == 'WHITE' and board[2][0][2] == 'WHITE' and board[3][1][0] == 'WHITE' and board[3][2][1] == 'WHITE': return 100
    # si black aligne 5 billes diagonales down
    if board[0][0][1] == 'BLACK' and board[0][1][2] == 'BLACK' and board[1][2][0] == 'BLACK' and board[3][0][1] == 'BLACK' and board[3][1][2] == 'BLACK': return -100
    if board[0][0][0] == 'BLACK' and board[0][1][1] == 'BLACK' and board[0][2][2] == 'BLACK' and board[3][0][0] == 'BLACK' and board[3][1][1] == 'BLACK': return -100
    if board[0][1][1] == 'BLACK' and board[0][2][2] == 'BLACK' and board[3][0][0] == 'BLACK' and board[3][1][1] == 'BLACK' and board[3][2][2] == 'BLACK': return -100
    if board[0][1][0] == 'BLACK' and board[0][2][1] == 'BLACK' and board[2][0][2] == 'BLACK' and board[3][1][0] == 'BLACK' and board[3][2][1] == 'BLACK': return -100
    return 0

def possible_moves(state: GameState): # renvoie la liste des moves possibles pour le player
    board = copy.copy(state["board"])
    moves = list()

    for stone_quadrant in range(4):
        for i in range(3):
            for j in range(3):
                if board[stone_quadrant][i][j] == 'EMPTY':
                    move = Move()
                    move["player"] = state["turn"]
                    move["stone_quadrant"] = stone_quadrant
                    move["row"] = i
                    move["col"] = j
                    for rot_quadrant in range(4):
                        move["rot_quadrant"] = rot_quadrant
                        move["direction"] = 'CLOCKWISE'
                        moves.append(move)
                        move["direction"] = 'ANTICLOCKWISE'
                        moves.append(move)
    return moves
    
def next_state_from_move(move, state): # renvoie le nouveau state à partir d'un move appliqué au state courant
    next_state = GameState()
    next_state["turn"] = 'WHITE' if state["turn"] == 'BLACK' else 'BLACK'
    next_state["board"] = copy.deepcopy(state["board"])
    next_state["board"][move["stone_quadrant"]][move["row"]][move["col"]] = move["player"]
    next_state["board"] = rotate(next_state["board"], move["rot_quadrant"], move["direction"])

    return next_state

def best_move(shared_state: GameState, depth: int, first_move = None, self_called = True): # renvoie le meilleur move si on explore les depth prochains coups, et son évaluation
    state = copy.deepcopy(shared_state)
    board = state["board"]

    if depth == 0 : # if we don't want to explore further
        # pick a random move among the possible moves
        moves = possible_moves(state)
        random_move = random.choice(moves)
        return random_move, evaluate(board)

    if state["turn"] == 'WHITE':
        maxEval = -100
        possible_next_moves = possible_moves(state)
        for k in range(len(possible_next_moves)):
            if not self_called:
                first_move = possible_next_moves[k]
            next_state = next_state_from_move(possible_next_moves[k], state)
            next_move, eval = best_move(next_state, depth - 1, first_move=first_move)
            if eval > maxEval or k == 0:
                maxEval = eval
                chosen_move = first_move
        return chosen_move, maxEval

    else:
        minEval = 100
        possible_next_moves = possible_moves(state)
        for k in range(len(possible_next_moves)):
            if not self_called:
                first_move = possible_next_moves[k]
            next_state = next_state_from_move(possible_next_moves[k], state)
            next_move, eval = best_move(next_state, depth - 1, first_move=first_move)
            if eval < minEval or k == 0:
                minEval = eval
                chosen_move = first_move
        return chosen_move, minEval