import datetime


def main():
    test = '2023-05-28 03:03:35.000000+00:00'
    _test = changetoDatetim(test)
    print(_test)


def changetoDatetim(target):
    if target is not None:
        # ミリ秒以降があれば取り除く
        _target = str(target).split(".")[0]
        try:
            # ミリ秒を取り除いたものをUTC時刻からJST時刻に変換する
            return datetime.datetime.strptime(_target, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=9)
        except Exception as e:
            print(e)
            return target


if __name__ == "__main__":
    main()
