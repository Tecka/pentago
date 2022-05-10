import sys
import math
import random
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

class State(BaseModel):
    board: list # [[0..2][0..2]0..3]
    turn: str # WHITE, BLACK

class Move(BaseModel):
    player: str # WHITE, BLACK
    stone_quadrant: int # 0..3
    row: int # 0..2
    col: int # 0..2
    rot_quadrant: int # 0..3
    direction: str # CLOCKWISE, ANTICLOCKWISE

@app.post("/state")
async def root(state: State):
    state = state.dict()
    move = Move()
    next_state = State()
    print(state)
    state['turn'] = 'BLACK' if state['turn'] == 'WHITE' else 'WHITE'
    
    #state["board"][2][0][1] = 'WHITE' if state['turn'] == 'WHITE' else 'BLACK'

    move, eval = best_move(state, 3) # PARAMETRE DU LEVEL DE L'IA
    print("My move is worth: " + str(eval))
    print("---------------------------")
    print("I land my " + move["player"] + " stone in quadrant " + str(move["stone_quadrant"]) + ", row " + str(move["row"]) + ", col " + str(move["col"]))
    print("Then I rotate quadrant " + str(move["rot_quadrant"]) + " " + move["direction"])

    next_state["turn"] = 'WHITE' if state["turn"] == 'BLACK' else 'BLACK'
    next_state["board"] = state["board"]
    next_state["board"][move["stone_quadrant"]][move["row"]][move["col"]] = move["player"]
    next_state["board"] = rotate(next_state["board"], move["rot_quadrant"], move["direction"])

    if evaluate(state["board"]) == 100:
        state['winner'] = 'WHITE'
    if evaluate(state["board"]) == -100:
        state['winner'] = 'BLACK'
    return next_state

def rotate(board: list, quadrant: int, direction: str): # renvoie le board avec un quart de tour sur le quadrant dans la direction
    if direction == 'CLOCKWISE':
        board[quadrant] = [
            [quadrant[2][0], quadrant[1][0], quadrant[0][0]],
            [quadrant[2][1], quadrant[1][1], quadrant[0][1]],
            [quadrant[2][2], quadrant[1][2], quadrant[0][2]]
            ]
    else:
        board[quadrant] = [
            [quadrant[0][2], quadrant[1][2], quadrant[2][2]],
            [quadrant[0][1], quadrant[1][1], quadrant[2][1]],
            [quadrant[0][0], quadrant[1][0], quadrant[2][0]],
            ]
    return board

def evaluate(board: list): # renvoie l'évaluation de la position du board (100 si blanc gagne, -100 si noir gagne, sinon 0 => A AMELIORER POUR LEVEL UP L'IA)
    # si white aligne 5 billes horizontales
    #print(board)
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

def possible_moves(state: State): # renvoie la liste des moves possibles pour le player
    board = state["board"]
    moves = list()

    for stone_quadrant in range(3):
        for i in range(2):
            for j in range(2):
                if board[stone_quadrant][i][j] == 'EMPTY':
                    move = Move()
                    move["player"] = state["turn"]
                    move["stone_quadrant"] = stone_quadrant
                    move["row"] = i
                    move["col"] = j
                    for rot_quadrant in range(3):
                        move["rot_quadrant"] = rot_quadrant
                        move["direction"] = 'CLOCKWISE'
                        moves.append(move)
                        move["direction"] = 'ANTICLOCKWISE'
                        moves.append(move)
    #print(moves)
    return moves
    
def possible_next_states(state: State): # renvoie la liste des states possibles à partir d'un state donné
    states = list()

    for move in possible_moves(state):
        next_state = State()
        next_state["turn"] = 'WHITE' if state["turn"] == 'BLACK' else 'BLACK'
        next_state["board"] = state["board"]
        next_state["board"][move["stone_quadrant"]][move["row"]][move["col"]] = move["player"]
        next_state["board"] = rotate(next_state["board"], move["rot_quadrant"], move["direction"])
        states.append(next_state)

    return states

def best_move(state: State, depth: int): # renvoie le meilleur move si on explore les depth prochains coups, et son évaluation
    board = state["board"]

    if depth == 0 : # if we don't want to explore further
        print("I explored as far as I was allowed to.")
        # pick a random move among the possible moves
        moves = possible_moves(state)
        random_move = random.choice(moves)
        return random_move, evaluate(board)
        
    if state["turn"] == 'WHITE':
        maxEval = -100
        next_states = possible_next_states(state)
        for k in range(len(next_states)) :
            next_move, eval = best_move(next_states[k], depth - 1)
            if eval > maxEval:
                maxEval = eval
                chosen_move = next_move
        return chosen_move, maxEval

    else:
        minEval = 100
        next_states = possible_next_states(state)
        for k in range(len(next_states)) :
            next_move, eval = best_move(next_states[k], depth - 1)
            if eval < minEval:
                minEval = eval
                chosen_move = next_move
        return chosen_move, minEval
