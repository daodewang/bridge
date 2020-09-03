import matplotlib.pyplot as plt
import pandas as pd
import json


def draw_data(brfiles, ebfiles, gt):
    plt.figure(figsize=(10, 5))  # 设置画布的尺寸
    plt.title(f'Removal Impact in the {gt}', fontsize=20)  # 标题，并设定字号大小
    plt.xlabel(u'Round', fontsize=14)  # 设置x轴，并设定字号大小
    plt.ylabel(u'Normalized GCC Size', fontsize=14)  # 设置y轴，并设定字号大小

    #

    colors = ["r", "g", "b"]
    i = 0
    for file in brfiles:
        with open(gt+file+'.txt', 'r', encoding='utf-8') as f:
            print(file)
            len_of_mcc = json.load(f)
            m = len(len_of_mcc)
            x = [e/m for e in range(m)]

            # color：颜色，linewidth：线宽，linestyle：线条类型，label：图例，marker：数据点的类型
            plt.plot(x, len_of_mcc, color=colors[i], linewidth=1, linestyle='-', label=file)
            i = i+1

    i = 0
    colors = ["r", "g", "b"]
    for file in ebfiles:
        with open(gt+file+'.txt', 'r', encoding='utf-8') as f:
            print(file)
            len_of_mcc = json.load(f)
            m = len(len_of_mcc)
            x = [e / m for e in range(m)]

            # color：颜色，linewidth：线宽，linestyle：线条类型，label：图例，marker：数据点的类型
            plt.plot(x, len_of_mcc, color=colors[i], linewidth=1, linestyle='--', label=file)
            i = i+1

    plt.legend(loc=1)  # 图例展示位置，数字代表第几象限
    plt.show()  # 显示图像
    plt.savefig(f'{gt}-removal.png')
    plt.savefig(f'{gt}-removal.eps')


if __name__ == '__main__':
    brf = '-br-'
    ebf = '-eb-'
    brfiles = [brf+'1000', brf+'2000', brf+'4000']
    ebfiles = [ebf+'1000', ebf+'2000', ebf+'4000']

    graphtype = 'ER'

    draw_data(brfiles, ebfiles, graphtype)
    draw_data(brfiles, ebfiles, graphtype)
