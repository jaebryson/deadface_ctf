import telnetlib
import stockfish
import chess
# this is python3

def get_board(tn: telnetlib.Telnet):
    tn.read_until(b'\n')
    board = []
    for i in range(0, 8):
        out = tn.read_until(b'\n').decode('ascii').strip()
        print(out)
        board.append(out)
    
    # convert to FEN
    fen = []
    for row in board:
        row = row.replace(' ', '')
        spaces = 0
        for c in row:
            if c == '.':
                spaces += 1
            else:
                if spaces > 0:
                    fen.append(str(spaces))
                    spaces = 0
                fen.append(c)
        if spaces > 0:
            fen.append(str(spaces))
        fen.append('/')
    fen = ''.join(fen)
    fen = fen[:-1]
    fen += ' w - - 0 1'
    return fen

def get_move(board):
    sf = stockfish.Stockfish(path='/usr/games/stockfish')
    sf.set_fen_position(board)

    sf.update_engine_parameters({"Threads": 4})
    # set search depth
    sf.set_depth(10)
    # set stockfish level
    sf.set_skill_level(20)
    move = sf.get_best_move()

    # convert from UCI to SAN
    board = chess.Board(board)
    move = board.san(chess.Move.from_uci(move))
    return move


if __name__ == '__main__':
    HOST = "grandmaster.deadface.io"
    PORT = 5000

    # connect and get the first prompt
    tn = telnetlib.Telnet(HOST, PORT)

    board = get_board(tn)
    print(board)
    move = get_move(board)
    print(move)
    # put move into bit string
    move = move.encode('utf-8')
    tn.write(move + b'\n')

    # read the next line
    out = tn.read_until(b'\n')
    print(out.decode('ascii').strip())
