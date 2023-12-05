from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from misc.DaemonThrottlingStorage import DaemonThrottlingStorage
from database.database import Database
from asyncio import run

token = '6313687293:AAFuGMCfB5BH-HQ18CoTkFrFDhmRtIhK9i0'
db_url = 'postgresql+asyncpg://znoavxai:Bm92e74No_AQ152T3LpQwZOriBkhfu13@ella.db.elephantsql.com/znoavxai'
admin_link = 'IsHeCoder'

storage = MemoryStorage()
daemon_storage = DaemonThrottlingStorage(ex=10, max=5)

async def init_db():
	return await Database(
		db_url=db_url
	)
db = run(init_db())

dp = Dispatcher(storage=storage)
bot = Bot(
    token=token,
    parse_mode='HTML',
    disable_web_page_preview=True
)