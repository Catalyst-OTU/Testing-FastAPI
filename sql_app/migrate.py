from passlib.context import CryptContext
from sqlalchemy import text
import schemas
from database import Database, Base, engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)



# SEEDING USER DATA INTO DATABASE

# db_addUser = schemas.User()
# db_addUser.email = "admin@admin.com"
# db_addUser.username = "Super Admin"
# db_addUser.hashed_password = pwd_context.hash("password")
# db_addUser.status = "Active"
# db.add(db_addUser)

# db.flush()
# db.commit()
# db.close()
