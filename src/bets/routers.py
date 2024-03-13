from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.bets.schemas import BetSchema, BetCreateSchema, BetUpdateSchema

from src.pkgs.db.engine import get_db

from .services import set_bet_to_database, get_all_bets, update_bet_by_event_id

router = APIRouter(tags=["Bets"])


@router.post("/bets", status_code=status.HTTP_201_CREATED, response_model=BetSchema)
async def create_bet(data: BetCreateSchema, session: AsyncSession = Depends(get_db)):
    result = await set_bet_to_database(data=data, session=session)
    return result


@router.get("/bets", response_model=list[BetSchema])
async def get_bets(session: AsyncSession = Depends(get_db)):
    result = await get_all_bets(session=session)
    return result


@router.put("/events/{event_id}", response_model=list[BetSchema])
async def update_bet(event_id: str, data: BetUpdateSchema, session: AsyncSession = Depends(get_db)):
    result = await update_bet_by_event_id(event_id=event_id, data=data, session=session)
    return result
