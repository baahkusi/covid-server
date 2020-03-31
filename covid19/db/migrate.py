from playhouse.migrate import *
from ..config import db
from .auth import *
# initialize migrator
migrator = PostgresqlMigrator(db)

migrations = [
]

if __name__ == "__main__":
    if migrations:
        try:
            print('Loading Migrations ...')
            with db.transaction():
                migrate(*migrations)
            print('Migrations Successfully Completed.')
        except Exception as e:
            print(e)
    else:
        print("No migrations specified ...")
