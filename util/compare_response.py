import jsondiff


def main():
    compareResponse()


def compareResponse():
    test1 = {"res": "account", "res2": ["diec"]}
    test2 = {"res": "account", "res2": {"diec"}}

    if len(test1.keys()) == len(test2.keys()):
        for key in test1.keys():
            print(type(test1.get(key)))
            # print(test1.get(str(key)) == test2.get(str(key)))
    else:
        print("notSame")


if __name__ == "__main__":
    main()
