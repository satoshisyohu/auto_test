def check_type():
    test = {"values": {"test": "test"}}

    test1 = {"values": "aaaa",
             "values1": "bbb",
             "valuee1":[
                 {"json1":
                    {"a":"b"}},
                 {"json2":
                      {"a":"b"}}],
             "valuee2":[
                 {"json1":
                      {"a":"b"}},
                 {"json2":
                      {"a":"b"}}]}


    test2 = {"values": "aaaa",
             "values1": "bbb",
             "valuee2":[
                 {"json1":
                      {"a":"b"}},
                 {"json2":
                      {"a":"b"}}],
             "valuee1":[
                 {"json1":
                      {"a":"b"}},
                 {"json2":
                      {"a":"b"}}]}
    # typeによって見分けて行くしかないかな。
    #　自分用メモ、pythonに関してはdictの順番が異なっていても一致する。配列の順序違いはng
    if test1 == test2:
        print("ok")
    else:
        print("ng")


def main():
    check_type()


if __name__ == "__main__":
    main()
