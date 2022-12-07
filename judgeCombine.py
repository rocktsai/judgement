# 整理 json 使用的工具
import json
import csv

# 執行 command 的時候用的
import os

# 強制等待 (執行期間休息一下)
from time import sleep
import time

# 子處理程序，用來取代 os.system 的功能
import subprocess

import pandas as pd
import numpy as np

# 匯入 正規表達式
import re

# 建立儲存文件的資料夾
folderPath = '/Users/allentsai/python_web_scraping-master/judgement_file'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)
# ju_court = os.listdir(folderPath)[2]  # 查詢資料夾下的所有檔案名稱
# ju_Path = f'{folderPath}/{ju_court}'  # 簡化路徑
# ju_court = os.listdir(folderPath)
# print(f"{ju_court}")
# print(ju_Path)

folderList = os.listdir(folderPath)  # 查詢資料夾下的所有檔案名稱
pIndex = 0   # 檔案順序 index 設定
for p in folderList:
    print(p, ':', pIndex)
    pIndex += 1
fp = int(input("選取要合併的資料夾 : "))  # 選取資料夾
ju_court = folderList[fp]
ju_Path = f'{folderPath}/{ju_court}'  # 簡化路徑
# print(ju_Path)

# 從哪一個年度開始往回抓
startYear = 111

listJudgeContent = []
errorList = []


def contentToCsv(year, month):

    # 會有csv檔是空的情況,因此要用try/except接錯誤訊息
    try:
        # pd.read_csv(f'{ju_Path}/{ju_court}_{year}年_{month}月.csv')
        csv = pd.read_csv(
            f'{ju_Path}/{ju_court}_{year}年_{month}月.csv', encoding='utf-8-sig')
        # print(len(csv))
        # print(type(csv))
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


# 透過json合併csv檔案 , 使用 python split 來 clean 判決書 並貼進 csv 裡
def combine_split(year, month):

    with open(f"{ju_Path}/{ju_court}_{year}年_{month}月.json", "r", encoding="utf-8") as js:
        strJs = js.read()
    listJudge = json.loads(strJs)

    txtObj = ''
    content = ''
    main = '主文'
    clerk = '書記官'

    for i in range(0, len(listJudge)):
        a = i + 1

        with open(f'{ju_Path}/判決書/{ju_court}_{year}年_{month}月_{a}.txt', 'r', encoding='utf-8') as txt:
            txtObj = txt.read()

            # 去掉空白、全形空白、換行...等
        txt_clean = ''.join(txtObj.split())

        try:
            # 先判斷是否有主文
            if main in txt_clean:

                # 依照主文 split
                # txt_main = <class 'str'>
                txt_main = ''.join(txt_clean.split(main)[1:])

                # 依照書記官做結尾切割 , 先切成 list
                txt_clerk = txt_main.split(clerk)  # txt_clerk = <class 'list'>

                # 切完的 list 轉 str
                txt_cont = ''.join(txt_clerk[0])  # 主文～書記官
                clerkName = ''.join(txt_clerk[1])[0:3]  # 切出書記官名字

                content = main + ':' + txt_cont    # + clerk + ':' + clerkName + '。' # 加書記官

            else:
                content = txt_clean

            listJudgeContent.append({
                # list 的第幾筆
                'judge_index': listJudge[i]['judge_index'],
                'judge_year': year,                                   # 裁判年度
                'judge_month': listJudge[i]['judge_month'],              # 裁判月份
                'judge_title': listJudge[i]['judge_title'],  # 裁判案由
                'judge_NO': listJudge[i]['judge_NO'],  # 裁判字號
                'judge_court': listJudge[i]['judge_court'],           # 判決法院
                'judge_link': listJudge[i]['judge_link'],      # 判決書連結
                'judge_content': content                       # 判決書內文
            })
            print(f'已合併完：{ju_court}_{year}年_{month}月_{a}.txt')

        except IndexError as IE:

            listJudgeContent.append({
                # list 的第幾筆
                'judge_index': listJudge[i]['judge_index'],
                'judge_year': year,                                   # 裁判年度
                'judge_month': listJudge[i]['judge_month'],              # 裁判月份
                'judge_title': listJudge[i]['judge_title'],  # 裁判案由
                'judge_NO': listJudge[i]['judge_NO'],  # 裁判字號
                'judge_court': listJudge[i]['judge_court'],           # 判決法院
                'judge_link': listJudge[i]['judge_link'],      # 判決書連結
                'judge_content': txt_clean                      # 判決書內文
            })

            errorList.append({
                'error_txt': f'{ju_court}_{year}年_{month}月_{a}.txt',
                'error_info': IE
            })

    # print(len(listJudgeContent))
    # print(listJudgeContent)


# ！！！小心！！！ 全部合併可能會變成大數據 , 打不開
def combineAll_split():

    for d in range(10):
        year = startYear - d
        for month in range(1, 13):
            combine_split(year, month)
        print(f"完成建立{year}年度")


def listToFile():

    with open(f"{ju_Path}/{ju_court}_10年rawdata.json", "a", encoding="utf-8") as js:
        js.write(json.dumps(listJudgeContent, ensure_ascii=False))
    pd.DataFrame(listJudgeContent).to_csv(
        f"{ju_Path}/{ju_court}_10年rawdata.csv", index=None, encoding="utf-8-sig")

    pd.DataFrame(errorList).to_csv(
        f"{ju_Path}/{ju_court}_ErrorList.csv", index=None, encoding="utf-8-sig")


if __name__ == "__main__":
    startTime = time.time()
    # contentToCsv(102, 1)
    # contentToCsv_loop()
    combineAll_split()
    listToFile()
    print(f"總花費時間 : {((time.time() - startTime)/60):.2f} 分鐘")
