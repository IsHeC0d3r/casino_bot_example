from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import update
from database.models.User import User
from database.models.Stats import Stats

async def add_balance(db: AsyncSession, id: int, add: int) -> None:

    await db.execute(
        update(User).where(
            User.telegram == id
        ).values(balance = User.balance + add)
    )

async def insert_winner(db: AsyncSession, id: int, winner: int) -> None:
    await db.execute(update(Stats).where(
        (
            (Stats.participant_1 == id) |
            (Stats.participant_2 == id)
        ) &
        (Stats.winner == -1)).values(winner = winner)
    )
    if id == winner:
        await add_balance(
            db=db,
            id=id,
            add=85
        )
    else:
        await add_balance(
            db=db,
            id=id,
            add=-100
        )