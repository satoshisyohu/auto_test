import re
import uuid
import datetime

# 予約後変数

# uuid
UUID = '${UUID}'

# timestamp
CURRENT_TIMESTAMP = '${CURRENT_TIMESTAMP}'
SPANNER_TIMESTAMP_PLUS_MINUS = '${CURRENT_TIMESTAMP'

CURRENT_DATE = '${CURRENT_DATE}'
CURRENT_DATE_PLUS_MINUS = '${CURRENT_DATE'


# 予め予約されている変数を置き換える処理。
# 指定できる予約後はReadme を参照すること

def switch_reserve_words(target_word):
    print(target_word)
    # 変更後の文字列を格納する変数
    res_target_word = ''

    # 正規表現で対象となる予約語を検索し、リストに格納する
    change_words_list = re.findall(r"^\${[a-zA-Z0-9-+_]+}", target_word)

    # リストに格納された予約語を取り出し、対象に置き換えて行く。
    for change_word in change_words_list:

        # 予約後の${UUID}を変換するメソッド
        if UUID in change_word:
            res_target_word = target_word.replace(change_word, str(uuid.uuid4()))
        elif CURRENT_TIMESTAMP in change_word:
            res_target_word = target_word.replace(change_word, datetime.datetime.now().isoformat())
        elif CURRENT_DATE in change_word:
            res_target_word = target_word.replace(change_word, datetime.date.today().isoformat())

        elif SPANNER_TIMESTAMP_PLUS_MINUS in change_word:
            editedTargetWord = str(change_word).replace("${CURRENT_TIMESTAMP", "").replace("}", "")
            now = datetime.datetime.now()
            res_target_word = changeTime(editedTargetWord, now)

        elif CURRENT_DATE_PLUS_MINUS in change_word:
            editedTargetWord = str(change_word).replace("${CURRENT_DATE", "").replace("}", "")
            now = datetime.date.today()
            res_target_word = changeTime(editedTargetWord, now)

    return res_target_word


def changeTime(target, now):
    if "-" in target:
        days = target.replace("-", "")
        targetTime = now - datetime.timedelta(days=int(days))
    else:
        days = target.replace("+", "")
        targetTime = now + datetime.timedelta(days=int(days))
    return targetTime.isoformat()


def main():
    print("start")

    target = '${UUID}'

    # print(re.sub(r"\${\w+}", target,'test'))
    # print(re.search(r"/\${\w+}/", target)ß)

    if re.search(r"^\${[a-zA-Z0-9-+_]+}", target) is not None:
        print(switch_reserve_words(target))


if __name__ == "__main__":
    main()
