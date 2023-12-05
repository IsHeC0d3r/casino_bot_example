from typing import Any, Awaitable, Callable, Dict, Optional, Set
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update

from loader import db

class DB(BaseMiddleware):
	async def __call__(
		self,
		handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
		event: Update,
		data: Dict[str, Any]
	) -> Any:
		async with db.session() as session:
			data['db'] = session
		handler = await handler(event, data)
		if data['db']:
			await data['db'].commit()
			await data['db'].close()
			del data['db']
		return handler
	
	def setup(
		self: BaseMiddleware, router: Dispatcher, exclude: Optional[Set[str]] = None
	) -> BaseMiddleware:
		"""
		Register middleware for all events in the Router

		:param router:
		:param exclude:
		:return:
		"""
		if exclude is None:
			exclude = set()
		exclude_events = {"update", *exclude}
		for event_name, observer in router.observers.items():
			if event_name in exclude_events:
				continue
			observer.outer_middleware(self)
		return self