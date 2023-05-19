from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db

#POSTGRESSQL_URL = "postgresql+psycopg2://username:password@localhost/database_name"@
MYSQL_URL = "mysql+pymysql://root:@localhost:3306/otu_fastapi?charset=utf8"
#MYSQL_URL = "mysql+pymysql://root:Openforme@localhost:3306/fastapi_student_results?charset=utf8"
POOL_SIZE = 20
POOL_RECYCLE = 3600
POOL_TIMEOUT = 15
MAX_OVERFLOW = 2
CONNECT_TIMEOUT = 60

metadata_obj = MetaData()

engine = create_engine(MYSQL_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





class Database():
    def __init__(self) -> None:
        self.connection_is_active = False
        self.engine = None

    def get_db_connection(self):
        if self.connection_is_active == False:
            connect_args = {"connect_timeout":CONNECT_TIMEOUT}
            try:
                self.engine = create_engine(MYSQL_URL, pool_size=POOL_SIZE, pool_recycle=POOL_RECYCLE,
                        pool_timeout=POOL_TIMEOUT, max_overflow=MAX_OVERFLOW, connect_args=connect_args)
                return self.engine
            except Exception as ex:
                print("Error connecting to DB : ", ex)
        return self.engine

    def get_db_session(self,engine):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            return session
        except Exception as ex:
            print("Error getting DB session : ", ex)
            return None