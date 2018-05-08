from tkinter import *
from tkinter.messagebox import *
from evaluate import *
from alphmao import branch, alphaBeta
#from alphmao import NODE, miniMax, alphaBeta

class Board():

    def __init__(self):
        self.number_of_move = 0
        self.size = 16
        self.chess = [[0 for i in range(self.size + 1)] for i in range(self.size + 1)]
        self.realchess = [[0 for k in range(self.size)] for k in range(self.size)]
        for i in range(1,self.size + 1):
            for j in range(1,self.size + 1):
                self.realchess[i-1][j-1] = self.chess[i][j]
        self.width = (self.size + 1) * 30
        self.height = (self.size + 1) * 30
        board_size = str(self.width) + "x" + str(self.height)
        tk = Tk()
        tk.title("GoBang")
        tk.geometry(board_size)
        self.checkboard = Canvas(tk, width=self.width, height=self.height)
        self.checkboard.pack(expand=YES, fill=BOTH)
        self.level = 1

    def set_size(self, size):
        self.size = size
        self.reset()

    def display_board(self):
        for i in range(1, self.size + 1):
            self.checkboard.create_line(i * 30, 30, i * 30, 480, width=2)
        for i in range(1, self.size + 1):
            self.checkboard.create_line(30, i * 30, 480, i * 30, width=2)

    def turn(self):
        if self.number_of_move % 2 == 0:
            return "black"
        else:
            return "white"

    def move(self, event):
        if event.x % 30 > 15:
            event.x = event.x // 30 + 1
        else:
            event.x = event.x // 30
        if event.y % 30 > 15:
            event.y = event.y // 30 + 1
        else:
            event.y = event.y // 30

        if event.x > self.size:
            event.x = self.size
        if event.y > self.size:
            event.y = self.size
        if event.x < 1:
            event.x = 1
        if event.y < 1:
            event.y = 1

        x1 = event.x * 30 - 15
        y1 = event.y * 30 - 15
        x2 = event.x * 30 + 15
        y2 = event.y * 30 + 15

        if self.chess[event.x][event.y] == 0:
            self.checkboard.create_oval(x1, y1, x2, y2, fill=self.turn())
            self.chess[event.x][event.y] = self.turn()
            #print(event.x-1,event.y-1)
            #print(len(self.realchess[0]),len(self.realchess))
            self.realchess[event.x-1][event.y-1] = self.turn()
            #branch1 = branch(self.realchess,self.level,self.turn())
            #print(branch1.evaluateNega())
            self.number_of_move += 1
            win_state, player = self.judge_win()
            #score = alphaBeta(branch1)
            #print(score)
            #print(self.chess)
            #print(self.realchess)
            if win_state:
                continued = askyesno("message", player + " win" + "\n" + "try again?")
                if continued:
                    self.reset()
            else:
                self.move_alph()

    def move_alph(self):
        branch1 = branch(self.realchess,self.level,self.turn())
        #branch1 = NODE(self.realchess,self.level,self.turn())
        score = alphaBeta(branch1)
        #print(branch1.i,branch1.j)
        #print(score)
        x1 = (branch1.i + 1) * 30 - 15
        y1 = (branch1.j + 1) * 30 - 15
        x2 = (branch1.i + 1) * 30 + 15
        y2 = (branch1.j + 1) * 30 + 15
        self.checkboard.create_oval(x1, y1, x2, y2, fill=self.turn())
        self.chess[branch1.i+1][branch1.j+1] = self.turn()
        self.realchess[branch1.i][branch1.j] = self.turn()
        self.number_of_move += 1
        win_state, player = self.judge_win()
        if win_state:
                continued = askyesno("message", player + " win" + "\n" + "try again?")
                if continued:
                    self.reset()

    def move2(self):
         self.checkboard.bind("<Button-1>", self.move)


    def reset(self):
         self.chess = [[0 for i in range(self.size + 1)] for i in range(self.size + 1)]
         self.checkboard.delete("all")
         self.display_board()

    def judge_win_up(self, x, y):
        if 0 != self.chess[x][y] == self.chess[x][y + 1] == self.chess[x][y + 2] == self.chess[x][y + 3] == self.chess[x][y + 4]:
            return True
        else:
            return False

    def judge_win_cross(self, x, y):
        if 0 != self.chess[x][y] == self.chess[x + 1][y] == self.chess[x + 2][y] == self.chess[x + 3][y] == self.chess[x + 4][y]:
            return True
        else:
            return False

    def judge_win_diagonal(self, x, y):
        if 0 != self.chess[x][y] == self.chess[x + 1][y + 1] == self.chess[x + 2][y + 2] == self.chess[x + 3][y + 3] == self.chess[x + 4][y + 4]:
            return True
        else:
            return False

    def judge_win_diagonal2(self, x, y):
        if 0 != self.chess[x][y] == self.chess[x + 1][y - 1] == self.chess[x + 2][y - 2] == self.chess[x + 3][y - 3] == self.chess[x + 4][y - 4]:
            return True
        else:
            return False

    def judge_win(self):
        for i in range(1, self.size + 1):
            for j in range(1, self.size - 3):
                if self.judge_win_up(i, j):
                    return True, self.chess[i][j]
        for i in range(1, self.size - 3):
            for j in range(1, self.size + 1):
                if self.judge_win_cross(i, j):
                    return True, self.chess[i][j]
        for i in range(1, self.size - 3):
            for j in range(1, self.size - 3):
                if self.judge_win_diagonal(i, j):
                    return True, self.chess[i][j]
        for i in range(1, self.size - 3):
            for j in range(self.size, 5, -1):
                if self.judge_win_diagonal2(i, j):
                    return True, self.chess[i][j]
        return False, None



if __name__ == "__main__":
    b = Board()
    b.display_board()
    # win_state, winner = b.judge_win()
    # while True:
    b.move2()
    # win_state, winner = b.judge_win()

    # if win_state:
    #     continued = askyesno("message", winner + "win" + "\n" + "try again?")
    #     if continued:
    #         b.reset()
    #         # else:
    #         #     break










# size = 16
# chess = [[0 for i in range(size)] for i in range(size)]


# def move(event):
#     if event.x % 30 > 15:
#         event.x = event.x // 30 + 1
#     else:
#         event.x = event.x // 30
#     if event.y % 30 > 15:
#         event.y = event.y // 30 + 1
#     else:
#         event.y = event.y // 30
#     x1, y1 = (event.x + 1) * 30, (event.y + 1) * 30



# def board():
#     tk = Tk()
#     tk.title("五子棋")
#     tk.geometry("510x510")
#     checkboard = Canvas(tk, width=500, height=500)
#     checkboard.pack(expand=YES, fill=BOTH)
#     for i in range(1, size + 1):
#         checkboard.create_line(i * 30, 30, i * 30, 480, width=2)
#     for i in range(1, size + 1):
#         checkboard.create_line(30, i * 30, 480, i * 30, width=2)


