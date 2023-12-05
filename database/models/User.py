from sqlalchemy import Column, Integer, BigInteger, DateTime
from datetime import datetime

from ..base import Base

class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
	telegram = Column(BigInteger)
	balance = Column(BigInteger, default=0)
	admin_lvl = Column(Integer, default=1)
	status = Column(Integer, default=0)
	banned = Column(Integer, default=0)
	time = Column(DateTime, default=datetime.utcnow)