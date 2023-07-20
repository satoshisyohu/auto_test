import datetime
import sys

import yaml
from logging import getLogger

# logger = logger_client.get_logger()
TARGET_TABLE = {"Drippers": "/Users/bandousatoshi/dev/python/zdf_api_autotest/entity/drippers.yaml"}


# logger = getLogger("log")


def main():
    entity = [['be403e44-2e5a-e5d9-b657-cb21695ee2f5', 'V60', '円錐', datetime.date.today(), datetime.datetime.now(),
               'admin', datetime.datetime.now(), 'admin'],
              ['be403e44-2e5a-e5d9-b657-cb21695ee2f5', 'V60', '円錐', datetime.date.today(), datetime.datetime.now(),
               'admin', datetime.datetime.now(), 'admin']]
    targets = ['V68', 'V60']

    crate_entity_for_compare("Drippers", entity)


# todo レコードの返却方法について再度要検討
def crate_entity_for_compare(table_name, entities):
    """
    Description:
        Spannerから受け取ったレコードをjson形式にして返却する。
        API実行後にログに機密情報が出力されていないか確認するために、confidential項目をログに含めて返却する
    Args:
        table_name (str): 変換対象のTBL
        entities (list): Spannerから取得したレコードのリスト
    Returns:
        dict: {"TBL_NAME": [{{"column1": "values"}, {"column２": "values"}},
        {{"column1": "values"}, {"column２": "values"}}],
         "confidential": ["confidentialA"]}

    """

    confidential_list = []

    entity_yaml_name = TARGET_TABLE.get(table_name)

    response = {}
    response_list = []

    if entity_yaml_name is not None:

        for entity in entities:
            with open(entity_yaml_name) as target_test:
                table_name_key: dict = yaml.safe_load(target_test)
                column_key: dict = table_name_key[table_name]
                column_keys_list: list = column_key.keys()
                count = 0
                for column in column_keys_list:
                    column_information: dict = column_key.get(column)
                    # if column_information.get("type") == "string":
                    #     print("文字列")
                    # elif column_information.get("type") == "int":
                    #     print("数字")
                    # elif column_information.get("type") == "date":
                    #     print("日付型")
                    # elif column_information.get("type") == "timestamp":
                    #     print("タイムスタンプ")

                    # 暗号化対象の場合は暗号化して、格納する
                    if column_information.get("crypt"):
                        # 暗号化したものを格納する
                        table_name_key[table_name][column]["value"] = entity[count]

                    table_name_key[table_name][column]["value"] = entity[count]

                    # コンフィデンシャル項目の確認
                    print(entity[count])
                    if column_information.get("confidential"):
                        # コンフィデンシャル項目がある場合はリストに格納する。
                        confidential_list.append(entity[count])

                    count += 1

                # コンフィデンシャル項目をリストに入れて返却する
                table_name_key["confidential"] = confidential_list
                response_list.append(table_name_key[table_name])
        response[table_name] = response_list
        response["confidential"] = confidential_list
        print(response)
        return response


if __name__ == "__main__":
    main()
