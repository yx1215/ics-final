'''
huo_score = [0,10,100,200,9990,100000]
tiao_score= [0, 1, 10, 100, 1000, 10000]
mian_score = [0, 1, 10, 100, 9980, 100000]
mian_tiao_score = [0,0,2,35,700,800]
dead_tiao_score = [0,0,0,0,600,600]
dead_score = [0,0,0,0,0,10000]
punish_score = 6000

huo_score = [0, 0, 120, 720, 4320, 50000]
tiao_score = [0, 0, 120, 720, 720, 0]
mian_score = [0, 0, 0, 0, 720, 50000]
mian_tiao_score = [0, 0, 0, 0, 720, 0]
dead_tiao_score = [0, 0, 0, 0, 720, 0]
dead_score = [0, 0, 0, 0, 0, 50000]
punish_score = 10
'''

huo_score = [0, 0, 120, 720, 4320, 99999]
tiao_score = [0, 0, 120, 720, 720, 0]
mian_score = [0, 0, 0, 0, 720, 99999]
mian_tiao_score = [0, 0, 0, 0, 720, 0]
dead_tiao_score = [0, 0, 0, 0, 720, 0]
dead_score = [0, 0, 0, 0, 0, 99999]
punish_score = 0



def evaluate_line(line):
    item = [[line[0], 1, False]]
    # line[0] is color
    # 1 is the total connected num
    # false if means weakly connected ** **
    index = 0
    for i in range(1, len(line)):
        if line[i] == item[index][0]:
            item[index][1] += 1
        else:
            index += 1
            item.append([line[i], 1, False])
    merge_item = [item[0]]

    # combine weakly connected
    i = 1
    while i < len(item) - 1:
        color, color_num, judge = item[i]
        last_color, last_color_num, judge = item[i - 1]
        after_color, after_color_num, judge = item[i + 1]
        if color == 0 and color_num == 1 and last_color == after_color and last_color != 0 and last_color_num < 4 and after_color_num < 4:
            it = (last_color, last_color_num + after_color_num, True)
            if merge_item[-1][-1] == False:
                # if not weakly connected before, combine the two
                merge_item.pop()
            else:
                # if weakly connected before, insert one thing between them
                merge_item.append([0, 1, False])
            merge_item.append(it)
            i += 2
        else:
            # if no weakly connected
            merge_item.append(item[i])
            i += 1
    if i < len(item):
        # not weakly connected in the end, append the last one
        merge_item.append(item[-1])

    # in advance wrong thing
    #merge_item = [(2, 1, False)] + merge_item + [(2, 1, False)]

    # get the score
    score = {
        "black": [0, 0],
        "white": [0, 0]
    }

    for i in range(1, len(merge_item) - 1):
        color, color_num, flag = merge_item[i]
        last_color, last_color_num, last_flag = merge_item[i - 1]
        after_color, after_color_num, after_flag = merge_item[i + 1]

        if color == 0:
            continue

        color_num = 5 if color_num >= 5 else color_num
        if flag == False and color_num >= 5:
            # win
            score[color][0] += huo_score[color_num]
        elif last_color == after_color == 0:
            if flag == False:
                # huo
                score[color][0] += huo_score[color_num]
                if color_num >= 3:
                    score[color][1] += punish_score + 100

            else:
                # tiao
                score[color][0] += tiao_score[color_num]
                if color_num >= 3:
                    score[color][1] += punish_score
        elif ((last_color == 0 and after_color != color) or (last_color != color and after_color == 0)):
            if flag == False:
                # mian
                score[color][0] += mian_score[color_num]
                if color_num >= 3:
                    score[color][1] += punish_score
            else:
                # miantiao
                score[color][0] += mian_tiao_score[color_num]
                if color_num >= 3:
                    score[color][1] += punish_score
        else:
            if flag == False:
                # dead
                score[color][0] += dead_score[color_num]
            else:
                # dead tiao
                score[color][0] += dead_tiao_score[color_num]
                if color_num >= 3:
                    score[color][1] += punish_score
    return score
