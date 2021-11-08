from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Column, MetaData, String)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

POSTGRESQL_URL = 'postgresql+psycopg2://User:TparLnA7A665zC6f@173.249.16.9:5434/mariia_test'

metadata = MetaData()


class BusinessRow(Base):
    __tablename__ = 'business_number_data'
    title = Column(String, nullable=False, primary_key=True)
    site = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    work_hours = Column(String, nullable=False)
    address = Column(String, nullable=False)


class Database:
    def __init__(self):
        self.engine = create_engine(POSTGRESQL_URL)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)

    def save_business_data(self, business_number_data: BusinessRow):
        session = self.session()
        session.merge(business_number_data)
        session.commit()
