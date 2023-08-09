import jsondiff


def main():
    resultLis = []
    test1 = {"res": "account",
             "res2": ["diec"],
             "res1":
                 {"res": "res",
                  "test": "test"}}
    test2 = {"res": "account",
             "res2": ["diec"],
             "res1":
                 {"res": "res",
                  "test": "tes1"}}

    res = _compare(test1, test2, resultLis)
    print(res)


def compareResponse():
    test1 = {"res": "account", "res2": ["diec"], "res1": {"res": "res", "test": "test"}}
    test2 = {"res": "account", "res2": ["diec"], "res1": {"res": "res", "test": "test"}}

    if len(test1.keys()) == len(test2.keys()):
        for key in test1.keys():
            print(type(test1.get(key)))
            # print(test1.get(str(key)) == test2.get(str(key)))
    else:
        print("notSame")


def _compare(test1, test2, resultList):
    keys = test1.keys()
    for key in keys:
        if isinstance(test1.get(key), dict):
            _compare(test1.get(key), test2.get(key), resultList)
        else:
            #ここで予約後の処理を入れていく
            if test1.get(key) == test2.get(key):
                resultList.append(True)
                print("ok")
            else:
                print("ng")
                resultList.append(False)
    return resultList


if __name__ == "__main__":
    main()
