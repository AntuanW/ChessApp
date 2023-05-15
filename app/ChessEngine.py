import chess
import chess.polyglot


class ChessEngine:
    def __init__(self, board, depth=2):
        self.board = board

        self.depth = depth

        self.pawntable = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.knightstable = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]

        self.bishopstable = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]

        self.rookstable = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.queenstable = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 5, 5, 5, 5, 5, 0, -10,
            0, 0, 5, 5, 5, 5, 0, -5,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]

        self.kingstable = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]

        self.boardvalue = self.init_evaluate_board()

        self.piecetypes = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]

        self.tables = [self.pawntable, self.knightstable, self.bishopstable, self.rookstable, self.queenstable,
                       self.kingstable]

        self.piecevalues = [100, 320, 330, 500, 900]

        self.movehistory = []

    def init_evaluate_board(self):
        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        bp = len(self.board.pieces(chess.PAWN, chess.BLACK))
        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        br = len(self.board.pieces(chess.ROOK, chess.BLACK))
        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))

        material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

        pawnsq = sum([self.pawntable[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq = pawnsq + sum([-self.pawntable[chess.square_mirror(i)]
                               for i in self.board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([self.knightstable[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-self.knightstable[chess.square_mirror(i)]
                                   for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([self.bishopstable[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-self.bishopstable[chess.square_mirror(i)]
                                   for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([self.rookstable[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-self.rookstable[chess.square_mirror(i)]
                               for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([self.queenstable[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-self.queenstable[chess.square_mirror(i)]
                                 for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([self.kingstable[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-self.kingstable[chess.square_mirror(i)]
                               for i in self.board.pieces(chess.KING, chess.BLACK)])

        boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

        return boardvalue

    def evaluate_board(self):

        if self.board.is_checkmate():
            if self.board.turn:
                return -9999
            else:
                return 9999
        if self.board.is_stalemate():
            return 0
        if self.board.is_insufficient_material():
            return 0

        eval = self.init_evaluate_board()
        if self.board.turn:
            return eval
        else:
            return -eval

    def update_eval(self, mov, side):
        # update piecequares
        movingpiece = self.board.piece_type_at(mov.from_square)
        if side:
            self.boardvalue = self.boardvalue - self.tables[movingpiece - 1][mov.from_square]
            # update castling
            if (mov.from_square == chess.E1) and (mov.to_square == chess.G1):
                self.boardvalue = self.boardvalue - self.rookstable[chess.H1]
                self.boardvalue = self.boardvalue + self.rookstable[chess.F1]
            elif (mov.from_square == chess.E1) and (mov.to_square == chess.C1):
                self.boardvalue = self.boardvalue - self.rookstable[chess.A1]
                self.boardvalue = self.boardvalue + self.rookstable[chess.D1]
        else:
            self.boardvalue = self.boardvalue + self.tables[movingpiece - 1][mov.from_square]
            # update castling
            if (mov.from_square == chess.E8) and (mov.to_square == chess.G8):
                self.boardvalue = self.boardvalue + self.rookstable[chess.H8]
                self.boardvalue = self.boardvalue - self.rookstable[chess.F8]
            elif (mov.from_square == chess.E8) and (mov.to_square == chess.C8):
                self.boardvalue = self.boardvalue + self.rookstable[chess.A8]
                self.boardvalue = self.boardvalue - self.rookstable[chess.D8]

        if side:
            self.boardvalue = self.boardvalue + self.tables[movingpiece - 1][mov.to_square]
        else:
            self.boardvalue = self.boardvalue - self.tables[movingpiece - 1][mov.to_square]

        # update material
        if mov.drop != None:
            if side:
                self.boardvalue = self.boardvalue + self.piecevalues[mov.drop - 1]
            else:
                self.boardvalue = self.boardvalue - self.piecevalues[mov.drop - 1]

        # update promotion
        if mov.promotion != None:
            if side:
                self.boardvalue = self.boardvalue + self.piecevalues[mov.promotion - 1] - self.piecevalues[
                    movingpiece - 1]
                self.boardvalue = self.boardvalue - self.tables[movingpiece - 1][mov.to_square] + \
                                  self.tables[mov.promotion - 1][mov.to_square]
            else:
                self.boardvalue = self.boardvalue - self.piecevalues[mov.promotion - 1] + self.piecevalues[
                    movingpiece - 1]
                self.boardvalue = self.boardvalue + self.tables[movingpiece - 1][mov.to_square] - \
                                  self.tables[mov.promotion - 1][mov.to_square]

        return mov

    def make_move(self, mov):
        self.update_eval(mov, self.board.turn)
        self.board.push(mov)
        return mov

    def unmake_move(self):
        mov = self.board.pop()
        self.update_eval(mov, not self.board.turn)

        return mov

    def quiesce(self, alpha, beta):
        stand_pat = self.evaluate_board()
        if (stand_pat >= beta):
            return beta
        if (alpha < stand_pat):
            alpha = stand_pat

        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.make_move(move)
                score = -self.quiesce(-beta, -alpha)
                self.unmake_move()

                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha

    def alphabeta(self, alpha, beta, depthleft):
        bestscore = -9999
        if (depthleft == 0):
            return self.quiesce(alpha, beta)
        for move in self.board.legal_moves:
            self.make_move(move)
            score = -self.alphabeta(-beta, -alpha, depthleft - 1)
            self.unmake_move()
            if (score >= beta):
                return score
            if (score > bestscore):
                bestscore = score
            if (score > alpha):
                alpha = score
        return bestscore

    def selectmove(self, depth):
        try:
            move = chess.polyglot.MemoryMappedReader("../resources/ChessImg/Perfect2017.bin").weighted_choice(
                self.board).move
            self.movehistory.append(move)
            return move
        except:
            bestMove = chess.Move.null()
            bestValue = -99999
            alpha = -100000
            beta = 100000
            for move in self.board.legal_moves:
                self.make_move(move)
                boardValue = -self.alphabeta(-beta, -alpha, depth - 1)
                if boardValue > bestValue:
                    bestValue = boardValue;
                    bestMove = move
                if (boardValue > alpha):
                    alpha = boardValue
                self.unmake_move()
            self.movehistory.append(bestMove)
            return bestMove

    def make_best_move(self):
        mov = self.selectmove(self.depth)
        self.make_move(mov)
