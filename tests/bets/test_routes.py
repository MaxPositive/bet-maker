from tests.conftest import client
from .factories import BetFactory


async def test_create_bet(client):
    data = {
        "event_id": "uid123kf",
        "bet_amount": 1230056.00,
    }
    response = await client.post("/bets", json=data)
    assert 201 == response.status_code
    response_data = response.json()
    assert data["event_id"] == response_data["event_id"]
    assert data["bet_amount"] == response_data["bet_amount"]


async def test_create_bet_errors(client):
    f_err_data = {
        "event_id": "uid123kf",
        "bet_amount": -1230056.00,
    }
    s_err_data = {
        "event_id": "uid123kf",
        "bet_amount": 1230056.003,
    }
    response = await client.post("/bets", json=f_err_data)
    assert 422 == response.status_code
    assert "Input should be greater than 0" in response.json()["detail"][0]["msg"]
    response = await client.post("/bets", json=s_err_data)
    assert 422 == response.status_code
    assert "Bet amount can't have more than 2 decimal places" in response.json()["detail"][0]["msg"]


async def test_get_all_bets(client):
    bets = await BetFactory.create_batch(10)
    response = await client.get("/bets")
    assert 200 == response.status_code
    data = response.json()
    assert 10 == len(data)
    assert data[-1]["event_id"] == bets[-1].event_id


async def test_update_bets_by_event_id(client):
    event_id = "12345"
    await BetFactory.create_batch(5, event_id=event_id)
    data = {"status": "WIN"}
    response = await client.put(f"/events/{event_id}", json=data)
    assert 200 == response.status_code
    response_data = response.json()
    assert 5 == len(response_data)
    assert "WIN" == response_data[-1]["status"]
