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
# ju_court = os.listdir(folderPath)[2]  # 查詢資料夾下的所有檔案名稱
# ju_Path = f'{folderPath}/{ju_court}'  # 簡化路徑
folderList = os.listdir(folderPath)
# print(f"list : {folderList}")
pIndex = 0
for p in folderList:
    print(p, ':', pIndex)
    pIndex += 1
fp = int(input("\nChoose work folder : "))
folder = folderList[fp]  # 檔案名：judge案由分類
print(f'你選擇的是：{folder}\n')
folderName = '所有地院10年_rawdata'
version = '_ver_2'

# 篩選去掉不要的之後的list
cleanedJudge = []

# 設定篩選不要的判決書的關鍵字
nTitle = '裁定'
nCont_1 = '不受理'  # '公訴不受理'
nCont_2 = '駁回'  # '上訴駁回'
nCont_3 = '共同犯'  # 多人犯罪
nCont_4 = '易服勞役'
nCrime = '無罪'

# 裁判案由分類 list
tlist_01 = []
tName_01 = '重傷害'
title_01 = ['重傷害', '重傷害等', '家暴重傷害等', '家暴重傷害', '因重傷害案附帶民訴等',
            '因重傷害案附帶民訴', '家庭暴力防治法之重傷害', '因重傷害附帶民訴', '因重傷害案提起附帶民事訴訟', '家暴之重傷害']
tlist_02 = []
tName_02 = '重傷害未遂'
title_02 = ['重傷害未遂', '重傷害未遂等', '重傷害未遂附帶民訴']
tlist_03 = []
tName_03 = '重傷害致死'
title_03 = ['重傷害致死附帶民訴', '重傷害致死', '重傷害致死等']
tlist_04 = []
tName_04 = '教唆傷害'
title_04 = ['教唆傷害']
tlist_05 = []
tName_05 = '傷害'
title_05 = ['傷害等', '傷害', '家暴傷害', '家暴傷害等', '因傷害案附帶民訴', '家庭暴力罪之傷害', '家庭暴力罪之傷害附帶民訴', '因傷害案附帶民訴等', '家庭暴力罪之傷害等', '家庭暴力罪之傷害附帶民訴等', '家庭暴力防治法之傷害等', '家庭暴力防治法之傷害', '違反家庭暴力防治法之傷害', '家庭暴力之傷害',
            '家暴傷害罪', '家暴傷害罪等', '因傷害附帶民訴', '因家暴傷害附帶民訴', '因家庭暴力之傷害案件提起附帶', '因家庭暴力之傷害案提起附帶民事訴訟', '因傷害案提起附帶民事訴訟', '家庭暴力之傷害等', '家庭暴力事件之傷害', '傷害（少連偵）', '傷害（少連偵）等', '傷害（調少連偵）', '傷害等（少連偵）', '傷害聲請羈押等']
tlist_06 = []
tName_06 = '傷害直系血親尊親屬'
title_06 = ['傷害直系血親尊親屬附帶民訴', '傷害直系血親尊親屬等', '傷害直系血親尊親屬', '傷害尊親屬', '傷害尊親屬等', '家暴傷害直系血親尊親屬',
            '家暴傷害直系血親尊親屬等', '傷害直系血親尊親屬罪等', '傷害尊親屬罪', '傷害尊親屬罪等', '傷害直系尊親屬', '傷害直系尊親屬等']
tlist_07 = []
tName_07 = '傷害直系血親尊親屬致死'
title_07 = ['傷害直系血親尊親屬致死']
tlist_08 = []
tName_08 = '傷害直系血親尊親屬致重傷害'
title_08 = ['重傷害尊親屬罪']
tlist_09 = []
tName_09 = '傷害致死'
title_09 = ['傷害致死', '傷害致死等', '傷害致死附帶民訴', '因傷害致死附帶民訴等', '傷害致死附帶民訴等', '因傷害致死附帶民訴', '家庭暴力防治法之傷害致死',
            '家庭暴力防制法之傷害致死', '家暴傷害致死等', '家暴傷害致死', '因傷害致死案提起附帶民事訴訟', '家庭暴力罪之傷害致死', '傷害致死聲請羈押等']
tlist_10 = []
tName_10 = '傷害致重傷害'
title_10 = ['傷害致重傷', '傷害致重傷附帶民訴', '傷害致重傷等',
            '傷害致重傷害', '傷害致重傷害等', '家暴傷害致重傷', '家庭暴力罪之傷害致重傷']
tlist_11 = []
tName_11 = '過失致重傷害'
title_11 = ['過失重傷害', '因過失重傷害案附帶民訴', '過失致重傷害', '業務過失重傷害', '過失重傷害附帶民訴', '業務過失重傷害附帶民訴', '因過失重傷害案附帶民訴等', '過失重傷害等', '業務過失重傷害等', '因業務過失重傷害', '業務過失致重傷害',
            '過失致重傷害等', '業務過失致重傷害等', '因過失致重傷害附帶民訴', '因業務過失重傷害案提起附帶民', '因業務過失重傷害案提起附帶民事訴訟', '因過失重傷害案提起附帶民事訴', '因過失重傷害案提起附帶民事訴訟', '過失傷害致重傷', '過失傷害致重傷等', '過失傷害致重傷害']
tlist_12 = []
tName_12 = '過失傷害'
title_12 = ['過失傷害', '過失傷害等', '因過失傷害案附帶民訴', '業務過失傷害', '業務過失傷害等', '因業務過失傷害案附帶民訴', '因過失傷害案附帶民訴等', '因業務過失傷害案附帶民訴等',
            '家庭暴力防制法之過失傷害', '家庭暴力防治法之過失傷害', '家暴過失傷害', '因過失傷害附帶民訴', '因業務過失傷害案提起附帶民事訴訟', '因過失傷害案提起附帶民事訴訟', '義務過失傷害']

# 將所有地院合併,並篩掉不需要的資料(裁定、不受理等等)


def combineAllCourt():

    rfolderList = os.listdir(f'{folderPath}/{folder}')
    # print(f"{folderList}")
    rpIndex = 0
    for rp in rfolderList:
        print(rp, ':', rpIndex)
        rpIndex += 1
    rfp = int(input("\n選擇放置所有 地院rawdata 的資料夾 : "))
    rfolder = rfolderList[rfp]
    print(f'你選擇的是：{rfolder}\n')
    # 找到所有json檔案
    rData = f'{folderPath}/{folder}/{rfolder}'
    rDataList = os.listdir(rData)
    # print(rDataList)
    # print(rData)

    typeErrorCount = 0     # 設定不符預期格式計數器
    resultErrorCount = 0   # 設定判決結果有誤計數器
    # 一份一份json開啟
    for j in rDataList:
        with open(f'{rData}/{j}', 'r', encoding='utf-8-sig') as js:
            strJs = js.read()
        listJudge = json.loads(strJs)
        print(j)

        for i in range(len(listJudge)):
            if nTitle in listJudge[i]['judge_NO']:
                continue
            elif nCont_1 in listJudge[i]['judge_content']:
                continue
            elif nCont_2 in listJudge[i]['judge_content']:
                continue
            elif nCont_3 in listJudge[i]['judge_content']:
                continue
            elif nCont_4 in listJudge[i]['judge_content']:
                continue
            elif nCrime in listJudge[i]['judge_content']:
                cleanedJudge.append({
                    'judge_court': listJudge[i]['judge_court'],      # 判決法院
                    'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                    'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                    # 地院年度月份的第幾筆
                    'judge_index': listJudge[i]['judge_index'],
                    'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                    'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                    'judge_crime': nCrime,                           # 罪名
                    'judge_result': '零日',                             # 刑責
                    'judge_resultInt': 0                             # 刑責int
                })
            else:
                reg = r'[犯因][\u4E00-\u9FFF]*傷[害]?[\u4E00-\u9FFF]*，處[\u4E00-\u9FFF]*'
                m = re.search(reg, listJudge[i]['judge_content'])

                try:
                    judge_crime = m[0].split('，')[0][1:]
                    judge_result = m[0].split('，')[1][1:]
                    judge_resultInt = word2int(m[0].split('，')[1][1:])

                    if judge_resultInt == 999999:
                        resultErrorCount += 1
                        continue

                    cleanedJudge.append({
                        'judge_court': listJudge[i]['judge_court'],      # 判決法院
                        'judge_year': listJudge[i]['judge_year'],      # 裁判年度
                        'judge_month': listJudge[i]['judge_month'],     # 裁判月份
                        # 地院年度月份的第幾筆
                        'judge_index': listJudge[i]['judge_index'],
                        'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                        # 判決書內文
                        'judge_content': listJudge[i]['judge_content'],
                        'judge_crime': judge_crime,          # 罪名
                        'judge_result': judge_result,        # 刑責
                        # 刑責int
                        'judge_resultInt': judge_resultInt
                    })
                except TypeError as te:

                    typeErrorCount += 1
                    # print(f"{listJudge[i]['judge_court']}_{listJudge[i]['judge_year']}_{listJudge[i]['judge_month']}_{listJudge[i]['judge_index']} : 判決寫法不符預期格式")

    print(f'共有{typeErrorCount}筆判決寫法不符預期格式\n\
    共有{resultErrorCount}筆判決結果有誤\n\
    清整完剩餘{len(cleanedJudge)}筆資料')
    with open(f'{folderPath}/{folder}/{folderName}{version}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(cleanedJudge, ensure_ascii=False))
    pd.DataFrame(cleanedJudge).to_csv(
        f'{folderPath}/{folder}/{folderName}{version}.csv', index=None, encoding="utf-8-sig")


# 刑責中文字轉數字
def word2int(judge_result):
    num = {"零": 0, "壹": 1, "一": 1, "貳": 2, "贰": 2, "二": 2, "參": 3, "参": 3, "叁": 3, "叄": 3, "三": 3, "肆": 4, "四": 4,
           "伍": 5, "五": 5, "陸": 6, "六": 6, "柒": 7, "七": 7, "捌": 8, "八": 8, "玖": 9, "九": 9, "拾": 10, "十": 10, "佰": 100, "百": 100}
    unit = {"年": 365, "月": 30, "日": 1}

    transfer = []
    transfer2 = []
    transfer3 = []
    number = 0
    judge = []
    unitMatch = 0

    # 將每一筆判刑內容中文字逐一取出
    for j in judge_result:
        # 將國字數字和單位轉換成數字list
        if j in num:
            transfer.append(num.get(j))
        elif j in unit:
            transfer.append(j)
            unitMatch += 1
    if unitMatch == 0:
        unitMatch = 999999
        return unitMatch
    # print(f'transfer={transfer}')
    # 將transfer list中數字做運算
    for n in transfer:
        if n in unit:
            transfer2.append(number)
            transfer2.append(n)
            number = 0
        elif n == 100:
            if number == 0:
                number += 100
            else:
                number *= 100
        elif n != 10:
            number += n
        elif n == 10:
            if number == 0:
                number += 10
            else:
                number *= 10
    # print(f'transfer2={transfer2}')
    # 將數字和單位做運算
    for m in transfer2:
        if m in unit:
            number *= unit[m]
            transfer3.append(number)
            number = 0
        else:
            number += m
    # print(f'transfer3={transfer3}')
    # 將刑期加總並加到csv中
    number = sum(transfer3)
    return number
    # print(f'number={number}',type(number))
    # judge.append(number)
    # print(judge)


# 分類判決案由
def judgeClassify():
    cfolderList = os.listdir(f'{folderPath}/{folder}')
    # print(f"{cfolderList}")
    cpIndex = 0
    for cp in cfolderList:
        print(cp, ':', cpIndex)
        cpIndex += 1
    cfp = int(input("\n選擇要分類的rawdata.json : "))
    cfolder = cfolderList[cfp]
    print(f'你選擇的是：{cfolder}\n')
    # print(cfolder)
    # print(f'{folderPath}/{folder}/{cfolder}')  # 檢查完整路徑是否正確

    with open(f'{folderPath}/{folder}/{cfolder}', 'r', encoding='utf-8') as js:
        strJs = js.read()
    listJudge = json.loads(strJs)  # <class 'list'>

    for i in range(len(listJudge)):
        if listJudge[i]['judge_title'] in title_01:
            tlist_01.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_02:
            tlist_02.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_03:
            tlist_03.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })

        elif listJudge[i]['judge_title'] in title_04:
            tlist_04.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_05:
            tlist_05.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_06:
            tlist_06.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_07:
            tlist_07.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_08:
            tlist_08.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_09:
            tlist_09.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_10:
            tlist_10.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_11:
            tlist_11.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        elif listJudge[i]['judge_title'] in title_12:
            tlist_12.append({
                'judge_court': listJudge[i]['judge_court'],      # 判決法院
                'judge_year': listJudge[i]['judge_year'],         # 裁判年度
                'judge_month': listJudge[i]['judge_month'],       # 裁判月份
                'judge_index': listJudge[i]['judge_index'],      # 地院年度月份的第幾筆
                'judge_title': listJudge[i]['judge_title'],      # 裁判案由
                'judge_content': listJudge[i]['judge_content'],   # 判決書內文
                'judge_crime': listJudge[i]['judge_crime'],      # 罪名
                'judge_result': listJudge[i]['judge_result']      # 刑責
            })
        else:
            print('Title 不在列表中')


def listSave():
    cFolderPath = f'{folderPath}/{folder}/地方法院_10年_分類資料'
    if not os.path.exists(cFolderPath):
        os.makedirs(cFolderPath)

    with open(f'{cFolderPath}/{tName_01}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_01, ensure_ascii=False))
    pd.DataFrame(tlist_01).to_csv(
        f'{cFolderPath}/{tName_01}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_02}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_02, ensure_ascii=False))
    pd.DataFrame(tlist_02).to_csv(
        f'{cFolderPath}/{tName_02}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_03}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_03, ensure_ascii=False))
    pd.DataFrame(tlist_03).to_csv(
        f'{cFolderPath}/{tName_03}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_04}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_04, ensure_ascii=False))
    pd.DataFrame(tlist_04).to_csv(
        f'{cFolderPath}/{tName_04}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_05}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_05, ensure_ascii=False))
    pd.DataFrame(tlist_05).to_csv(
        f'{cFolderPath}/{tName_05}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_06}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_06, ensure_ascii=False))
    pd.DataFrame(tlist_06).to_csv(
        f'{cFolderPath}/{tName_06}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_07}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_07, ensure_ascii=False))
    pd.DataFrame(tlist_07).to_csv(
        f'{cFolderPath}/{tName_07}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_08}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_08, ensure_ascii=False))
    pd.DataFrame(tlist_08).to_csv(
        f'{cFolderPath}/{tName_08}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_09}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_09, ensure_ascii=False))
    pd.DataFrame(tlist_09).to_csv(
        f'{cFolderPath}/{tName_09}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_10}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_10, ensure_ascii=False))
    pd.DataFrame(tlist_10).to_csv(
        f'{cFolderPath}/{tName_10}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_11}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_11, ensure_ascii=False))
    pd.DataFrame(tlist_11).to_csv(
        f'{cFolderPath}/{tName_11}.csv', index=None, encoding="utf-8-sig")

    with open(f'{cFolderPath}/{tName_12}.json', "a", encoding="utf-8") as js:
        js.write(json.dumps(tlist_12, ensure_ascii=False))
    pd.DataFrame(tlist_12).to_csv(
        f'{cFolderPath}/{tName_12}.csv', index=None, encoding="utf-8-sig")


if __name__ == "__main__":
    startTime = time.time()
    combineAllCourt()
    # judgeClassify()
    # listSave()
    print(f"總花費時間 : {((time.time() - startTime)/60):.2f} 分鐘")
