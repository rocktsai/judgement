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

# 普通傷害罪：傷害之犯意 傷害之不確定故意 具有主觀上傷害之犯意 基於傷害 傷害他人身體之犯意
T_277 = ['傷害之犯意', '傷害之不確定故意', '具有主觀上傷害之犯意', '基於傷害', '傷害他人身體之犯意']

# 重傷害罪：毀敗或嚴重減損 毀敗或嚴重毀損 重傷害之不確定故意 重傷害之故意 基於使人受重傷害之犯意
T_278 = ['重傷害之不確定故意', '重傷害之故意', '基於使人受重傷害之犯意']

# 重傷害未遂：未達毀敗或減損 之重傷害結果而未遂 如經過相當之診治而能回復原狀 或雖不能回復原狀而僅減衰其效用者 仍不得謂為該款之重傷 未有重傷害結果 應以未遂論 毀敗或嚴重減損 毀敗或嚴重毀損 之重傷害結果而未遂 未達毀敗或減損
T_278_att = ['之重傷害結果而未遂', '未達毀敗或減損', '未達毀敗或嚴重減損', '如經過相當之診治而能回復原狀',
             '或雖不能回復原狀而僅減衰其效用者', '仍不得謂為該款之重傷', '未有重傷害結果', '應以未遂論']

# 過失傷害：無不能注意之情事 無不能注意之情形 竟疏未注意 疏未注意上開注意義務 違反上開注意義務 違反前揭注意義務 違反前開注意義務 本應具有前揭注意義務 本應具有前開注意義務 本應具有上開注意義務 具有相當因果關係 本應審慎注意
T_284 = ['無不能注意之情事', '無不能注意之情形', '竟疏未注意', '疏未注意上開注意義務', '違反上開注意義務', '違反前揭注意義務',
         '違反前開注意義務', '本應具有前揭注意義務', '本應具有前開注意義務', '本應具有上開注意義務', '具有相當因果關係', '本應審慎注意']

# 無罪：尚符合正當防衛 尚符合緊急避難 尚符合父母懲戒權 尚符合教師懲戒權 符合正當防衛而阻卻違法
Recht = ['尚符合正當防衛', '尚符合緊急避難', '尚符合父母懲戒權',
         '尚符合教師懲戒權', '符合正當防衛而阻卻違法', '符合緊急避難而阻卻違法']


feature_elememtsAndCrime = []


folderPath = '/Users/allentsai/python_web_scraping-master/judgement_file'
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

# 測試用主文
test_content = '主文:張智發犯傷害罪，處有期徒刑陸月，如易科罰金，以新臺幣壹仟元折算壹日。犯罪事實及理由一、犯罪事實：張智發於民國110年5月29日下午1時許，在彰化縣○○鄉○○村○○路0段00號住處，與家人發生糾紛而經家人報警處理，其於警方到場後，明知張恩綺、施秉宏均係身著警察制服依法執行職務之警員，竟基於妨害公務之犯意，當場以「恁爸差消哩係警察喔！」、「恁爸就是要針對你！」、「穿衫（意指警察制服）我也沒在信道」、「你菜鳥警察你是怎樣！」（均臺語）等語，辱罵在場依法執行職務之警員張恩綺、施秉宏（所涉公然侮辱罪嫌部分，未據告訴），並於得知救護車到場時情緒激動，遂承前妨害公務及普通傷害之犯意，先推擠警員施秉宏，警員張恩綺見狀上前制止，卻被張智發出手勒住張恩綺的脖子，張恩綺不斷掙扎，經施秉宏及張智發之家人合力制止張智發，施秉宏並將張智發手部上銬，而在上開衝突期間張智發持續掙扎，並吼叫「你們叫警察趕快走喔，不然我等下搶槍不要怪我喔！」、「你給我銬試試看，我絕對會讓你後悔，恁爸絕對會讓你們倆後悔！幹你娘！你娘！銬啥！」、「恁爸絕對會讓你後悔，恁爸剛剛說過了，你給我銬三小，你給我銬試試看，恁爸絕對會搶槍的，我給你警告你還給我銬！」、「來，你叫什麼名！」、「你給我銬又給我壓喔，你就不要下班被我遇到喔，我先跟你警告，你給我銬沒關係，你現在給我銬我手很痛喔，我數到三你沒放開我絕對會讓你後悔！」、「你們下班給恁爸卡注意ㄟ，幹你娘機掰！我已經沒有動了，你還壓我喔，你們下班給我注意一點，你們如果下班不要給我從永靖來！」、「看三小！幹你娘機掰！看你家死人！幹你娘！看三小！蛤！你係看三小！恁爸跟死人講話！」、「恁爸發誓啦，我張智發啦，誰開救護車載恁爸，他全家死光光，包括這裡的警察，恁爸活到三十歲就好啦，幹你娘，恁爸這條命跟他博，幹你娘！」、「會怕死就別來！臭機掰！」（均臺語）等語，以此方式對於執行職務之警員張恩綺及施秉宏，施以強暴、脅迫，妨害張恩綺與施秉宏執行職務，且足以貶損張恩綺、施秉宏公務執行之社會評價，同時造成張恩綺受有右側手部挫傷及右側手肘挫傷等傷害。二、證據：1.被告張智發於警詢時及偵訊中之自白。2.證人即告訴人張恩綺證述。3.彰化縣員林分局永靖分駐所110報案紀錄單。4.員生醫院診斷證明書。5.密錄器影像畫面截圖及錄影光碟、警方密錄器譯文。6.衛生福利部彰化醫院函暨病歷資料。7.彰化縣警察局員林分局函暨職務報告、彰化縣疑似精神病人護送鑑定及就醫通報單、彰化縣警察局員林分局永靖分駐所員警工作紀錄簿。8.本院110年度簡附民第89號案件全卷卷宗資料（包含當庭勘驗密錄器光碟）。三、核被告所為，係犯刑法第135條第1項之對於執行職務公務員施強暴、同法第140條第1項之侮辱公務員、同法第277條第1項之傷害罪。又被告以一行為，同時觸犯上開數罪名，為想像競合犯，應依刑法第55條規定，從一重處斷。檢察官雖認被告亦同時觸犯刑法第305條之恐嚇危害安全罪嫌等情，然警員施秉宏部分，警員施秉宏則未曾表示被告言語導致其心生畏懼；且依本院於附帶民事訴訟案件審理時當庭勘驗密錄器影像所示，被告於怒罵、恐嚇警員之同時，亦對於警員有推擠、傷害行為，而恐嚇罪係危險犯，傷害罪係實害犯，依實害行為吸收危險行為之原則，被告對警員張恩綺恐嚇同時加以傷害，恐嚇行為已經為實害之傷害所吸收，無另需論以想像競合犯。四、本院審酌被告張智發在警察執行職務時，對於警察執法行為施加肢體及言語暴力，影響警員職務之執行，並造成警員即告訴人張恩綺受傷；而從本院於審理附帶民事訴訟中所勘驗員警密錄器影像中可知，被告在警員執行職務時，不但對於警員施秉宏及張恩綺咆哮、以三字經及不雅文字怒罵及恐嚇外，也拍打、推擠警員施秉宏，另攻擊警員張恩綺，造成張恩綺手部輕微受傷，另以手勒住警員張恩綺脖子，影片中並可聽見張恩綺痛苦喘息之聲音，此部分雖未造成警員張恩綺受傷（依本案之證據，告訴人張恩綺僅有手部受傷），但是已嚴重影響警員職務之執行；另審酌被告雖然坦承犯行，但在本院審理附帶民事案件時，仍可見被告在開庭時對於告訴人張恩綺惡言相向，毫無悔意；兼衡被告自述國中畢業之智識程度、從商等一切情狀，量處如所示之刑，並諭知易科罰金之折算標準。五、據上論斷，依刑事訴訟法第449條第1項前段、第3項、第454條第1項，逕以簡易判決處刑如。六、如不服本判決，得於判決送達後20日內向本院提出上訴狀，上訴於本院第二審合議庭（須附繕本）。本案經檢察官何蕙君聲請以簡易判決處刑。中華民國111年1月13日刑事第二庭法官陳怡潔以上正本證明與原本無異。如不服本判決，得自收受送達之日起20日內，表明上訴理由，向本院提起上訴狀（須附繕本）。告訴人或被害人對於判決如有不服具備理由請求檢察官上訴者，其上訴期間之計算係以檢察官收受判決正本之日期為準。中華民國111年1月13日'


# 針對構成要件的組合判斷出罪刑
def rawdata_to_featureForm():
    efolderList = os.listdir(f'{folderPath}/{folder}')
    epIndex = 0
    for ep in efolderList:
        print(ep, ':', epIndex)
        epIndex += 1
    efp = int(input("\n選擇要分出罪刑的rawdata.json : "))
    efolder = efolderList[efp]
    print(f'你選擇的是：{efolder}\n')

    with open(f'{folderPath}/{folder}/{efolder}', 'r', encoding='utf-8') as jsr:
        strJs = jsr.read()
    listJudge = json.loads(strJs)

    for i in range(len(listJudge)):
        strJudgeCont = listJudge[i]['judge_content']
        T_278_score, T_278_att_score, T_284_score, T_277_score, Recht_score, Crime_pred = elements_to_judgecrime(
            strJudgeCont)
        match = 0
        if Crime_pred in listJudge[i]['judge_crime']:
            match = 1
        feature_elememtsAndCrime.append({
            'judge_court': listJudge[i]['judge_court'],      # 判決法院
            'judge_year': listJudge[i]['judge_year'],         # 裁判年度
            'judge_month': listJudge[i]['judge_month'],       # 裁判月份
            'judge_index': listJudge[i]['judge_index'],     # 地院年度月份的第幾筆
            'judge_title': listJudge[i]['judge_title'],      # 裁判案由
            'T_278_score': T_278_score[0],                      # 重傷害罪_分數
            'T_278_att_score': T_278_att_score[0],              # 重傷害未遂_分數
            'T_284_score': T_284_score[0],                      # 過失傷害_分數
            'T_277_score': T_277_score[0],                      # 普通傷害_分數
            'Recht_score': Recht_score[0],                      # 無罪_分數
            'judge_crimePred': Crime_pred,                       # 罪刑預測
            'judge_crime': listJudge[i]['judge_crime'],          # 罪名
            'Match': match,                                      # 罪刑預測與實際罪名是否相符
            'judge_result': listJudge[i]['judge_result'],        # 刑責
            'judge_resultInt': listJudge[i]['judge_resultInt']  # 刑責int
        })
    with open(f'{folderPath}/{folder}/feature_罪刑預測.json', 'w', encoding='utf-8') as jsw:
        jsw.write(json.dumps(feature_elememtsAndCrime, ensure_ascii=False))
    pd.DataFrame(feature_elememtsAndCrime).to_csv(
        f'{folderPath}/{folder}/feature_罪刑預測.csv', index=None, encoding='utf-8')


# 針對構成要件的組合判斷出罪刑
def elements_to_judgecrime(strJudgeCont):

    T_278_score = [0, '重傷害罪']
    T_278_att_score = [0, '重傷害未遂']
    T_284_score = [0, '過失傷害']
    T_277_score = [0, '普通傷害罪']
    Recht_score = [0, '無罪']
    Crime_pred = ''  # 罪刑預測

    # print(strJudgeCont)
    for t in T_278:
        if t in strJudgeCont:
            T_278_score[0] += 1
            # print(t)
    print(f'{T_278_score[1]} = {T_278_score[0]}')

    for t in T_278_att:
        if t in strJudgeCont:
            T_278_att_score[0] += 1
            # print(t)
    print(f'{T_278_att_score[1]} = {T_278_att_score[0]}')

    for t in T_284:
        if t in strJudgeCont:
            T_284_score[0] += 1
            # print(t)
    print(f'{T_284_score[1]} = {T_284_score[0]}')

    for t in T_277:
        if t in strJudgeCont:
            T_277_score[0] += 1
            # print(t)
    print(f'{T_277_score[1]} = {T_277_score[0]}')

    for r in Recht:
        if r in strJudgeCont:
            Recht_score[0] += 1
            # print(r)
    print(f'{Recht_score[1]} = {Recht_score[0]}')

    if Recht_score[0] > 0:
        Crime_pred = Recht_score[1]
    elif max(T_278_score, T_278_att_score, T_284_score, T_277_score)[0] == 0:
        Crime_pred = Recht_score[1]
    else:
        Crime_pred = max(T_278_score, T_278_att_score,
                         T_284_score, T_277_score)[1]

    print(f'罪刑預測：{Crime_pred}')
    return T_278_score, T_278_att_score, T_284_score, T_277_score, Recht_score, Crime_pred


if __name__ == "__main__":
    startTime = time.time()

    rawdata_to_featureForm()
    # elements_to_judgecrime(test_content)

    print(f"總花費時間 : {((time.time() - startTime)/60):.2f} 分鐘")
