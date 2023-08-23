import datetime


def main():
    test = '2023-05-28T03:03:35.45458811Z'
    print(test.split(".")[0])

    a = datetime.datetime.strptime(test.split(".")[0], "%Y-%m-%dT%H:%M:%S")

    compare = datetime.datetime(2023, 5, 28, 3, 3, 35, 4444).replace(microsecond=0)
    print(compare == a)

    print((a))
    print(type(compare))
    print(compare)
    print(isinstance(compare, datetime.datetime))


if __name__ == "__main__":
    main()
