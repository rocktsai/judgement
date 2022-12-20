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
ju_court = os.listdir(folderPath)[2]  # 查詢資料夾下的所有檔案名稱
ju_Path = f'{folderPath}/{ju_court}'  # 簡化路徑
# ju_court = os.listdir(folderPath)
# print(f"{ju_court}")

# 從哪一個年度開始往回抓
startYear = 111

listJudgeContent = []


def contentToCsv(year, month):

    # 會有csv檔是空的情況,因此要用try/except接錯誤訊息
    try:
        pd.read_csv(f'{ju_Path}/{ju_court}_{year}年_{month}月.csv')
        csv = pd.read_csv(
            f'{ju_Path}/{ju_court}_{year}年_{month}月.csv', encoding='utf-8-sig')
        # print(len(csv))
        print(type(csv))
        list = []
        for i in range(1, len(csv)+1):
            with open(f'{ju_Path}/判決書/{ju_court}_{year}年_{month}月_{i}.txt', 'r', encoding='utf-8') as txt:
                txtObj = txt.read()
                list.append(txtObj)
        # print(list)
        csv['content'] = list
        csv.to_csv(
            f'{ju_Path}/{ju_court}_{year}年_{month}月.csv', encoding='utf-8-sig', index=False)

    except pd.errors.EmptyDataError:
        print(f'{ju_court}_{year}年_{month}月.csv is "EMPTY" !!')


def contentToCsv_loop():

    for d in range(10):
        year = startYear - d
        for month in range(1, 13):
            contentToCsv(year, month)
        print(f"完成建立{year}年度")


# 透過json合併csv檔案 , 使用正則 clean 文本
def combine_re(year, month):

    with open(f"{ju_Path}/{ju_court}_{year}年_{month}月.json", "r", encoding="utf-8") as js:
        strJs = js.read()
    listJudge = json.loads(strJs)
    txtObj = ''
    for i in range(0, len(listJudge)):
        a = i + 1
        with open(f'{ju_Path}/判決書/{ju_court}_{year}年_{month}月_{a}.txt', 'r', encoding='utf-8') as txt:
            txtObj = txt.read()

        # Regular expresion 主  文.........~書記官
        # reg = r'主 [? ]*文(\n.*)*書記官'
        reg = r'主[?  ]*文(\n.*)*書記官'

        m = re.search(reg, txtObj)

        if m != None:
            # content = m[0]
            content = ''.join(m[0].split())
        else:
            # content = txtObj
            content = ''.join(txtObj.split())

        listJudgeContent.append({
            'judge_index': listJudge[i]['judge_index'],            # list 的第幾筆
            'judge_year': year,                                   # 裁判年度
            'judge_month': listJudge[i]['judge_month'],              # 裁判月份
            'judge_title': listJudge[i]['judge_title'],  # 裁判案由
            'judge_NO': listJudge[i]['judge_NO'],  # 裁判字號
            'judge_court': listJudge[i]['judge_court'],           # 判決法院
            'judge_link': listJudge[i]['judge_link'],      # 判決書連結
            'judge_content': content                       # 判決書內文
        })
    print(len(listJudgeContent))
    print(listJudgeContent)


# ！！！小心！！！ 全部合併可能會變成大數據 , 打不開
def combineAll_re():

    for d in range(1):
        year = startYear - d
        for month in range(1, 2):
            combine_re(year, month)
        print(f"完成建立{year}年度")


def listToFile():

    with open(f"{folderPath}/111_{ju_court}.json", "a", encoding="utf-8") as js:
        js.write(json.dumps(listJudgeContent, ensure_ascii=False))
    pd.DataFrame(listJudgeContent).to_csv(
        f"{folderPath}/111_{ju_court}.csv", index=None, encoding="utf-8-sig")


if __name__ == "__main__":
    startTime = time.time()

    # contentToCsv(102, 1)
    # contentToCsv_loop()

    combineAll_re()

    listToFile()

    print(f"總花費時間 : {((time.time() - startTime)/60):.2f} 分鐘")
