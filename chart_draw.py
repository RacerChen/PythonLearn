import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


def draw_2_axies():
    df = pd.read_csv('C:/Users/CJJ/Desktop/test.csv')
    del df['Unnamed: 0']
    print(df)
    # print(df[0:1])
    # print(df[1:2])
    # print(df.columns)

    # for col in df.columns:
    #     print(col)

    print(df.loc[0].astype(str))  # mean
    print(df.loc[1].astype(str))  # std
    # print(len(df.loc[1]))

    mean = df.loc[0]
    std = df.loc[1]

    for i in range(1, len(df.columns)):
        plt.bar(df.columns[i], mean[i], 1)
    for i in range(1, len(df.columns)):
        plt.scatter(df.columns[i], std[i], 1)
    plt.xlabel('inst')
    plt.ylabel('mean')

    plt.title('Title')
    plt.show()
    plt.close()


def draw_2_axis_2():
    df = pd.read_csv('C:/Users/CJJ/Desktop/test.csv')
    del df['Unnamed: 0']
    cols = df.columns
    mean = df.loc[0]
    std = df.loc[1]
    X = cols[1:len(cols)]
    Y1 = mean[1:len(mean)]
    Y2 = std[1:len(std)]

    fig, ax1 = plt.subplots()
    plt.xticks(rotation=45)

    k = 1.2

    ax1.bar(X, Y1, alpha=0.5, label="mean")
    ax1.set_xlabel("inst")
    ax1.set_ylabel("mean")
    ax1.set_ylim(min(Y1) * k, max(Y2) * k)

    ax2 = ax1.twinx()
    ax2.scatter(X, Y2, label="std")
    ax2.set_ylabel("std")
    ax2.set_ylim(min(Y1) * k, max(Y2) * k)

    fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
    plt.show()
    plt.savefig()


if __name__ == '__main__':
    draw_2_axies()
    draw_2_axis_2()
