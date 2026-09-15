from sqlalchemy import Integer, String, Column, Text
from db.db_engine import Base
from sqlalchemy import func
class User_Info(Base):
    __tablename__="UserInfo"
    userid = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String, primary_key=False, unique=True, nullable=False)
    hashedpassword = Column(Text, primary_key=False, nullable=False)
    role = Column(String, primary_key=False, nullable=False, default="user")
    createdon = Column(String, primary_key=False, server_default=func.current_timestamp())

#class for maintaining uploaded document hash to avoid duplicate processing
class Document_Hash(Base):
    __tablename__="DocumentHash"
    docid = Column(Integer, autoincrement=True, primary_key=True)
    doc_hash = Column(String, primary_key=False, unique=True, nullable=False)
    filename = Column(String, primary_key=False, nullable=False)
    createdon = Column(String, primary_key=False, server_default=func.current_timestamp())

class MessageHistory(Base):
    __tablename__="MessageHistory"
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String, primary_key=False, unique=False, nullable=False)
    human = Column(String, primary_key=False, unique=False, nullable=False)
    ai = Column(String, primary_key=False, unique=False, nullable=False)
    generatedon = Column(String, primary_key=False, server_default=func.current_timestamp())