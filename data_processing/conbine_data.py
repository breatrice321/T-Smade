# -*- coding: utf-8 -*-

import os
import pandas as pd

# combine 2 files
# dir_spectre = "../datasets/meltdown/attack/2/"#设置工作路径
dir_spectre ="../datasets/configuration_3/excel/meltdown_tmp/8/"
# dir_no_spectre = "../datasets/meltdown/normal/2/"
dir_no_spectre = "../datasets/configuration_3/excel/normal/8/"

spectre = os.listdir(dir_spectre)
no_spectre = os.listdir(dir_no_spectre)

t = dict(zip(spectre, no_spectre))
for spectre_i, no_spectre_i in t.items():
    excel_list = []
    if spectre_i == no_spectre_i:
        spectre_j = pd.read_excel(dir_spectre+spectre_i)
        no_spectre_j = pd.read_excel(dir_no_spectre + no_spectre_i)
        excel_list.append(spectre_j)
        excel_list.append(no_spectre_j)
        # print(excel_list)
        result = pd.concat(excel_list)
        # 查看合并后的数据
        result.head()
        result.shape
        result.to_excel('../datasets/configuration_3/excel/meltdown_tmp_and_normal/8/'+spectre_i, index=False)
        # result.to_excel('../datasets/meltdown/attack_and_normal/2/' + spectre_i, index=False)
        # result.to_excel('../datasets/train/' + spectre_i, index=False)


# # combine 1 file
#
# # path of the folder
# # path = r'../datasets/evasive-spectre/data/2/'
# path = r'../datasets/spectrev1/test/labortory/new_test/lab_2/spectre_and_no_spectre/8/'
#
# # reading all the excel files
# filenames = os.listdir(path)
#
# # initializing empty data frame
# finalexcelsheet = pd.DataFrame()
#
# # to iterate excel file one by one
# # inside the folder
# for file in filenames:
#     # combining multiple excel worksheets
#     # into single data frames
#     df = pd.concat(pd.read_excel(
#         path+file, sheet_name=None), ignore_index=True, sort=False)
#
#     # appending excel files one by one
#     finalexcelsheet = finalexcelsheet.append(
#         df, ignore_index=True)
#
#
# # save data
# finalexcelsheet.to_excel(r'../datasets/spectrev1/test/labortory/new_test/lab_2/spectre_and_no_spectre/combine/8_app.xlsx', index=False)