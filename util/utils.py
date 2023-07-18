import re
import uuid
import datetime

# 予約後変数

# uuid
UUID = '${UUID}'

# timestamp
CURRENT_TIMESTAMP = '${CURRENT_TIMESTAMP}'
# SPANNER_TIMESTAMP_MINUS = '${CURRENT_TIMESTAMP}-3'
# SPANNER_TIMESTAMP_PLUS = '${CURRENT_TIMESTAMP+'

CURRENT_DATE = '${CURRENT_DATE}'


# 予め予約されている変数を置き換える処理。
# 指定できる予約後はReadme を参照すること

def switch_reserve_words(target_word):
    # 変更後の文字列を格納する変数
    res_target_word = ''

    # 正規表現で対象となる予約語を検索し、リストに格納する
    change_words_list = re.findall(r"\${\w+}", target_word)

    # リストに格納された予約語を取り出し、対象に置き換えて行く。
    for change_word in change_words_list:

        # 予約後の${UUID}を変換するメソッド
        if UUID in change_word:
            res_target_word = target_word.replace(change_word, str(uuid.uuid4()))
        if CURRENT_TIMESTAMP in change_word:
            res_target_word = target_word.replace(change_word, datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        if CURRENT_DATE in change_word:
            res_target_word = target_word.replace(change_word, str(datetime.date.today()))
    return res_target_word


def main():
    print("start")

    target = '${CURRENT_DATE}'

    # print(re.sub(r"\${\w+}", target,'test'))
    # print(re.search(r"/\${\w+}/", target))

    if re.search(r"\${\w+}", target) is not None:
        print(switch_reserve_words(target))


if __name__ == "__main__":
    main()
