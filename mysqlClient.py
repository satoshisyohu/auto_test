import mysql.connector


def main():
    ip = '172.20.0.3'

    client = mysql.connector.connect(host=ip, user='root', password='rootpass', database='myDB')
    cursor = client.cursor()
    sql = "select * from users"
    res = cursor.execute(sql)

    print(res)


if __name__ == "__main__":
    main()
    print("end")
