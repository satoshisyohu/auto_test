import math
import re
import uuid
import datetime

# 予約後変数

# uuid
UUID = '${UUID}'

# timestamp
CURRENT_TIMESTAMP = '${CURRENT_TIMESTAMP}'
CURRENT_TIMESTAMP_PLUS_MINUS = '${CURRENT_TIMESTAMP'

CURRENT_DATE = '${CURRENT_DATE}'
CURRENT_DATE_PLUS_MINUS = '${CURRENT_DATE'

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


# 予め予約されている変数を置き換える処理。
# 指定できる予約後はReadme を参照すること

def switch_reserve_words(target_word):
    print(target_word)
    # 変更後の文字列を格納する変数
    res_target_word = ''

    # 正規表現で対象となる予約語を検索し、リストに格納する
    change_words_list = re.findall(r"^\${[a-zA-Z0-9-+_.]+}", target_word)

    # リストに格納された予約語を取り出し、対象に置き換えて行く。
    for change_word in change_words_list:

        # 予約後の${UUID}を変換するメソッド
        if UUID in change_word:
            res_target_word = target_word.replace(change_word, str(uuid.uuid4()))
        elif CURRENT_TIMESTAMP in change_word:
            res_target_word = target_word.replace(change_word,
                                                  datetime.datetime.now(JST).isoformat(timespec='milliseconds'))
        elif CURRENT_DATE in change_word:
            res_target_word = target_word.replace(change_word, datetime.date.today().isoformat())

        elif CURRENT_TIMESTAMP_PLUS_MINUS in change_word:
            editedTargetWord = str(change_word).replace(CURRENT_TIMESTAMP_PLUS_MINUS, "").replace("}", "")
            now = datetime.datetime.now(JST)
            res_target_word = changeTime(editedTargetWord, now)

        elif CURRENT_DATE_PLUS_MINUS in change_word:
            editedTargetWord = str(change_word).replace(CURRENT_DATE_PLUS_MINUS, "").replace("}", "")
            now = datetime.date.today()
            res_target_word = changeTime(editedTargetWord, now)
        else:
            res_target_word = change_word

    return res_target_word


def changeTime(target, now):
    if "-" in target:
        days = target.replace("-", "")
        if '.' in days:
            targetTime = dealFloat(days, now)
        else:
            targetTime = now - datetime.timedelta(days=int(days))
    else:
        days = target.replace("+", "")
        if '.' in days:
            targetTime = dealFloat(days, now)
        else:
            targetTime = now + datetime.timedelta(days=int(days))
    return targetTime.isoformat(timespec='milliseconds')


def dealFloat(target, now):
    hour = math.floor(float(target) * 24)
    return now + datetime.timedelta(hours=int(hour))


def main():
    print("start")

    target = '${CURRENT_DATE}'

    # print(re.sub(r"\${\w+}", target,'test'))
    # print(re.search(r"/\${\w+}/", target)ß)

    if re.search(r"^\${[a-zA-Z0-9-+_.]+}", target) is not None:
        print(switch_reserve_words(target))


if __name__ == "__main__":
    main()
