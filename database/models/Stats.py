from sqlalchemy import Column, Integer, BigInteger, String

from ..base import Base

class Stats(Base):
	__tablename__ = 'stats'
	
	id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
	participant_1 = Column(BigInteger)
	participant_2 = Column(BigInteger)
	game = Column(String)
	bet = Column(Integer)
	winner = Column(BigInteger, default=-1)