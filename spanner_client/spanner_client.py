import os
import sys

from google.cloud import spanner
import entity.drippers


def main():
    create_sql("test", "key", "value")
    database_id = 'dev-spanner-trial'
    clint = create_client(database_id)

    dripper_id = "be403e44-2e5a-e5d9-b657-cb21695ee2f7"

    sql = "select * from Drippers "
    opt_sql = f"where DripperId = \"{dripper_id}\""
    main_sql = sql + opt_sql
    print(main_sql)

    with clint.snapshot() as snapshot:
        results = snapshot.execute_sql(main_sql)
        for row in results:
            dripper = entity.drippers.Drippers(row)
            print(dripper.dripperId, dripper.CreatedDripperDate, dripper.CreatedDate)


def create_client(database_id):
    spanner_client = spanner.Client.from_service_account_json(
        '/Users/bandousatoshi/dev/python/zdf_api_autotest/credentials/coffee-376902-8b9b78cacdd6.json')

    instance_id = "trial-cloud-sppaner"

    instance = spanner_client.instance(instance_id)

    return instance.database(database_id)


def search_records(client, sql):
    with client.snapshot() as snapshot:
        results = snapshot.execute_sql(sql)
        return results
    # for row in results:
    #     dripper = Drippers(row)
    #     print(dripper.dripperId, dripper.CreatedDripperDate, dripper.CreatedDate)


def create_sql(table, key, value):
    sql = f'select * from {table} where {key} = \"{value}\"'
    return sql


# class Drippers:
#
# def __init__(self, row):
#     self.dripperId = row[0]
#     self.DripperName = row[1]
#     self.DripperType = row[2]
#     self.CreatedDripperDate = row[3]
#     self.CreatedDate = row[4]
#     self.CreatedUser = row[5]
#     self.UpdatedDate = row[6]
#     self.UpdatedUser = row[7]


if __name__ == "__main__":
    main()
