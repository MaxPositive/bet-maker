from pydantic import BaseModel, PositiveFloat, field_validator


class BetCreateSchema(BaseModel):
    event_id: str
    bet_amount: PositiveFloat

    @field_validator(mode="before", __field="bet_amount")
    def check_bet_amount(cls, value):
        if len(str(value).split(".")[1]) > 2:
            raise ValueError("Bet amount can't have more than 2 decimal places")
        return value


class BetUpdateSchema(BaseModel):
    status: str


class BetSchema(BaseModel):
    event_id: str
    bet_amount: PositiveFloat
    status: str
