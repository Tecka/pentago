import sys
import math

game_board = [[0 for i in range(6)] for j in range(6)]
# 0 : empty cell
# 1 : white cell
# -1 : black cell

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def move(oneboard, maximizingPlayer, row, col, turn_quadran, turn_direction): # renvoie new_board après un move
    #print("je move")
    new_board = [[2 for i in range(6)] for j in range(6)]

    for i in range(6):
        for j in range(6):
            new_board[i][j]= oneboard[i][j]

    # poser la bille de couleur
    if oneboard[row][col] == 0:
        if maximizingPlayer:
            new_board[row][col] = 1
        else:
            new_board[row][col] = -1
    else:
        print("Il y a déjà une bille ici")
        return

    #repérer le quadran à tourner
    if turn_quadran == "TopLeft":
        i_shift, j_shift = 0, 0
    elif turn_quadran == "TopRight":
        i_shift, j_shift = 0, 3
    elif turn_quadran == "DownLeft":
        i_shift, j_shift = 3, 0
    elif turn_quadran == "DownRight":
        i_shift, j_shift = 3, 3
    else:
        print("C'est quoi ce quadran de rotation ?? ", turn_quadran)
        return

    buffer_quadran = [[2 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            buffer_quadran[i][j] = new_board[i+i_shift][j+j_shift]

    #print("buffer_quadran")
    #print(buffer_quadran)

    #tourner le quadran
    turned_quadran = [[2 for i in range(3)] for j in range(3)]
    if turn_direction == "Right":
        turned_quadran[0][0]=buffer_quadran[2][0]
        turned_quadran[0][1]=buffer_quadran[1][0]
        turned_quadran[0][2]=buffer_quadran[0][0]
        turned_quadran[1][0]=buffer_quadran[2][1]
        turned_quadran[1][1]=buffer_quadran[1][1]
        turned_quadran[1][2]=buffer_quadran[0][1]
        turned_quadran[2][0]=buffer_quadran[2][2]
        turned_quadran[2][1]=buffer_quadran[1][2]
        turned_quadran[2][2]=buffer_quadran[0][2]
    elif turn_direction == "Left":
        turned_quadran[0][0]=buffer_quadran[0][2]
        turned_quadran[0][1]=buffer_quadran[1][2]
        turned_quadran[0][2]=buffer_quadran[2][2]
        turned_quadran[1][0]=buffer_quadran[0][1]
        turned_quadran[1][1]=buffer_quadran[1][1]
        turned_quadran[1][2]=buffer_quadran[2][1]
        turned_quadran[2][0]=buffer_quadran[0][0]
        turned_quadran[2][1]=buffer_quadran[1][0]
        turned_quadran[2][2]=buffer_quadran[2][0]
    else:
        print("C'est quoi cette direction de rotation ?? ", turn_direction)
        return

    #print("turned_quadran")
    #print(turned_quadran)

    #remettre le turned_quadran dans le board
    for i in range(3):
        for j in range(3):
            new_board[i+i_shift][j+j_shift] = turned_quadran[i][j]

    #affiche(new_board)   
    return new_board     

def affiche(aboard): # affiche un board
    for i in range(6):
        print(aboard[i])

def evaluate(board): # renvoie l'évaluation de la position du board (10 si blanc gagne, -10 si noir gagne, sinon 0)
    # si blanc aligne 5 billes, alors répondre 10
    for line in range(6):
        if board[line][0] + board[line][1] + board[line][2] + board[line][3] + board[line][4] == 5:
            return 10
        if board[line][1] + board[line][2] + board[line][3] + board[line][4] + board[line][5] == 5:
            return 10
    for row in range(6):
        if board[0][row] + board[1][row] + board[2][row] + board[3][row] + board[4][row] == 5:
            return 10
        if board[1][row] + board[2][row] + board[3][row] + board[4][row] + board[5][row] == 5:
            return 10
    if board[0][0] + board[1][1] + board[2][2] + board[3][3] + board[4][4] == 5:
        return 10
    if board[1][1] + board[2][2] + board[3][3] + board[4][4] + board[5][5] == 5:
        return 10
    if board[0][1] + board[1][2] + board[2][3] + board[3][4] + board[4][5] == 5:
        return 10
    if board[1][0] + board[2][1] + board[3][2] + board[4][3] + board[5][4] == 5:
        return 10
    if board[4][0] + board[3][1] + board[2][2] + board[1][3] + board[0][4] == 5:
        return 10
    if board[5][1] + board[4][2] + board[3][3] + board[2][4] + board[1][5] == 5:
        return 10
  
    # si noir aligne 5 billes, alors répondre -10
    for line in range(6):
        if board[line][0] + board[line][1] + board[line][2] + board[line][3] + board[line][4] == -5:
            return -10
        if board[line][1] + board[line][2] + board[line][3] + board[line][4] + board[line][5] == -5:
            return -10
    for row in range(6):
        if board[0][row] + board[1][row] + board[2][row] + board[3][row] + board[4][row] == -5:
            return -10
        if board[1][row] + board[2][row] + board[3][row] + board[4][row] + board[5][row] == -5:
            return -10
    if board[0][0] + board[1][1] + board[2][2] + board[3][3] + board[4][4] == -5:
        return -10
    if board[1][1] + board[2][2] + board[3][3] + board[4][4] + board[5][5] == -5:
        return -10
    if board[0][1] + board[1][2] + board[2][3] + board[3][4] + board[4][5] == -5:
        return -10
    if board[1][0] + board[2][1] + board[3][2] + board[4][3] + board[5][4] == -5:
        return -10
    if board[4][0] + board[3][1] + board[2][2] + board[1][3] + board[0][4] == -5:
        return -10
    if board[5][1] + board[4][2] + board[3][3] + board[2][4] + board[1][5] == -5:
        return -10

    # sinon répondre 0
    return 0

def some_moves(): #test de quelques smoves
    global game_board

    game_board = move(game_board, True, 0, 0, "TopLeft", "Right")
    print(evaluate(game_board))
    game_board = move(game_board, True, 1, 1, "TopRight", "Right")
    print(evaluate(game_board))
    game_board = move(game_board, False, 0, 5, "TopLeft", "Left")
    print(evaluate(game_board))
    game_board = move(game_board, True, 2, 2, "TopLeft", "Right")
    print(evaluate(game_board))
    game_board = move(game_board, True, 3, 3, "TopRight", "Right")
    print(evaluate(game_board))
    game_board = move(game_board, True, 4, 4, "TopLeft", "Left")
    print(evaluate(game_board))

def multiple_boards(board): #test de plusieurs boards
    #print(">> board")
    #print(board)
    #affiche(board)

    old_board = board
    #print(">> old_board")
    #print(old_board)
    #affiche(old_board)

    new_board = move(old_board, False, 0, 5, "TopLeft", "Left")
    print(">> old_board")
    #print(old_board)
    affiche(old_board)
    
    print(">> board")
    #print(board)
    affiche(board)


    print(">> new_board")
    #print(new_board)
    affiche(new_board)


    list_of_two_boards = old_board, new_board

    print("------")
    affiche(old_board)
    print(">>")
    affiche(list_of_two_boards[0])
    affiche(list_of_two_boards[1])
    print("========")
    print(list_of_two_boards)
    print("------")

def possible_next_boards(board, maximizingPlayer): #renvoie la liste des positions possibles au prochain coup =====ADD ROTATIONS
    possible_next_boards = list()
    #print("Whites playes ? ", maximizingPlayer)

    initial_board = [[2 for i in range(6)] for j in range(6)]
    for i in range(6):
        for j in range(6):
            initial_board[i][j]= board[i][j]
    #affiche(initial_board)

    for i in range(6):
        for j in range(6):
            if initial_board[i][j] == 0:
                # faire 8 nouveau board et les append à la liste
                potential_board_1 = move(initial_board, maximizingPlayer, i, j, "TopLeft", "Right")
                potential_board_2 = move(initial_board, maximizingPlayer, i, j, "TopLeft", "Left")
                potential_board_3 = move(initial_board, maximizingPlayer, i, j, "TopRight", "Right")
                potential_board_4 = move(initial_board, maximizingPlayer, i, j, "TopRight", "Left")
                potential_board_5 = move(initial_board, maximizingPlayer, i, j, "DownLeft", "Right")
                potential_board_6 = move(initial_board, maximizingPlayer, i, j, "DownLeft", "Left")
                potential_board_7 = move(initial_board, maximizingPlayer, i, j, "DownRight", "Right")
                potential_board_8 = move(initial_board, maximizingPlayer, i, j, "DownRight", "Left")
                possible_next_boards.append(potential_board_1)
                possible_next_boards.append(potential_board_2)
                possible_next_boards.append(potential_board_3)
                possible_next_boards.append(potential_board_4)
                possible_next_boards.append(potential_board_5)
                possible_next_boards.append(potential_board_6)
                possible_next_boards.append(potential_board_7)
                possible_next_boards.append(potential_board_8)
            
    """
    for p in range(len(possible_next_boards)):
        print("-possible next-")
        affiche(possible_next_boards[p])
    """
    print("Listing the 10 next possible boards")
    for p in range(10):
        print(p)
        affiche(possible_next_boards[p])

    return possible_next_boards

def minimax(board, depth, maximizingPlayer): #
    #print("Entering minimax with this board...")
    #affiche(board)
    #print(evaluate(board))

    if depth == 0 : # if we don't want to explore further
        #print("Profondeur max atteinte.")
        return evaluate(board), board
        
    if maximizingPlayer : # if it's White who needs to move
        maxEval = -100
        #calculer toutes les positions possibles : possible_next_boards
        next_boards = possible_next_boards(board, maximizingPlayer)
 
        for p in range(len(next_boards)) :
            #print("--possible--")
            #affiche(next_boards[p])
            eval, next_board = minimax(next_boards[p], depth - 1, False)
            if eval > maxEval:
                maxEval = eval
                chosen_board = next_board
        return maxEval, chosen_board
    else:
        minEval = 100
        next_boards = possible_next_boards(board, not(maximizingPlayer))
        for p in range(len(next_boards)) :
            #print("--possible--")
            #affiche(next_boards[p])
            eval, next_board = minimax(next_boards[p], depth - 1, True)
            if eval < minEval:
                minEval = eval
                chosen_board = next_board
        return minEval, chosen_board
 
 
# initial call
"""
evaluation, euh = minimax([[0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 1, 0, 1, 1, -1]], 1, True)
print(evaluation)
affiche(euh)
"""


# some_moves()
# multiple_boards(game_board)

def game(): # lance une partie de zéro
    print("(1) Les blancs commencent")
    print("(-1) Les noirs commencent")
    WhiteMoves = int(input("? "))
    print("=====")
    current_board = [[0 for i in range(6)] for j in range(6)]
    turn = 1
    if WhiteMoves == 1:
        print("les blancs commencent")

        #demander quel move
        her_move = input("Où joue Charlotte ('ligne colonne') ? ")
        print("elle joue : ", her_move)
        her_turn = input("Que tourne Charlotte ('quadran direction') ? ")
        if her_turn[0] == "1":
            turn_quadran = "TopLeft"
        elif her_turn[0] == "2":
            turn_quadran = "TopRight"
        elif her_turn[0] == "3":
            turn_quadran = "DownLeft"
        elif her_turn[0] == "4":
            turn_quadran = "DownRight"
        print(turn_quadran)

        #l'appliquer au current board
        print(her_move[0])
        print(her_move[2])
        new_board = move(current_board, True, int(her_move[0]), int(her_move[2]), turn_quadran, her_turn.split(" ")[1])
        print("---------")
        print("tour : ", turn)
        affiche(new_board)
        print(evaluate(new_board))
    else: 
        print("les noirs commencent")
        # noir joue un centre : l'appliquer au current board

  
    for t in range(1):
        print("---------")
          #jouer un move
          #si on gagne, fin
          #sinon demander le move de blanc
          #si blanc a gagné, fin
          #sinon on recommence


    return

def whatplay(): # renvoie le meilleur move à faire pour les noirs

    #saisir le board
    confirmed = False
    while confirmed == False:
        current_board = [[2 for i in range(6)] for j in range(6)]
        print("Quelle est la position actuelle ? 2:noirs 1:blancs 0:libres")
        for i in range(6):
            row = input()
            for j in range(6):
                current_board[i][j] = int(row[j])
                if current_board[i][j] ==2:
                    current_board[i][j] = -1     
        #affiche(current_board)
        confirmed = query_yes_no("Confirmé ?")

    if evaluate(current_board) == 10 :
        print("Blanc a gagné")
        return
    if evaluate(current_board) == -10 :
        print("Noir a gagné")
        return

    

    
    #choisir le meilleur move à faire
    print("Noir réfléchit...")
    minimax(current_board, 1, False)


    best_row = 9
    best_col = 9
    best_quadran = "Center"
    best_direction = "Freeze"

    #renvoyer le row,col, quadran, direction du move
    print("Noir joue : ", best_row, best_col)
    print("et tourne le quadran : ", best_quadran, best_direction)


#whatplay()

def test_move(tested_board):
    test_board = [[2 for i in range(6)] for j in range(6)]
    for i in range(6):
        for j in range(6):
            test_board[i][j] = tested_board[i][j]

    print("Testing...")
    affiche(test_board)


    eval, answered_board = minimax(test_board, 1, True)
    print("Playing...")
    affiche(answered_board)
    print("worth...", eval, " ?")
    print(evaluate(answered_board))




test_move([[1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, -1, 0, -1, 0], [0, 0, -1, -1, 1, -1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
