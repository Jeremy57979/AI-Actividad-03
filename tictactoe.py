"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    # Acá definimos el tablero inicial con todo vacío.
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Acá contamos cuántas X y cuántas O hay para saber a quién le toca.
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # Si hay más X que O, le toca a O. Si son iguales, le toca arrancar a X.
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Acá recolectamos las coordenadas de todas las casillas que siguen vacías.
    jugadas_posibles = set()
    for fila in range(3):
        for col in range(3):
            if board[fila][col] == EMPTY:
                jugadas_posibles.add((fila, col))
    return jugadas_posibles


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Acá validamos que la jugada sea legal. Si no lo es, lanzamos la excepción.
    if action not in actions(board):
        raise Exception("Acción no válida")
        
    # Copiamos el tablero original para no modificarlo directamente.
    tablero_clon = copy.deepcopy(board)
    tablero_clon[action[0]][action[1]] = player(board)
    return tablero_clon

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Acá revisamos las filas buscando 3 iguales.
    for fila in range(3):
        if board[fila][0] == board[fila][1] == board[fila][2] and board[fila][0] is not None:
            return board[fila][0]
            
    # Acá revisamos las columnas extrayendo los datos de una forma distinta.
    for col in range(3):
        columna_actual = [board[fila][col] for fila in range(3)]
        if columna_actual[0] is not None and all(casilla == columna_actual[0] for casilla in columna_actual):
            return columna_actual[0]
            
    # Acá revisamos las diagonales.
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Si ya hay un ganador, el juego termina.
    if winner(board) is not None:
        return True
        
    # Si todavía hay espacios vacíos, el juego sigue.
    for fila_actual in board:
        if EMPTY in fila_actual:
            return False
            
    # Si no hay ganador y no hay espacios vacíos, es empate y el juego termina.
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    campeon = winner(board)
    # Acá asignamos el valor final: 1 para X, -1 para O, 0 para empate.
    if campeon == X:
        return 1
    elif campeon == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Acá anidamos las funciones de búsqueda directamente dentro de minimax.
    # Así evitamos crear funciones extra fuera de las permitidas.
    
    def buscar_maximo(estado, alfa, beta):
        if terminal(estado):
            return utility(estado), None
        puntaje = float('-inf')
        jugada_ideal = None
        for movimiento in actions(estado):
            puntos_min, _ = buscar_minimo(result(estado, movimiento), alfa, beta)
            if puntos_min > puntaje:
                puntaje = puntos_min
                jugada_ideal = movimiento
            alfa = max(alfa, puntaje)
            if puntaje >= beta:
                break
        return puntaje, jugada_ideal

    def buscar_minimo(estado, alfa, beta):
        if terminal(estado):
            return utility(estado), None
        puntaje = float('inf')
        jugada_ideal = None
        for movimiento in actions(estado):
            puntos_max, _ = buscar_maximo(result(estado, movimiento), alfa, beta)
            if puntos_max < puntaje:
                puntaje = puntos_max
                jugada_ideal = movimiento
            beta = min(beta, puntaje)
            if puntaje <= alfa:
                break
        return puntaje, jugada_ideal

    # Ejecutamos la búsqueda dependiendo de quién es el turno.
    if player(board) == X:
        return buscar_maximo(board, float('-inf'), float('inf'))[1]
    else:
        return buscar_minimo(board, float('-inf'), float('inf'))[1]