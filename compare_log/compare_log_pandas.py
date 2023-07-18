import pandas as pd


# def read_file():
#     df = pd.read_csv('test.csv')
#     df_bool = df['error'] == 'error'
#     print(df_bool.sum())


def compare_log_counts(expected_log_count, target_error_level):
    """
    Args:
        expected_log_count (int): 期待するログ件数
        target_error_level (str): 検索するログレベル
    Returns:
        dict: 期待値と実際値の件数が一致する場合→　{"result" : True, "count": 実際のログ件数}
        　　　　期待値と実際値の件数が一致しない場合→　{"result" : False, "count": 実際のログ件数}
    """
    df = pd.read_csv('test.csv')
    actual_log_count = df['error'] == target_error_level
    response = {}
    if actual_log_count.sum() == expected_log_count:
        response["result"] = True
    else:
        response["result"] = False
    response["count"] = actual_log_count.sum()
    return response


def compare_target_log_word(target_word):
    """
    Args:
        target_word (str): 検索対象文字列
    Returns:
        dict: 対象の文字列が含まれている場合→　True
        　　　 対象の文字列が含まれていない場合→　False
    """
    df = pd.read_csv('test.csv')
    search_series = df['message'].str.contains(target_word)
    log_message_flag = False
    if search_series.sum() >= 1:
        log_message_flag = True
    return log_message_flag


def compare_target_log_word_modify(log_level, target_word):
    """
    Description:

    Args:
        log_level (str): 対象のログレベル
        target_word (str): 検索対象文字列
    Returns:
        dict: 対象の文字列が含まれている場合→　True
        　　　 対象の文字列が含まれていない場合→　False
    """
    response = {}
    df = pd.read_csv('test.csv')
    res = df.query('error.str.contains(@log_level) &message.str.contains(@target_word)')
    print(len(res))
    if len(res) >= 1:
        response["result"] = True
    else:
        response["result"] = False
    response["count"] = len(res)
    return response


def compare_confidential_log_word(target_word):
    """
    Args:
        target_word (str): 検索対象文字列
    Returns:
        dict: 対象の文字列が含まれている場合→　True
        　　　 対象の文字列が含まれていない場合→　False
    """
    df = pd.read_csv('test.csv')
    search_series = df['message'].str.contains(target_word)
    log_message_flag = False
    if search_series.sum() >= 1:
        log_message_flag = True
    return log_message_flag


def main():
    print("main")
    expected_log_count = 1
    response: dict = compare_log_counts(expected_log_count, "error")
    print("--------------ログ件数比較--------------")
    if response.get("result"):
        print(f'期待値 | 実際値 | 結果\r\n'
              f'{expected_log_count} | {response.get("count")} | OK')
    else:
        print(f'期待値 | 実際値 | 結果\r\n'
              f'{expected_log_count} | {response.get("count")} | NG')

    target_word = "失敗"
    print("--------------ログメッセージ比較--------------")
    if compare_confidential_log_word(target_word):
        print(f'結果：OK')
        print(f'対象ログ：「{target_word}」が出力されています。')
    else:
        print(f'対象ログ：「{target_word}」が出力されていません。')
        print(f'結果：NG')

    print("compare_target_log_word_modify")
    target_log_level = "error"
    print("--------------ログメッセージ:件数比較--------------")
    response_log = compare_target_log_word_modify(target_log_level, target_word)
    if response_log:
        if response_log.get("count") == 1:

            print(f'対象メッセージ | 対象ログレベル ｜ 件数 | 結果 \r\n'
                  f'{target_word} | {target_log_level} | '
                  f'{response_log.get("count")} | OK')
        else:
            print(f'対象メッセージ | 対象ログレベル ｜ 件数 | 結果 | 備考 \r\n'
                  f'{target_word} | {target_log_level} | '
                  f'{response_log.get("count")} | OK | ※対象ログが複数件出力されています。')
    else:
        print(f'対象メッセージ | 対象ログレベル ｜ 件数 | 結果 | 備考 \r\n'
              f'{target_word} | {target_log_level} | '
              f'{response_log.get("count")} | NG | 対象のログが出力されませんでした。')


if __name__ == "__main__":
    main()
