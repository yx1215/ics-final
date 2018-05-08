from evaluate import evaluate_line
from copy import deepcopy
import random

class branch():
    def __init__(self, chess, level, color,x,y):
        self.chess = chess
        self.color = color
        self.level = level
        self.length = len(self.chess)
        self.width = len(self.chess[0])
        self.i = x
        self.j = y

    def move(self, i, j, color):
        self.chess[i][j] = color

    def traverse(self):
        #for i in range(0, self.length):
        #    for j in range(0, self.width):
        q = 6
        m = self.i -q
        n = self.i +q
        x = self.j -q
        y = self.j +q
        if self.i-q < 0:
            m = 0
        if self.i+q > self.length:
            n = self.length
        if self.j-q < 0:
            x = 0
        if self.j+q > self.length:
            y = self.length
        for i in range(m,n):
            for j in range(x,y):
                if self.chess[i][j] == 0:
                    if self.color == "black":
                        nextcolor = "white"
                    elif self.color == "white":
                        nextcolor = "black"
                    new_branch = branch(deepcopy(self.chess), self.level-1, nextcolor,i,j)
                    new_branch.move(i, j, self.color)
                    yield new_branch, i, j

    def real_traverse(self):
        lst = []
        lst1 = []
        for i in self.traverse():
            lst.append(i[0].evaluateNega())
        lst.sort()
        lst = lst[-10::-1]
        for i in self.traverse():
            if i[0].evaluateNega() in lst:
                lst1.append(i)
        #print(lst)
        return lst1

    def evaluateNega(self):
        return -self.evaluate(self.chess,self.color)
        #return -self.evaluate(self.narrow(self.i,self.j),self.color)



    def evaluate(self,chess,color):
        vecs = []
        # shu hang
        length = len(chess)
        width = len(chess[0])
        for i in range(length):
            vecs.append(chess[i])
        # heng hang
        for j in range(width):
            vecs.append([chess[i][j] for i in range(0,length)])

        # \
        vecs.append([chess[x][x] for x in range(0,length)])
        for i in range(1, length-4):
            vec = [chess[x][x-i] for x in range(i, length)]
            vecs.append(vec)
            vec = [chess[y-i][y] for y in range(i, width)]
            vecs.append(vec)

        # /
        for i in range(4, length-1):
            vec = [chess[x][i-x] for x in range(i, -1, -1)]
            vecs.append(vec)
            vec = [chess[x][width-x+length-i-2] for x in range(length-i-1, length)]
            vecs.append(vec)

        table_score = 0
        for vec in vecs:
            score = evaluate_line(vec)
            if color == "black":
                #table_score += score['white'][0] - score['black'][0] - score['black'][1]
                score["white"][1] += 100
                table_score += score['white'][0] - score['black'][0] + score['white'][1]
            elif color == "white":
                score["black"][1] += 100
                #table_score += score['black'][0]- score['white'][0] - score['white'][1]
                table_score += score['black'][0]-score['white'][0] + score['black'][1]

        for i in range(15):
            for j in range(15):
                stone = chess[i][j]
                if color == "black":
                    if stone == "black":
                        table_score -= 7 - max(abs(i-7),abs(j-7))
                    elif stone == "white":
                        table_score += 7 - max(abs(i-7),abs(j-7))
                if color == "white":
                    if stone == "white":
                        table_score -= 7 - max(abs(i-7),abs(j-7))
                    elif stone == "black":
                        table_score += 7 - max(abs(i-7),abs(j-7))

        return table_score


def alphaBeta(branch, alpha= -99999, beta=99999):
    if branch.level <= 0:
        score = branch.evaluateNega()
        return score

    for new_branch, i, j in branch.traverse():
        new_score = -alphaBeta(new_branch, -beta, -alpha)
        if new_score > beta:
            return new_score
        if new_score > alpha:
            alpha = new_score
            branch.i, branch.j = i, j

    return alpha
