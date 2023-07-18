import dataclasses
import datetime


class Drippers:
    dripperId: str
    dripperName: str
    dripperType: str
    createdDripperDate: datetime.date
    createdDate: datetime
    createdUser: str
    updatedDate: datetime
    updatedUser: str

    def __init__(self, entity):
        self.dripperId = entity[0] + "test"
        self.dripperName = entity[1]
        self.DripperType = entity[2]
        self.createdDripperDate = entity[3]
        self.createdDate = entity[4]
        self.createdUser = entity[5]
        self.updatedDate = entity[6]
        self.updatedUser = entity[7]


def main():
        u =Drippers()

if __name__ == "__main__":
    main()
