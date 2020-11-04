from datetime import datetime

from peewee import *


dbhandle = SqliteDatabase("Team1C.db")


class BaseModel(Model):
    class Meta:
        database = dbhandle


class User(BaseModel):
    id = CharField()
    current_question = IntegerField()
    rigth_answer_count = IntegerField()
    is_admin = BooleanField(default=False)
    answer_lock = BooleanField(default=False)
    # self.current_test = "dev/null"

    class Meta:
        db_table = "users"


class Test(BaseModel):
    id = CharField()
    current_question = IntegerField()
    rigth_answer_count = IntegerField()

    class Meta:
        db_table = "test"


class UserTests(BaseModel):
    User = ForeignKeyField(User, backref='user_tests')
    Test = ForeignKeyField(Test, backref='user_tests')


class TestResult(BaseModel):
    user = ForeignKeyField(User, backref='user')
    date = DateTimeField(default=datetime.now())
    result = IntegerField()

    class Meta:
        db_table = 'test_result'
        order_by = ('date',)


def getUserById(user_id):
    return User.select().where(User.id == user_id).get()


def getLastUserResult(user_id):
    try:
        tr = TestResult.select().where(TestResult.user == getUserById(user_id)).order_by(TestResult.date.desc()).get()
    except DoesNotExist:
        return -1
    return tr.result

def getAdminList():
    al = []
    for admin in User.select().where(User.is_admin == True):
        al.append(admin)
    return al


if __name__ == '__main__':
    try:
        dbhandle.connect()
        User.create_table()
        Test.create_table()
        TestResult.create_table()
        UserTests.create_table()
    except InternalError as px:
        print(str(px))
