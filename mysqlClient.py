import datetime
import glob
import os

import mysql.connector
import yaml

MICROSERVICES = {"com": "myDB"}
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


def main():
    mysqlJson = {'com': [{'students': {'key': ['test_id'],
                                       'column': {'test_id': '1e5-8f75-4984-d148-53e29bdfe41d',
                                                  'student_number': 1, 'created_date': datetime.date(2005, 5, 10),
                                                  'created_timestamp': datetime.datetime(2023, 5, 28, 3, 3, 35,
                                                                                         454584,
                                                                                         tzinfo=datetime.timezone.utc)
                                                  }}}]}
    f = open('./data/createCustomer' + '_' + str(datetime.datetime.now()), 'x', encoding='UTF-8')

    retrieveObject(mysqlJson, f)


def retrieveObject(mysqlJson: dict, f):
    compareBase(mysqlJson, f)


def createClient():
    print("a")


def compareBase(mysqlJson: dict, f):
    """
    Description:
        mysqlの比較を実施するベースの処理
    Args:
        mysqlJson (dict): {'microservice名':[{'TBL名':{'key':['レコード取得時のkey'],'column':{'columnA':'期待値','columnB':'期待値'}}}]}
        f (write): ファイル
    """
    # confidential項目のリストを格納する
    confidentialList = []

    # 対象となるmysqlのmicroservice名を全て取得する
    microserviceKeys = list(mysqlJson.keys())

    # 取り出したmicroserviceごとに比較を実施していく。
    for microserviceKey in microserviceKeys:
        # DB名を取得するために定義されているマイクロサービスか確認する
        if MICROSERVICES.get(microserviceKey) is not None:
            compareProcess(mysqlJson.get(microserviceKey), f, MICROSERVICES.get(microserviceKey),
                                          microserviceKey, confidentialList)
        else:
            print("定義されていないマイクロサービスです。mysqlClient.pyのMICROSERVICESに対象のマイクロサービスを追加してください。")
    print(confidentialList)
    return confidentialList, True


def compareProcess(tableList, f, database, microserviceKey, confidentialList):
    """
    Description:
        mysqlの比較を実施するベースの処理
    Args:
        tableList (list): [{'TBL名':{'key':['レコード取得時のkey'],'column':{'columnA':'期待値','columnB':'期待値'}}}]
        f (write): ファイル
        database (str): データベース名
        confidentialList (list): confidential項目を格納して返却するlist
    """
    # ListからTBLの要素を取り出していく。
    for tableObject in tableList:
        tableName = list(tableObject.keys())[0]
        results = retrieveEntity(tableObject, tableName, database, f)
        print(results)
        entities: dict = createMysqlEntity(tableName, list(results), microserviceKey)
        confidentialList.extend(entities.get('confidential'))
        # compareEntity()

    return True


def retrieveEntity(tableObject: dict, tableName, database, f):
    try:
        client = mysql.connector.connect(host='127.0.0.1', port='3306', user='root', password='rootpass',
                                         database=database)
    except Exception as e:
        print(e)
        exit()
    cursor = client.cursor()
    sql = f'select * from {tableName} where test_id = \'81bc21e5-8f75-4984-d148-53e29bdfe41d\';'
    cursor.execute(sql)

    return cursor.fetchall()


def createSqlforMysql():
    sql = ''
    return sql


def createMysqlEntity(table_name, entities, microserviceKey):
    """
    Description:
        Spannerから受け取ったレコードをjson形式にして返却する。
        API実行後にログに機密情報が出力されていないか確認するために、confidential項目をログに含めて返却する
    Args:
        table_name (str): 変換対象のTBL
        entities (list): Spannerから取得したレコードのリスト
    Returns:
        SpannerEntityResponse:spannerの項目とコンフィデンシャル項目のリスト

    """

    confidential_list = []

    table_name_key: dict = read_yaml(microserviceKey, table_name)

    response = {}
    response_list = []

    for entity in entities:
        column_key: dict = table_name_key[table_name]
        column_keys_list = list(column_key.keys())
        count = 0
        for column in column_keys_list:
            column_information: dict = column_key.get(column)
            # if column_information.get("type") == "string":
            #     print("文字列")
            # elif column_information.get("type") == "int":
            #     print("数字")
            # elif column_information.get("type") == "date":
            #     print("日付型")
            if column_information.get("type") == "timestamp":
                if isinstance(entity[count], datetime.datetime):
                    table_name_key[table_name][column]["value"] = entity[count] + datetime.timedelta(hours=9)
                    print(entity[count] + datetime.timedelta(hours=9))
                    print(table_name_key[table_name][column]["value"])

            # 暗号化対象の場合は暗号化して、格納する
            elif column_information.get("crypt"):
                # 暗号化したものを格納する
                table_name_key[table_name][column]["value"] = entity[count]
            else:
                table_name_key[table_name][column]["value"] = entity[count]

            # コンフィデンシャル項目の確認
            if column_information.get("confidential"):
                # コンフィデンシャル項目がある場合はリストに格納する。
                confidential_list.append(entity[count])

            count += 1

        # コンフィデンシャル項目をリストに入れて返却する
        table_name_key["confidential"] = confidential_list
        response_list.append(table_name_key[table_name])
    response[table_name] = response_list
    print(response[table_name])
    response["confidential"] = confidential_list
    # tes = SpannerEntityResponse(response_list,confidential_list)
    return response


def read_yaml(microservice, table):
    try:
        # yamlを参照し、returnする
        with open(f'mysqlEntity/{microservice}/{table}.yaml') as target_test:
            return yaml.safe_load(target_test)
    except Exception as e:
        print(f'mysqlEntityディレクトリに{microservice}/{table}.yamlが存在していません。')
        exit(e)


if __name__ == "__main__":
    print("start")
    main()
    print("end")

# mysql -u root -p
# docker compose exec my_sql bash
# rootpass
