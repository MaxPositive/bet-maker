import factory

from src.utils import faker
from src.pkgs.db.engine import sessionmanager
from src.pkgs.db.tables import Bet


class AsyncFactory(factory.alchemy.SQLAlchemyModelFactory):
    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        async with sessionmanager.session() as session:
            session.add(obj)
            await session.commit()
        return obj

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]


class BetFactory(AsyncFactory):
    class Meta:
        model = Bet

    id = factory.Sequence(lambda n: n)
    event_id = factory.LazyAttribute(lambda e: str(faker.random_number()))
    bet_amount = factory.LazyAttribute(
        lambda n: faker.pydecimal(left_digits=10, right_digits=2, positive=True)
    )
    status = "Not played"
