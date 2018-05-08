from tkinter import *
from tkinter.messagebox import *
from chat_utils import *
from tkinter.font import *
import json
import random
from alphmao import *
from evaluate import *
class Board:

    def __init__(self, color, name):
        self.black = 0
        self.white = 0
        self.color = color
        self.number_of_move = 0
        self.size = 16

        self.chess = [[0 for i in range(self.size + 1)] for i in range(self.size + 1)]
        self.realchess = [[0 for i in range(self.size)] for i in range(self.size)]
        for i in range(1,self.size + 1):
            for j in range(1,self.size + 1):
                self.realchess[i-1][j-1] = self.chess[i][j]
        self.width = (self.size + 1) * 30 + 300
        self.height = (self.size + 1) * 30
        self.finished = False
        self.x = None
        self.y = None
        self.is_reset = False
        board_size = str(self.width) + "x" + str(self.height)
        self.tk = Tk()
        self.tk.title(name + "'s" + " GoBang")
        self.tk.geometry(board_size)
        self.font = Font(family="Helvetica", size=36)
        self.font2 = Font(size=15)
        self.checkboard = Canvas(self.tk, width=self.width, height=self.height)
        self.text_my_color = self.checkboard.create_text((650, 100), text="My color is: " + self.color, font=self.font)
        self.text_turn = self.checkboard.create_text((650, 150), text="Turn: " + self.turn(), font=self.font)
        # self.text_num = self.checkboard.create_text((650, 200),
        #                                             text="You have made {0} moves".format(
        #                                                 str((self.number_of_move - 1) // 2 + 1)), font=self.font2)
        # return event.x, event.y
        self.checkboard.pack(expand=YES, fill=BOTH)

        for i in range(1, self.size + 1):
            self.checkboard.create_line(i * 30, 30, i * 30, 480, width=2)
        for i in range(1, self.size + 1):
            self.checkboard.create_line(30, i * 30, 480, i * 30, width=2)
        # mainloop()
        self.level = 3

    def turn(self):
        if self.number_of_move % 2 == 0:
            return "black"
        else:
            return "white"

    def set_size(self, size):
        self.size = size
        self.reset()

    def current_position(self):
        return self.x, self.y

    def single_move(self, event):
        self.checkboard.delete(self.text_turn)
        # self.checkboard.delete(self.text_num)

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
        if self.chess[event.x][event.y] == 0 and self.color == self.turn() and not self.is_finished():
            self.x = event.x
            self.y = event.y
            self.checkboard.create_oval(x1, y1, x2, y2, fill=self.turn())
            self.chess[event.x][event.y] = self.turn()
            self.number_of_move += 1

        self.text_turn = self.checkboard.create_text((650, 150), text="Turn: " + self.turn(), font=self.font)
        # self.text_num = self.checkboard.create_text((650, 200), text="You have made {0} moves".format(
        #         str(self.return_move(self.color)), font=self.font2))

    def bind(self):
        self.checkboard.bind("<Button-1>", self.single_move)

    def return_move(self, color):
        black = (self.number_of_move - 1) // 2 + 1
        white = self.number_of_move // 2 + 1
        if color == "black":
            return black
        else:
            return white

    def move(self, event):

        self.checkboard.delete(self.text_turn)
        # self.checkboard.delete(self.text_num)

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
        self.x = event.x
        self.y = event.y
        x1 = event.x * 30 - 15
        y1 = event.y * 30 - 15
        x2 = event.x * 30 + 15
        y2 = event.y * 30 + 15
        if self.chess[event.x][event.y] == 0:
            self.checkboard.create_oval(x1, y1, x2, y2, fill=self.turn())
            self.chess[event.x][event.y] = self.turn()
            self.realchess[event.x - 1][event.y - 1] = self.turn()
            self.number_of_move += 1
            win_state, player = self.judge_win()
            if win_state:
                continued = askyesno("message", player + " win" + "\n" + "try again?")
                if continued:
                    self.reset()

                else:
                    self.finished = True

            else:
                self.move_alph()

        self.text_turn = self.checkboard.create_text((650, 150), text="Turn: " + self.turn(), font=self.font)
        # self.text_num = self.checkboard.create_text((650, 200),text= "You have made {0} moves".format(str((self.number_of_move - 1) // 2 + 1)), font=self.font2)

    def retry(self):
        win_state, player = self.judge_win()
        if win_state:
            continued = askyesno("message", player + " win" + "\n" + "try again?")
            if continued:
                self.finished = False
                self.is_reset = True

            else:
                self.finished = True

    def reset_state(self):
        return self.is_reset

    def is_finished(self):
        return self.finished

    def bind2(self):
        self.checkboard.bind("<Button-1>", self.move)

    def other_color(self):
        if self.color == "black":
            return "white"
        else:
            return "black"

    def other_move(self, x, y, color):

        if x is not None:
            self.checkboard.delete(self.text_turn)
            # self.checkboard.delete(self.text_num)
            x1 = x * 30 - 15
            y1 = y * 30 - 15
            x2 = x * 30 + 15
            y2 = y * 30 + 15
            if self.chess[x][y] == 0:
                self.checkboard.create_oval(x1, y1, x2, y2, fill=self.turn())
                self.chess[x][y] = color
                self.number_of_move += 1

            self.text_turn = self.checkboard.create_text((650, 150), text="Turn: " + self.turn(), font=self.font)
            # self.text_num = self.checkboard.create_text((650, 200), text="You have made {0} moves".format(
            #     str(self.return_move(self.other_color())), font=self.font2))

    def quit(self):
        self.reset()
        self.tk.destroy()

    def reset(self):
        self.chess = [[0 for i in range(self.size + 1)] for i in range(self.size + 1)]
        self.realchess = [[0 for i in range(self.size)] for i in range(self.size)]
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                self.realchess[i - 1][j - 1] = self.chess[i][j]
        self.number_of_move = 0
        self.checkboard.delete("all")
        for i in range(1, self.size + 1):
            self.checkboard.create_line(i * 30, 30, i * 30, 480, width=2)
        for i in range(1, self.size + 1):
            self.checkboard.create_line(30, i * 30, 480, i * 30, width=2)
        self.x = None
        self.y = None
        self.finished = False
        self.is_reset = False
        self.text_my_color = self.checkboard.create_text((650, 100), text="My color is: " + self.color, font=self.font)
        # self.text_turn = self.checkboard.create_text((650, 150), text="Turn: " + self.turn(), font=self.font)
        # self.text_num = self.checkboard.create_text((650, 200),
        #                                             text="You have made {0} moves".format(
        #                                                 str((self.number_of_move - 1) // 2 + 1)), font=self.font2)

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

    def mainloop(self):
        self.checkboard.mainloop()

    def update(self):
        self.checkboard.update_idletasks()
        self.checkboard.update()


    def move_alph(self):
        branch1 = branch(self.realchess,self.level,self.turn(), self.x, self.y)
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
                else:
                    self.finished = True


if __name__ == "__main__":
    b = Board("black", "a")
    # b.display_board()
    # b.move2_color(1,2,"black")
    b.bind2()
    while True:
        # b.move2()
        b.update()
        if b.is_finished():
            b.quit()







