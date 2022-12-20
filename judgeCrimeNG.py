# 整理 json 使用的工具
import csv
import json
# 執行 command 的時候用的
import os
# 匯入 正規表達式
import re
# 子處理程序，用來取代 os.system 的功能
import subprocess
import time
from pathlib import Path
# 強制等待 (執行期間休息一下)
from time import sleep

import numpy as np
import pandas as pd

# 建立儲存文件的資料夾
# folderPath = '/Users/allentsai/python_web_scraping-master/judgement_file'
folderPath = Path(__file__).resolve().parent/'judgement_file'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)
folderList = os.listdir(folderPath)
pIndex = 0
for p in folderList:
    print(p, ':', pIndex)
    pIndex += 1
fp = int(input("\nChoose work folder : "))
folder = folderList[fp]  # 檔案名：judge案由分類
print(f'你選擇的是：{folder}\n')
folderName = 'Crime_NO_Match'

listCrime = []


def sortCrimeNG():
    sfolderList = os.listdir(f'{folderPath}/{folder}')
    spIndex = 0
    for sp in sfolderList:
        print(sp, ':', spIndex)
        spIndex += 1
    sfp = int(input("\n選擇要篩選罪刑預測錯誤的.json : "))
    sfolder = sfolderList[sfp]
    print(f'你選擇的是：{sfolder}\n')

    with open(f'{folderPath}/{folder}/{sfolder}', 'r', encoding='utf-8') as jss:
        strJss = jss.read()
    listFeature = json.loads(strJss)

    sdIndex = 0
    for sd in sfolderList:
        print(sd, ':', sdIndex)
        sdIndex += 1
    sfd = int(input("\n選擇要篩選罪刑預測錯誤的.csv : "))
    sfolderd = sfolderList[sfd]
    print(f'你選擇的是：{sfolderd}\n')

    dfFeature = pd.read_csv(
        f'{folderPath}/{folder}/{sfolderd}', 'r', encoding='utf-8')

    for i in range(len(listFeature)):
        if listFeature[i]['judge_crimePred'] == '無罪' or listFeature[i]['judge_crime'] == '無罪':
            listCrime.append(listFeature[i])
            # listCrime.append({
            #     'judge_court': listFeature[i]['judge_court'],      # 判決法院
            #     'judge_year': listFeature[i]['judge_year'],         # 裁判年度
            #     'judge_month': listFeature[i]['judge_month'],       # 裁判月份
            #     'judge_index': listFeature[i]['judge_index'],     # 地院年度月份的第幾筆
            #     'judge_title': listFeature[i]['judge_title'],      # 裁判案由
            #     'judge_crimePred': listFeature[i]['judge_crimePred'],  # 罪刑預測
            #     'judge_crime': listFeature[i]['judge_crime'],          # 罪名
            #     'judge_result': listFeature[i]['judge_result'],        # 刑責
            #     'judge_resultInt': listFeature[i]['judge_resultInt']  # 刑責int
            # })

    pd.DataFrame(listCrime).to_csv(
        f'{folderPath}/{folder}/{folderName}.csv', encoding='utf-8')


if __name__ == "__main__":
    startTime = time.time()
    sortCrimeNG()
    print(f"總花費時間 : {((time.time() - startTime)/60):.2f} 分鐘")
