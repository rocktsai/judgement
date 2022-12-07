# 操作 browser 的 API
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 處理逾時例外的工具
from selenium.common.exceptions import TimeoutException

# 面對動態網頁，等待某個元素出現的工具，通常與 exptected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait

# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC

# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By

# 加入行為鍊 ActionChain (在 WebDriver 中模擬滑鼠移動、點繫、拖曳、按右鍵出現選單，以及鍵盤輸入文字、按下鍵盤上的按鈕等)
from selenium.webdriver.common.action_chains import ActionChains

# 強制等待 (執行期間休息一下)
from time import sleep
import time

# 整理 json 使用的工具
import json
import csv

# 執行 command 的時候用的
import os

# 子處理程序，用來取代 os.system 的功能
import subprocess

import pandas as pd

# 啟動瀏覽器工具的選項
my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")                #不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")  # 最大化視窗
my_options.add_argument("--incognito")  # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")  # 取消 chrome 推播通知
my_options.add_argument("--lang=zh-TW")  # 設定為正體中文

# 使用 Chrome 的 WebDriver
driver = webdriver.Chrome(
    options=my_options,
    service=Service(ChromeDriverManager().install())
)

# 建立儲存文件的資料夾
folderPath = '/Users/allentsai/python_web_scraping-master/judgement_file'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

# 放置爬取的資料
judgeList = []

# 從哪一個年度開始往回抓
startYear = 105


def conSearch(year):

    for month in range(1, 13):
        # driver.get('https://law.judicial.gov.tw/FJUD/default.aspx')
        driver.get('https://judgment.judicial.gov.tw/FJUD/default.aspx')

        # 更多條件查詢
        conBtm = driver.find_element(
            By.CSS_SELECTOR, 'a.btn.btn-warning').click()

        # 等待一下
        sleep(3)

        # 條件選取
        case_clear = driver.find_element(
            By.CSS_SELECTOR, 'button[type="reset"]').click()    # 重置搜尋條件

        case_type = driver.find_element(
            By.CSS_SELECTOR, 'input[value="M"]').click()        # 案件類別
        sleep(1)
        case_y1 = driver.find_element(
            By.CSS_SELECTOR, 'input#dy1')                       # 裁判期間－起年
        case_y1.send_keys(year)
        case_m1 = driver.find_element(
            By.CSS_SELECTOR, 'input#dm1')                       # 裁判期間－起月
        case_m1.send_keys(month)
        case_d1 = driver.find_element(
            By.CSS_SELECTOR, 'input#dd1')                       # 裁判期間－起日
        case_d1.send_keys('1')
        case_y2 = driver.find_element(
            By.CSS_SELECTOR, 'input#dy2')                       # 裁判期間－迄年
        case_y2.send_keys(year)
        case_m2 = driver.find_element(
            By.CSS_SELECTOR, 'input#dm2')                       # 裁判期間－迄月
        case_m2.send_keys(month)
        case_d2 = driver.find_element(
            By.CSS_SELECTOR, 'input#dd2')                       # 裁判期間－迄日
        case_d2.send_keys('31')
        sleep(1)
        case_title = driver.find_element(
            By.CSS_SELECTOR, 'input#jud_title')                 # 裁判案由
        case_title.send_keys('傷害')
        sleep(3)
        case_place = driver.find_element(                       # 裁判法院
            By.CSS_SELECTOR, 'div.col-sm-3 select#jud_court option[value=CTD]')  # .click()
        ju_court = case_place.get_attribute("innerText")
        case_place.click()
        driver.switch_to.default_content()
        sleep(3)
        case_submit = driver.find_element(
            By.CSS_SELECTOR, 'input.btn.btn-success').click()   # 送出搜尋條件

        print(f"目前搜尋月份 : {month}")
        # 等待一下
        sleep(5)

        # 抓取所有搜尋結果的Link
        getLink(year, month, ju_court)
    print(f"{year}年搜尋結束")


def conSearch_year():
    # 爬取個年度資料
    countYear = 0
    for d in range(1):
        year = startYear - d
        countYear += 1
        print(f"開始搜尋{year}年度")
        conSearch(year)
    print(f"所有年度搜尋完畢，共有{countYear}年的資料")


def getLink(year, month, ju_court):

    iframe = driver.find_element(
        By.CSS_SELECTOR, 'iframe#iframe-data')
    driver.switch_to.frame(iframe)

    count = 1
    judgeList = []   # 放置爬取的資料，每次迴圈清空list
    indexNo = 0
    while True:
        # 先抓搜尋結果下一頁的元素
        nextPage = driver.find_elements(
            By.CSS_SELECTOR, 'a#hlNext')

        # Get Main Link
        ju_link = driver.find_elements(
            By.CSS_SELECTOR, 'table#jud a.hlTitle_scroll')

        ju_title = driver.find_elements(
            By.CSS_SELECTOR, 'table#jud td[width="30%"]')

        # 建立判決書資料集
        # 判決書column：判決書日期、判決結果、案由、法院、傷害類型、犯後態度、前科、法條、是否簡易判決、心智狀態性別、年紀、教育程度、社經地位

        for j in range(len(ju_link)):
            # print(ju_title[j].get_attribute("innerText"))
            # print(ju_link[j].get_attribute("href"))
            indexNo += 1
            judgeList.append({
                'judge_index': indexNo,            # list 的第幾筆
                'judge_month': month,              # 判決書日期，目前只有月份
                'judge_title': ju_title[j].get_attribute("innerText"),  # 裁判案由
                'judge_NO': ju_link[j].get_attribute("innerText"),  # 裁判字號
                'judge_court': ju_court,           # 判決法院
                'judge_link': ju_link[j].get_attribute("href")    # 判決書連結
            })

        if nextPage != []:
            nextPage[0].click()
            count += 1
            print(f"進入第{count}頁")
            sleep(3)
        else:
            print("已是最後一頁")
            break
    print(f"{year}年{month}月共有{indexNo}筆資料，已收集完成。")

    # 建立法院子目錄
    ju_Path = f'{folderPath}/{ju_court}'
    if not os.path.exists(ju_Path):
        os.makedirs(ju_Path)

    # 建立判決書 json 檔
    with open(f"{ju_Path}/{ju_court}_{year}年_{month}月.json", "w", encoding="utf-8") as js:
        js.write(json.dumps(judgeList, ensure_ascii=False))
    # 建立判決書 csv 檔
    pd.DataFrame(judgeList).to_csv(
        f"{ju_Path}/{ju_court}_{year}年_{month}月.csv", index=None)


# 走訪各連結抓判決書內文
def getJudgeContent():

    # ju_court = os.listdir(folderPath)[1]  # 查詢資料夾下的所有檔案名稱
    # ju_Path = f'{folderPath}/{ju_court}'  # 簡化路徑
    # # print(f"{ju_Path}")

    folderList = os.listdir(folderPath)  # 查詢資料夾下的所有檔案名稱
    pIndex = 0   # 檔案順序 index 設定
    for p in folderList:
        print(p, ':', pIndex)
        pIndex += 1
    fp = int(input("Choose folder : "))  # 選取資料夾
    ju_court = folderList[fp]
    ju_Path = f'{folderPath}/{ju_court}'  # 簡化路徑

    for d in range(10):
        year = startYear - d
        for month in range(1, 13):
            with open(f"{ju_Path}/{ju_court}_{year}年_{month}月.json", "r", encoding="utf-8") as js:
                strJs = js.read()
            listJudge = json.loads(strJs)

            juContent_Path = f'{ju_Path}/判決書'
            if not os.path.exists(juContent_Path):
                os.makedirs(juContent_Path)

            for i in range(len(listJudge)):
                driver.get(listJudge[i]["judge_link"])
                sleep(1)
                ju_content = driver.find_element(
                    By.CSS_SELECTOR, 'div.int-table.col-xs-8')
                with open(f"{juContent_Path}/{ju_court}_{year}年_{month}月_{listJudge[i]['judge_index']}.txt", "w", encoding="utf-8") as file:
                    file.write(ju_content.get_attribute("innerText"))


def close():
    driver.quit()


if __name__ == "__main__":
    startTime = time.time()
    # conSearch()
    conSearch_year()
    # getJudgeContent()
    # close()
    print(f"總花費時間 : {((time.time() - startTime)/60):.2f} 分鐘")
