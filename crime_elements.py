'''
構成要件。CrimePredictCategory
selection：傷害意圖-1：過失、非故意非過失 、故意傷害、故意重傷害
selection：造成被害人受傷程度-2：非重傷、重傷、死亡 、無受傷結果
selection：傷害對象-3：尊親屬（父母與祖父母)、非尊親屬

。0 無罪：非故意非過失、無受傷結果
。9 傷害直系血親尊親屬 ：故意傷害、非重傷、尊親屬
。10 傷害直系血親尊親屬致死 ：故意傷害、死亡、尊親屬
。1 過失傷害：過失、非重傷、非尊親屬
。2 過失傷害致重傷：過失、重傷、非尊親屬
。3 傷害：故意傷害、非重傷、非尊親屬
。4 傷害致重傷 ：故意傷害、重傷、非尊親屬
。5 傷害致死 ：故意傷害、死亡、非尊親屬
。6 重傷害 ：故意重傷害、重傷、非尊親屬
。7 重傷害未遂 ：故意重傷害、非重傷、非尊親屬
。8 重傷致死 ：故意重傷害、死亡、非尊親屬
。11 其他：
'''
listSelect1 = ['非故意非過失', '過失', '故意傷害', '故意重傷害']
listSelect2 = ['無受傷結果', '非重傷', '重傷', '死亡']
listSelect3 = ['非尊親屬', '尊親屬']
listSelection = [listSelect1, listSelect2, listSelect3]


def element2Crime(select1, select2, select3):
    if select1 == '非故意非過失':
        crimePred = [0, '無罪']  # 無罪
        return crimePred
    elif select2 == '無受傷結果':
        crimePred = [0, '無罪']  # 無罪
        return crimePred
    elif select1 == '過失':
        if select2 == '非重傷':
            crimePred = [1, '過失傷害']  # 過失傷害
            return crimePred
        elif select2 == '重傷':
            crimePred = [2, '過失傷害致重傷']  # 過失傷害致重傷
            return crimePred
        elif select2 == '死亡':
            crimePred = [5, '傷害致死']  # 傷害致死
            return crimePred
    elif select1 == '故意傷害':
        if select2 == '非重傷':
            if select3 == '非尊親屬':
                crimePred = [3, '傷害']  # 傷害
                return crimePred
            elif select3 == '尊親屬':
                crimePred = [9, '傷害直系血親尊親屬']  # 傷害直系血親尊親屬
                return crimePred
        elif select2 == '重傷':
            if select3 == '非尊親屬':
                crimePred = [4, '傷害致重傷']  # 傷害致重傷
                return crimePred
            elif select3 == '尊親屬':
                crimePred = [9, '傷害直系血親尊親屬']  # 傷害直系血親尊親屬
                return crimePred
        elif select2 == '死亡':
            if select3 == '非尊親屬':
                crimePred = [5, '傷害致死']  # 傷害致死
                return crimePred
            elif select3 == '尊親屬':
                crimePred = [10, '傷害直系血親尊親屬致死']  # 傷害直系血親尊親屬致死
                return crimePred
    elif select1 == '故意重傷害':
        if select2 == '非重傷':
            if select3 == '非尊親屬':
                crimePred = [7, '重傷害未遂']  # 重傷害未遂
                return crimePred
            elif select3 == '尊親屬':
                crimePred = [9, '傷害直系血親尊親屬']  # 傷害直系血親尊親屬
                return crimePred
        elif select2 == '重傷':
            if select3 == '非尊親屬':
                crimePred = [6, '重傷害']  # 重傷害
                return crimePred
            elif select3 == '尊親屬':
                crimePred = [9, '傷害直系血親尊親屬']  # 傷害直系血親尊親屬
                return crimePred
        elif select2 == '死亡':
            if select3 == '非尊親屬':
                crimePred = [8, '重傷致死']  # 重傷致死
                return crimePred
            elif select3 == '尊親屬':
                crimePred = [10, '傷害直系血親尊親屬致死']
                return crimePred


if __name__ == '__main__':

    so = 0
    selected = []
    for sitem in listSelection:
        so += 1
        print(f'Selection {so}')
        i = 0
        for item in sitem:
            print(f'{i} : {item}')
            i += 1
        selected.append(int(input("\nSelect one : ")))
        print('\n')
    select1 = listSelect1[selected[0]]
    select2 = listSelect2[selected[1]]
    select3 = listSelect3[selected[2]]
    print(f'構成要件 : {select1} + {select2} + {select3}')

    result = element2Crime(select1, select2, select3)
    print(f'判斷罪刑結果為：{result[0]} - {result[1]}')
