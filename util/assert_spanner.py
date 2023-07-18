import datetime

import yaml
from logger_client import logger_client

logger = logger_client.get_logger()
TARGET_TABLE = {"Drippers": "/Users/bandousatoshi/dev/python/zdf_api_autotest/entity/drippers.yaml"}


def main():
    entity = ['be403e44-2e5a-e5d9-b657-cb21695ee2f5', 'V60', '円錐', datetime.date.today(), datetime.datetime.now(),
              'admin', datetime.datetime.now(), 'admin']

    compare_spanner("Drippers", entity)


def compare_spanner(table_name, entity):
    entity_yaml_name = TARGET_TABLE.get(table_name)
    if entity_yaml_name is not None:
        with open(entity_yaml_name) as target_test:
            table_name_key: dict = yaml.safe_load(target_test)
            column_key: dict = table_name_key[table_name]
            column_keys_list: list = column_key.keys()
            count = 0
            for column in column_keys_list:
                column_information: dict = column_key.get(column)
                if column_information.get("type") == "string":
                    logger.info("文字列")
                elif column_information.get("type") == "int":
                    logger.info("数字")
                elif column_information.get("type") == "date":
                    logger.info("日付型")
                elif column_information.get("type") == "timestamp":
                    logger.info("タイムスタンプ")
                # 暗号化対象確認
                if column_information.get("crypt"):
                    logger.info("暗号化対象と暗号化処理を実行")

                if column_information.get("confidential"):
                    # todo confidential項目はリストに入れて返却する用にする。
                    # 返却された側はそれをリストに格納して、最後に一括で検索する。　
                    logger.info("どうしようかな")
                table_name_key[table_name][column]["value"] = entity[count]
                count += 1
            logger.info(table_name_key)
            return table_name_key


if __name__ == "__main__":
    main()
