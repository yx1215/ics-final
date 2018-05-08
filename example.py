from tkinter import *
import tkinter.messagebox

color_number = 1
code = ""
size = 16
chess_color = 0
xxx = 1
yyy = 1
# 保存棋盘
chess = [[0 for i in range(size+1)] for i in range(size+1)]
# 保存棋盘权值
chess_Value = [[0 for i in range(size+1)] for i in range(size+1)]
dic = {"0": 0, "1": 8, "2": 10, "11": 50, "22": 1000, "111": 2500, "222": 3000, "1111": 5000, "2222": 20000,
       "21": 4, "12": 2, "211": 25, "122": 20, "11112": 3000, "112": 30, "1112": 2800, "221": 500, "2221": 2000,
       "22221": 10000}


def paint(event):
    #  使棋落在棋盘点上
    global color_number
    if event.x % 30 > 15 :
        event.x = event.x//30 + 1
    else:
        event.x = event.x // 30
    if event.y % 30 > 15:
        event.y = event.y // 30 + 1
    else:
        event.y = event.y//30
    if event.x > size:
        event.x = size
    if event.y > size:
        event.y = size
    if event.x < 1:
        event.x = 1
    if event.y < 1:
        event.y = 1

    # 黑白轮流落子
    x1, y1 = (event.x*30 - 15), (event.y*30 - 15)
    x2, y2 = (event.x*30 + 15), (event.y*30 + 15)
    if chess[event.x][event.y] == 0:
        # if color_number % 2 != 0:
        canvas.create_oval(x1, y1, x2, y2, fill="black")
        chess[event.x][event.y] = 1
        color_number = color_number + 1
        gameover(event.x, event.y)
        #  else:
        #     canvas.create_oval(x1, y1, x2, y2, fill="white")
        #     chess[event.x][event.y] = 2
        ai()
    color_number += 1
    print(event)


def ai():
    global xxx, yyy
    global code  #获取棋型
    global chess_color #保存颜色
    for i in range(1, size+1):
        for j in range(1, size + 1):
            if chess[i][j] == 0:
                code = ""
                chess_color = 0
                for x in range(i + 1, size + 1):
                    # 如果向右的第一位置为空就跳出循环
                    if chess[x][j] == 0:
                        break
                    else:
                        if chess_color == 0:  # 这是右边第一颗棋子
                            code += str(chess[x][j])  # 记录它的颜色
                            chess_color = chess[x][j]  # 保存它的颜色
                        else:
                            if chess_color == chess[x][j]:  # 跟第一颗棋子颜色相同
                                code += str(chess[x][j])  # 记录它的颜色
                            else:  # 右边找到一颗不同颜色的棋子
                                code += str(chess[x][j])
                                break
                # 取出对应的权值
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                # 把code，chess_color清空
                code = ""
                chess_color = 0
                # 向左
                for x in range(i - 1, 0, -1):
                    # 如果向左的第一位置为空就跳出循环
                    if chess[x][j] == 0:
                        break
                    else:
                        if chess_color == 0:  # 这是左边第一颗棋子
                            code += str(chess[x][j])  # 记录它的颜色
                            chess_color = chess[x][j]  # 保存它的颜色
                        else:
                            if chess_color == chess[x][j]:  # 跟第一颗棋子颜色相同
                                code += str(chess[x][j])  # 记录它的颜色
                            else:  # 左边找到一颗不同颜色的棋子
                                code += str(chess[x][j])
                                break
                #  取出对应的权值
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                #  把code，chess_color清空
                code = ""
                chess_color = 0
                #  向上
                for y in range(j - 1, 0, -1):
                    #  如果向上的第一位置为空就跳出循环
                    if chess[i][y] == 0:
                        break
                    else:
                        if chess_color == 0:  # 这是上边第一颗棋子
                            code += str(chess[i][y])  # 记录它的颜色
                            chess_color = chess[i][y]  # 保存它的颜色
                        else:
                            if chess_color == chess[i][y]:  # 跟第一颗棋子颜色相同
                                code += str(chess[i][y])  # 记录它的颜色
                            else:  # 上边找到一颗不同颜色的棋子
                                code += str(chess[i][y])
                                break
                #  取出对应的权值
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                #  把code，chess_color清空
                code = ""
                chess_color = 0
                # 向下
                for y in range(j+1, size+1):
                    # 如果向下的第一位置为空就跳出循环
                    if chess[i][y] == 0:
                        break
                    else:
                        if chess_color == 0:  # 这是下边第一颗棋子
                            code += str(chess[i][y])  # 记录它的颜色
                            chess_color = chess[i][y]  # 保存它的颜色
                        else:
                            if chess_color == chess[i][y]:  # 跟第一颗棋子颜色相同
                                code += str(chess[i][y])  # 记录它的颜色
                            else:  # 下边找到一颗不同颜色的棋子
                                code += str(chess[i][y])
                                break
                # 取出对应的权值
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                # 把code，chess_color清空
                code = ""
                chess_color = 0
                # 向左下
                for x, y in zip(range(i - 1, 0, -1), range(j + 1, size + 1)):
                    # 如果向左下的第一位置为空就跳出循环
                    if chess[x][y] == 0:
                        break
                    else:
                        if chess_color == 0:  # 这是左下边第一颗棋子
                            code += str(chess[x][y])  # 记录它的颜色
                            chess_color = chess[x][y]  # 保存它的颜色
                        else:
                            if chess_color == chess[x][y]:  # 跟第一颗棋子颜色相同
                                code += str(chess[x][y])  # 记录它的颜色
                            else:  # 左下找到一颗不同颜色的棋子
                                code += str(chess[x][y])
                                break
                # 取出对应的权值
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                # 把code，chess_color清空
                code = ""
                chess_color = 0
                # 向右上
                for x, y in zip(range(i + 1, size+1), range(j - 1, 0, -1)):
                    # 如果向右上的第一位置为空就跳出循环
                    if chess[x][y] == 0:
                        break
                    else:
                        if chess_color == 0:  # 这是右上边第一颗棋子
                            code += str(chess[x][y])  # 记录它的颜色
                            chess_color = chess[x][y]  # 保存它的颜色
                        else:
                            if chess_color == chess[x][y]:  # 跟第一颗棋子颜色相同
                                code += str(chess[x][y])  # 记录它的颜色
                            else:  # 右上找到一颗不同颜色的棋子
                                code += str(chess[x][y])
                                break
                # 取出对应的权值
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                # 把code，chess_color清空
                code = ""
                chess_color = 0
                # 向左上
                for x, y in zip(range(i - 1, 0, -1), range(j - 1, 0, -1)):
                    # 如果向左上的第一位置为空就跳出循环
                    if chess[x][y] == 0:
                        break
                    else:
                        if chess_color == 0:  # 这是左
                            # 上边第一颗棋子
                            code += str(chess[x][y])  # 记录它的颜色
                            chess_color = chess[x][y]  # 保存它的颜色
                        else:
                            if chess_color == chess[x][y]:  # 跟第一颗棋子颜色相同
                                code += str(chess[x][y])  # 记录它的颜色
                            else:  # 左上找到一颗不同颜色的棋子
                                code += str(chess[x][y])
                                break
                # 取出对应的权值
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                # 把code，chess_color清空
                code = ""
                chess_color = 0
                # 向右下
                for x, y in zip(range(i+1, size+1), range(j+1, size+1)):
                    # 如果向右下的第一位置为空就跳出循环
                    if chess[x][y] == 0:
                        break
                    else:
                        if chess_color == 0:  # 这是右下
                            # 上边第一颗棋子
                            code += str(chess[x][y])  # 记录它的颜色
                            chess_color = chess[x][y]  # 保存它的颜色
                        else:
                            if chess_color == chess[x][y]:  # 跟第一颗棋子颜色相同
                                code += str(chess[x][y])  # 记录它的颜色
                            else:  # 右下找到一颗不同颜色的棋子
                                code += str(chess[x][y])
                                break
                # 取出对应的权值
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                # 把code，chess_color清空
                code = ""
                chess_color = 0
    mymax = 0
    for a in range(1, size+1):
        for b in range(1, size + 1):
            if chess_Value[a][b] > mymax and chess[a][b] == 0:
                mymax = chess_Value[a][b]
                xxx = a
                yyy = b
    chess[xxx][yyy] = 2
    canvas.create_oval(xxx*30-15, yyy*30-15, xxx*30+15, yyy*30+15, fill="white")
    gameover(xxx, yyy)


#   判断输赢的方法
def gameover(xx, yy):

    count = 0
    for i in range(xx + 1, 17):
        if chess[i][yy] == chess[xx][yy]:
            count += 1
        else:
            break
    for i in range(xx, 0, -1):
        if chess[i][yy] == chess[xx][yy]:
            count += 1
        else:
            break
    if count == 5:
        tkinter.messagebox.showinfo("", "Game over")
    count = 0

    for i in range(yy + 1, 17):
        if chess[xx][i] == chess[xx][yy]:
            count += 1
        else:
            break
    for i in range(yy, 0, -1):
        if chess[xx][i] == chess[xx][yy]:
            count += 1
        else:
            break
    if count == 5:
        tkinter.messagebox.showinfo("", "Game over")
    count = 0

    for i, j in zip(range(xx+1, 17), range(yy+1, 17)):
        if chess[i][j] == chess[xx][yy]:
            count += 1
        else:
            break
    for i, j in zip(range(xx, 0, -1), range(yy, 0, -1)):
        if chess[i][j] == chess[xx][yy]:
            count += 1
        else:
            break
    if count == 5:
        tkinter.messagebox.showinfo("", "Game over")
    count = 0

    for i, j in zip(range(xx - 1, 0, -1), range(yy + 1, 17)):
        if chess[i][j] == chess[xx][yy]:
            count += 1
        else:
            break
    for i, j in zip(range(xx, 17), range(yy, 0, -1)):
        if chess[i][j] == chess[xx][yy]:
            count += 1
        else:
            break
    if count == 5:
        tkinter.messagebox.showinfo("", "Game over")
    count = 0

# 创建窗体
print(paint)
tk = Tk()
tk.title("五子棋")
tk.geometry("510x510")
#  窗体上加画布
canvas = Canvas(tk, width=500, height=500)
canvas.pack(expand=YES, fill=BOTH)
m = 0
#  给画布加监听
canvas.bind("<Button-1>", paint)

# canvas.create_line(0,0,0,450,width=6)
#  画棋盘
for num in range(1, 17):
    canvas.create_line(num*30, 30, num*30, 480, width=2)
for num in range(1, 17):
    canvas.create_line(30, num*30, 480, num*30, width=2)
tk.mainloop()