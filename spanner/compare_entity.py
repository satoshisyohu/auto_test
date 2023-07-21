import datetime
import re
import sys

import util.utils as util

CRLF = '\r\n'
SPACE_15 = '      '
LINE = '----------------------------------------------------------------------'

def main():
    print("comapare Spanner")

    NOT_COMPARED = '${NOT_COMPARED}'
    IS_EXIST = '${IS_EXIST}'
    CURRENT_TIMESTAMP = '${CURRENT_TIMESTAMP}'
    #
    # deal_reserve_spanner_words('${NOT_COMPARED}',"aa") #ok
    # deal_reserve_spanner_words('${NOT_COMPARED}',None) #ok
    # deal_reserve_spanner_words('${IS_EXIST}',"a") #ok
    # deal_reserve_spanner_words('${IS_EXIST}',None) #ng

    deal_reserve_spanner_words('${CURRENT_TIMESTAMP}','2023-07-21 00:44:00') #ok
    deal_reserve_spanner_words('${CURRENT_TIMESTAMP}','2023-05-28 01:36:35') #ng
    #
    # deal_reserve_spanner_words("test","test") #ok
    # deal_reserve_spanner_words("test","tet") #ok

    sys.exit()

    expected_entity = {'DripperId': 'be403e44-2e5a-e5d9-b657-cb21695ee2f6', 'DripperName': None,
                       'DripperType': 'ウェーブ', 'CreatedDripperDate': datetime.date.today(),
                       'CreatedDate': datetime.datetime.now(),
                       'CreatedUser': 'admin',
                       'UpdatedDate': datetime.datetime.now(),
                       'UpdatedUser': 'admin'}

    actual_entity = [{"DripperId": 'be403e44-2e5a-e5d9-b657-cb21695ee2f6', "DripperName": None, "DripperType": 'ウェーブ',
                      "CreatedDripperDate": datetime.date.today(),
                      "CreatedDate": datetime.datetime.now(), "CreatedUser": 'admin',
                      "UpdatedDate": datetime.datetime.now(), "UpdatedUser": 'admin'},
                     {"DripperId": 'be403e44-2e5a-e5d9-b657-cb21695ee2f6', "DripperName": None, "DripperType": 'ウェーブ',
                      "CreatedDripperDate": datetime.date.today(),
                      "CreatedDate": datetime.datetime.now(), "CreatedUser": 'admin',
                      "UpdatedDate": datetime.datetime.now(), "UpdatedUser": 'admin'}]
    table_name = "Drippers"
    compare_spanner_entity(expected_entity, actual_entity, table_name)
    # dict: [{{"column1": "values"}}, {{"column２": "values"}}]


def compare_spanner_entity(expected_entity, actual_entity, table_name):
    """
    Description:
        期待値に定められたエンティティのjsonとSpannerから実際に取得した値をリストを取得する。
        取得したリストのlengthが0の場合は期待値のみ書き込み処理を終了する。
        取得したリストのlengthが1の場合は期待値と実際値を処理を終了する。(期待値は0)
        取得したリストのlengthが2以上の場合
            1レコード目:実際値と期待値を比較し書き込み
            2レコード目以降:実際値のみ記入する。

    Args:
        expected_entity (dict): 変換対象のTBL
        actual_entity (list): Spannerから取得したレコードのリスト
        table_name(str): TBL名称
    Returns:
        void: 比較に成功した場合はTrue
    """
    # 期待値より、比較に必要なカラム名を抽出する。
    column_names = expected_entity.keys()

    print(table_name)
    print(LINE)

    # Spannerからレコードが取得できなかった場合は、TBL名と比較結果をNGで出力する。
    if len(actual_entity) == 0:
        # f.write(f'{SPACE_15} 期待値|実際値|ステータス {CRLF}')

        print(f'{SPACE_15} 期待値|実際値|ステータス {CRLF}')
        for column_name in column_names:
            print(f'{SPACE_15} {expected_entity.get(column_name)}|None|NG {CRLF}')

    # Spanner、実際値ともに同じの場合はレコードを比較する。
    # todo 特定の文言が含まれている場合は変換処理を実施する。
    elif len(actual_entity) == 1:
        print(f'{SPACE_15} 期待値|実際値|ステータス {CRLF}')

        for column_name in column_names:
            # 特定のワードが含まれている時の処理も必要
            if expected_entity.get(column_name) == actual_entity[0][column_name]:
                print(f'{SPACE_15} {expected_entity.get(column_name)}|{actual_entity[0][column_name]}|OK {CRLF}')
            else:
                print(f'{SPACE_15} {expected_entity.get(column_name)}|{actual_entity[0][column_name]}|NG {CRLF}')

    # Spanner>実際値が2件以上の場合は1件目のみ比較する。
    # 2件目以降は書き込みを実施するが、結果はNGとする。

    elif len(actual_entity) >= 2:
        count = 0
        for actual in actual_entity:

            if count == 0:
                for column_name in column_names:
                    # todo 特定の文言が含まれている場合は変換処理を実施する。
                    if expected_entity.get(column_name) == actual.get(column_name):
                        print(
                            f'{SPACE_15} {expected_entity.get(column_name)}|{actual.get(column_name)}|OK {CRLF}')
                    else:
                        print(
                            f'{SPACE_15} {expected_entity.get(column_name)}|{actual.get(column_name)}|NG {CRLF}')

            else:
                print(f'{table_name} [{count}]')
                print(LINE)
            # 出力時にカラム名が必要なためカラム名をループで回す。
                for column_name in column_names:
                    print(f'{SPACE_15} None|{actual.get(column_name)}|NG {CRLF}')
            count += 1

def deal_reserve_spanner_words(expectedWords,acutualWords):
    NOT_COMPARED = '${NOT_COMPARED}'
    IS_EXIST = '${IS_EXIST}'
    CURRENT_TIMESTAMP = '${CURRENT_TIMESTAMP}'
    print("予約後の処理を実施する")
    # ${NOT_COMPARED}→比較対象外とする。
    # ${IS_EXIST}→対象のレコードがNull(None)でなければOK
    # ${CURRENT_TIMESTAMP}→API実行時刻であればOK
    editedexpectedWords = None
    editedAcutualWords = None
    #とりあえず簡単に比較
    if re.search(r"\${\w+}", expectedWords) is not None:
        editedexpectedWords = util.switch_reserve_words(expectedWords)
        if NOT_COMPARED in expectedWords:
            print("okk")
            return True
        if IS_EXIST in expectedWords:
            if acutualWords is not None:
                print("okk")
                return True
            else:
                print("ng")
                return False
        if CURRENT_TIMESTAMP in expectedWords:
            start = datetime.timedelta(minutes=1)
            end = datetime.timedelta(minutes=-1)
            timestamp = datetime.datetime.now()
            editedAcutualWords = datetime.datetime.strptime(acutualWords, '%Y-%m-%d %H:%M:%S')
            if timestamp - start <= editedAcutualWords <= timestamp - end:
                print("ok")
                return True
            else:
                print("Ng")
                return False
    else:
        return expectedWords == acutualWords




if __name__ == "__main__":
    main()
