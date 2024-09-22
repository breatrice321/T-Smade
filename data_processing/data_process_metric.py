import math
import os
import time

import numpy as np
import pandas as pd
import openpyxl


f_path = r'../raw_data/'
name = os.listdir(f_path)
for name_i in name:
    with open(f_path + "/" + name_i) as f:
        data = np.loadtxt(f, dtype=str, skiprows=3, usecols=(1, 2))

        # 将数组按照每五行一组进行分组
        groups = [data[i:i + 5] for i in range(0, len(data), 5)]

        # 创建一个空列表，用于存储处理后的数据
        filtered_data = []

        # 循环遍历每一组数据
        for group in groups:
            if '<not' not in group[:, 0] and group[0, 0] != '0' and group[3, 0] != '0':
                filtered_data.append(group)

        # 将处理后的数据合并成一个新的数组
        data = np.vstack(filtered_data)

        rows, columns = data.shape

        branches = []
        branch_misses = []
        branch_miss_rate = []
        LLC = []
        LLC_misses = []
        LLC_miss_rate = []
        interrupts = []
        LLC_branch = []
        type = []

        for i in range(rows):
            if data[i][1] == "branches":
                a = float(data[i][0].replace(",", ""))
                if a == 0.0:
                    continue
                branches.append(a)
            if data[i][1] == "branch-misses":
                b = float(data[i][0].replace(",", ""))
                branch_misses.append(b)
            if data[i][1] == "r4f2e":
                c = float(data[i][0].replace(",", ""))
                LLC.append(c)
            if data[i][1] == "r412e":
                d = float(data[i][0].replace(",", ""))
                LLC_misses.append(d)
            if i % 5 == 3:
                e = b / a
                branch_miss_rate.append(e)
                f = d / c
                LLC_miss_rate.append(f)
                h = f / e
                LLC_branch.append(math.pow(h, 1.05))
                # LLC_branch.append(h)
                type.append(1)

        branches = np.array(branches)
        branches = branches.reshape(-1, 1)
        # print(branches)
        branch_misses = np.array(branch_misses)
        branch_misses = branch_misses.reshape(-1, 1)
        # print(branch_misses)
        branch_miss_rate = np.array(branch_miss_rate)
        branch_miss_rate = branch_miss_rate.reshape(-1, 1)
        # print(branch_miss_rate)
        LLC = np.array(LLC)
        LLC = LLC.reshape(-1, 1)
        # print(LLC)
        LLC_misses = np.array(LLC_misses)
        LLC_misses = LLC_misses.reshape(-1, 1)
        # print(LLC_misses)
        LLC_miss_rate = np.array(LLC_miss_rate)
        LLC_miss_rate = LLC_miss_rate.reshape(-1, 1)
        # print(LLC_miss_rate)
        LLC_branch = np.array(LLC_branch)
        LLC_branch = LLC_branch.reshape(-1, 1)
        type = np.array(type)
        type = type.reshape(-1, 1)
        # print(type)


        data = np.concatenate(
            (branches, branch_misses, LLC, LLC_misses, branch_miss_rate, LLC_miss_rate, LLC_branch, type),
            axis=1)
        dataFrame = pd.DataFrame(data, columns=['branches', 'branch misses', 'LLC', 'LLC misses', 'branch miss rate',
                                                'LLC miss rate', 'LLC miss rate / branch miss rate', 'type'])

        mypath = "../dataset/noise_6/" + name_i + ".xlsx"

        # 新建空白工作簿
        mybook = openpyxl.Workbook()
        # 根据参数(mypath)保存空白工作簿(mybook),即创建保存多个空白的excel文件
        mybook.save(mypath)

        with pd.ExcelWriter(mypath) as writer:
            dataFrame.to_excel(writer, sheet_name='page1', float_format='%.6f', index=False)


