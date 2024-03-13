from typing import Any

from sqlalchemy import insert, update, select

from sqlalchemy.ext.asyncio import AsyncSession

from src.pkgs.db.engine import fetch_all, fetch_one

from src.pkgs.db.tables import Bet

from src.bets.schemas import BetCreateSchema, BetUpdateSchema


async def set_bet_to_database(data: BetCreateSchema, session: AsyncSession) -> dict[str, Any]:
    stmt = (
        insert(Bet)
        .values(
            {
                "event_id": data.event_id,
                "bet_amount": data.bet_amount,
            }
        )
        .returning(Bet)
    )
    result = await session.execute(stmt)
    await session.commit()
    return await fetch_one(result)


async def get_all_bets(session: AsyncSession) -> list[dict[str, Any]]:
    stmt = select(Bet)
    result = await session.execute(stmt)
    return await fetch_all(result)


async def update_bet_by_event_id(
    event_id: str, data: BetUpdateSchema, session: AsyncSession
) -> list[dict[str, Any]]:
    stmt = update(Bet).where(Bet.event_id == event_id).values(status=data.status).returning(Bet)
    result = await session.execute(stmt)
    await session.commit()
    return await fetch_all(result)
