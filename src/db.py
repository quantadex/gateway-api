from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase
import os
import datetime
import dsnparse

def get_db():
    url = dsnparse.parse(os.environ.get("DB_URL"))
    db = PooledPostgresqlExtDatabase(
        url.path[1:],
        max_connections=8,
        stale_timeout=300,
        host=url.host,
        password=url.password,
        user=url.username)
    return db

class UserMap(Model):
    account = CharField(primary_key=True)
    public_key = CharField()
    email = CharField()
    created_at = DateField(default=datetime.datetime.now)

    class Meta:
        database = get_db()


def create_user(account: str, pk: str, email:str):
    try:
        found = UserMap.get(UserMap.account == account)
        if found:
            return False
    except UserMap.DoesNotExist:
        user = UserMap(account=account, public_key=pk, email=email)
        return user.save(force_insert=True)

# db = get_db()
# print(db)
# print(create_user("quoc2", "pk", "q@q.com"))
