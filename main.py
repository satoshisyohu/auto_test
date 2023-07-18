import datetime
import glob
import json
import os.path
import sys

import yaml
import requests
import pprint
import dotenv
import re

from requests import Response

import entity.drippers
from spanner_client import spanner_client
import util.load_args
from logger_client import logger_client
from util.utils import switch_reserve_words
from util.assert_spanner import compare_spanner

from result_writer import result_writer as res_writer

URI = 'requestURI'
TEST_CASE = 'testCase'
CASE_NO = 'caseNo'
TITLE = 'title'
HEADER = 'header'
X_REQUEST_VERSION = 'x-request-version'
X_ID_TOKEN = 'x-id-Token'
X_ITDEMPOTENCY_KEY = 'x-idempotency-key'
REQUEST = 'request'
RESPONSE = 'response'
BODY = 'body'
SPANNER = 'spanner'
LOG = 'log'
HOST = "http://localhost:8080"
KEY = "key"

CRLF = '\r\n'
SPACE_15 = '        '

NOT_COMPARE_WORDS = ["not compared"]

logger = logger_client.get_logger()

MICROSERVICES = {"cotra": "-front-cotra", "deposit": "-fcore-deposit"}

TABLE = ["Drippers"]


def main():
    # 環境変数の読み込み

    # 引数の読み込み
    args = util.load_args.load_args()
    env = args.env  # 実行環境
    case = args.case  # 実行するテストフォルダ名
    case_no = args.no  # テストケース番号
    mode = args.mode  # 実行するモード

    # yamlファイルを読み込む
    target_yaml = read_yaml(case)

    # yamlから対象となるテストケース番号を抽出する
    test_list = create_target_test_list(target_yaml, case_no)

    # テスト実行、期待値の比較等
    execute_test(target_yaml, test_list, env)


def read_environ():
    dotenv.load_dotenv()
    print(os.getenv('ENVIRONMENT'))
    print(os.getenv('DATABASES'))

    # 環境変数を上書きする
    os.environ['ENVIRONMENT'] = 'dev'
    print(os.getenv('ENVIRONMENT'))


# 処理実行時に引数を受け取る
# 引数より対象のディレクトリを読み込みyamlファイルを返却する。
# param1: 実行するテストのディレクトリ名(テスト名)
# param2  実行時のテスト番号、指定されていない場合はNoneで全ケース実行となる
def read_yaml(case):
    print("yamlファイルの読み込み")

    # ディレクトリの存在確認
    # todo createCustomerの部分は引数から受け取る
    if not os.path.isdir(case):
        exit()
    files = glob.glob(case + '/*')

    # ループさせているが基本的にはファイルが１つの想定
    # todo 後々　A実行後にBも実行等のシナリオテストもできるようにしたい
    for file in files:
        if file.endswith('.yaml'):
            target_yaml = file
        else:
            exit("yamlファイルが存在していません")

    # yamlを参照し、returnする
    with open(target_yaml) as target_test:
        obj: dict = yaml.safe_load(target_test)
    return obj


# yamlを受け取り実行するテスト番号のリストを返却する
# param1: yamlファイル
# param2  実行時のテスト番号、指定されていない場合はNoneで全ケース実行となる
def create_target_test_list(obj, case_no):
    test_case_no_list = obj[TEST_CASE]

    # 対象となるテストケースを格納するためのリスト
    target_test_number_list = []

    # yamlファイルからテストケースを抽出する。
    if case_no is None:
        for test_case_no in test_case_no_list:
            # if str(test_case_no).startswith("TS-"):
            target_test_number_list.append(str(test_case_no))
    # テストケースが指定されている場合は引数から抽出する。
    else:
        target_test_number_list = case_no.split(',')

    return target_test_number_list


# yamlと実行するテスト番号を受け取りテストを実行し、結果をassertする
# param1: yamlファイル
# param2  テストケース番号
def execute_test(obj, test_list, env):
    for test_no in test_list:
        logger.info(test_no)

        # テストに必要な情報を抽出する。
        target_test_information: dict = obj[TEST_CASE][test_no]

        # headerの情報を抽出する
        raw_header: dict = target_test_information[HEADER]
        # 予約後が含まれている場合は事前に変換する
        edited_header: dict = create_message(raw_header)

        # req body抽出
        raw_request_body: dict = target_test_information[REQUEST]

        # 予約後が含まれている場合は事前に変換する
        edited_requests_body: dict = create_message(raw_request_body)

        logger.info(edited_requests_body)
        # APIの実行
        logger.info(f'テストケース{test_no}:「{target_test_information[TITLE]}」を実行します。')
        response: Response = requests.post(url=HOST + obj[URI], json=edited_requests_body, headers=edited_header)
        logger.info(f'実行時間:{response.elapsed.total_seconds()}秒')
        logger.info(f'レスポンス:{response}')

        # 実際値のレスポンスボディ抽出
        actual_response_body: dict = response.json()

        # 実際値のレスポンス情報抽出
        expected_response_body: dict = target_test_information[RESPONSE]

        # 期待値のレスポンスステータス抽出
        expected_status = expected_response_body['status']

        # 期待値のレスポンスボディ抽出
        expected_response_body: dict = expected_response_body['body']

        # ファイルに名前を付けるための現在時刻
        now = datetime.datetime.now()

        # 引数から受け取った値をトリミングしてファイル名にするように変更する
        f = open('./data/createCustomer' + '_' + str(now), 'x', encoding='UTF-8')
        # excel書き込み用のカウンタインスタンス変数
        count = 4
        wb = res_writer.create_workbook()
        ws = res_writer.create_new_sheet(wb, f'TS-{test_no}', str(now))
        f.write('テスト番号：TS-' + test_no + CRLF)
        f.write('実行時刻：' + str(now) + CRLF)
        f.write('--------ステータスコード--------' + CRLF)
        res_writer.write_expect_actual(ws=ws, count=count, title="ステータスコード")
        write_expect_actual(f)

        f.write(SPACE_15 + str(response.status_code) + "|" + str(expected_status) + CRLF)

        # statusコードの比較
        if response.status_code == expected_status:
            # statusコードの書き込み
            ws, count = res_writer.write_status_code(ws=ws, expected_status_code=expected_status,
                                                     actual_status_code=response.status_code, count=count)
            # statusコードの比較に成功してステータスが200の場合
            if expected_status == 200:
                f.write(f'--------レスポンスボディ比較--------{CRLF}')
                write_expect_actual(f)

                # response比較
                # 正常終了かつレスポンスの値が存在しない場合
                compare_elements_dict: dict = {}
                if len(expected_response_body) == 0 and actual_response_body == expected_response_body:
                    logger.info("response比較 is OK")
                    f.write(f'{expected_response_body} | {actual_response_body} | OK')

                # 正常終了かつレスポンスに値が存在している場合値を比較する
                # 比較方法は期待値のレスポンスから要素を取得し実際に帰ってきた値からも同じように要素を取得する。
                # responseの辞書の数が同じ場合は期待値をループで回す。
                # responseの辞書の数が期待値のほうが多い場合は期待値を回す。
                elif len(expected_response_body) >= len(actual_response_body):
                    compare_elements_dict = expected_response_body

                # responseの辞書の数が実際値のほうが多い場合は実際値を回す
                else:
                    compare_elements_dict = actual_response_body

                # response
                # この回し方はだめな気がする。
                # todo 期待値側にしか予約後はないから期待値側を回す用にしないといけない。
                # 実際値にのみある値が返却されていたときにどうする？
                # todo 細かく比較できるように条件分岐していく必要あり
                for compare_element in list(compare_elements_dict.keys()):
                    # 予め比較しない文言が設定されている場合は比較を実施しない。
                    if expected_response_body.get(compare_element) in NOT_COMPARE_WORDS:
                        continue
                    elif expected_response_body.get(compare_element) == actual_response_body.get(compare_element):
                        logger.info("response比較 is OK")

                # Spannerの値の比較
                # 比較対象のmicroservices名を抽出する。
                microservices = target_test_information[SPANNER]

                # microservicesごとにデータベースの期待値を比較していく
                f.write('--------Spanner比較--------' + CRLF)
                for target_databases in microservices:

                    # 対象のマイクロサービスが定義されていない場合は比較をしない。
                    if MICROSERVICES.get(target_databases) is not None:

                        # spanner_client用にdatabases_idを生成
                        databases_id = env + MICROSERVICES[target_databases]

                        # 対象microserviceから比較対象となるTBL名をリストとして抽出する。
                        table_objects: list = target_test_information[SPANNER][target_databases]

                        for table in table_objects:

                            # リストから抽出したオブジェクトをdict形式に変換する
                            table_dict = dict(table)

                            # table名を取得する。
                            table_name = list(table.keys())[0]
                            ws, count = res_writer.write_expect_actual(ws=ws, count=count, title=table_name)

                            # レコード取得時のカラム名を取得する
                            key = table_dict[table_name][KEY]
                            logger.info(key)
                            value = table_dict[table_name]["column"][key]
                            client = spanner_client.create_client('dev-spanner-trial')
                            sql = spanner_client.create_sql(table=table_name, key=key, value=value)

                            spanner_response = list(spanner_client.search_records(client=client, sql=sql))

                            # responseのリストの長さが0の場合はエラーとして書き込む
                            f.write(f'{table_name}{CRLF}')

                            write_expect_actual(f)

                            for response in spanner_response:
                                if table_name in TABLE:

                                    # 取得した値のリストをdict形式に変換する
                                    entity_dict: dict = util.assert_spanner.compare_spanner(table_name, response)

                                    # 取得したdictからカラム名をリスト形式で抽出する
                                    column_names: list = entity_dict[table_name]

                                    # カラム名をリストで回し値をアサートしていく。
                                    for column_name in column_names:
                                        # spannerの値を比較する。
                                        # todo 比較の前に期待値レコードに特定のワードがないか確認する。あればスキップするようにする。
                                        if table_dict[table_name]["column"][column_name] == \
                                                entity_dict[table_name][column_name]["value"]:
                                            f.write(
                                                f'{SPACE_15}{str(entity_dict[table_name][column_name]["value"])} | {str(table_dict[table_name]["column"][column_name])} | OK{CRLF}')
                                            logger.info("ok")
                                        else:
                                            f.write(
                                                f'{SPACE_15}{str(entity_dict[table_name][column_name]["value"])} | {str(table_dict[table_name]["column"][column_name])} | NG{CRLF}')

                                            logger.info("ng")

                    # spannerのクライアントを作成する。
                    # TBLのレコードを取得する。
                    # 値を比較する。OK、NG等のアサーションを実施する。
                    else:
                        logger.info("定義されていないマイクロサービスです")
                        continue

            elif expected_status == 400 or 500:
                logger.info("エラー時の情報比較")





        else:
            logger.info("statusコード比較失敗")

        # db比較

        # log取得

        # 結果をファイルに書き込み
        res_writer.save_workbook(wb)
        f.close()


def create_message(elements):
    for element in elements:
        value: str = elements[element]

        if re.search(r"\${\w+}", value) is not None:
            print(value)

            elements[element] = switch_reserve_words(value)
    return elements


def write_expect_actual(f):
    f.write(f'{SPACE_15} 期待値|実際値 {CRLF}')


if __name__ == "__main__":
    main()
