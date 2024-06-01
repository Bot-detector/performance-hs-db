import json
import os
import random
import time
from datetime import date, datetime, timedelta

from src import HiscoreRecord
from src.example.main import BenchMark

metrics = {
    "test_insert": [],
    "test_get_all_records_for_player": [],
    "test_get_latest_record_for_player": [],
    "test_get_all_records_for_many_players": [],
    "test_get_latest_record_for_many_players": [],
}


def create_test_data(len_players: int = 1_000_000):
    print("creating sample data")
    return {
        player_id: [
            datetime.now() - timedelta(days=i) for i in range(random.randint(0, 60))
        ]
        for player_id in range(len_players)
    }


def create_batch(data: dict, batch_size: int) -> list[HiscoreRecord]:
    players_in_batch = list(data.keys())
    random.shuffle(players_in_batch)
    players_in_batch = players_in_batch[:batch_size]
    batch = []
    for pib in players_in_batch:
        player = data.get(pib)
        if not player:
            data.pop(pib)
            continue
        earliest_record = player[-1]
        data[pib].remove(earliest_record)
        assert earliest_record not in data[pib]
        batch.append(
            HiscoreRecord(
                scrape_ts=earliest_record,
                scrape_date=date.isoformat(earliest_record),
                player_id=pib,
            )
        )
        if data[pib] == []:
            data.pop(pib)
    return batch


players = set()


def test_insert():
    global players
    global metrics

    bench = BenchMark()
    len_players = 10_000

    data = create_test_data(len_players=len_players)
    # inserting singles

    total_records = 100_000
    batch_size = 100
    for i in range(int(total_records / batch_size)):
        batch = create_batch(data=data, batch_size=batch_size)

        bench.insert_many_records(records=batch)

        if i % 10 == 0:
            print(f"{i=}, inserted: {i*batch_size}, players left: {len(data)}")
            metrics["test_insert"].append((i, time.time()))

        for b in batch:
            players.add(b.player_id)
        if len(data) == 0:
            break

    # easy bench :D
    table_sizes = bench.get_size()
    # Sum up the sizes of all tables
    total_size_mb = sum(row[1] for row in table_sizes)
    print(total_size_mb, table_sizes)


def test_get_all_records_for_player():
    global players
    global metrics

    _players = list(players)
    random.shuffle(_players)
    bench = BenchMark()

    for i, player in enumerate(_players[:100]):
        data = bench.get_all_records_for_player(player_id=player)
        if i % 10 == 0:
            metrics["test_get_all_records_for_player"].append((i, time.time()))
    # print("get_all_records_for_player", data[:: len(data) - 1])
    # print("=" * 20)


def test_get_latest_record_for_player():
    global players
    global metrics

    _players = list(players)
    random.shuffle(_players)
    bench = BenchMark()

    for i, player in enumerate(_players[:100]):
        data = bench.get_latest_record_for_player(player_id=player)
        if i % 10 == 0:
            metrics["test_get_latest_record_for_player"].append((i, time.time()))
    # print("get_latest_record_for_player", data)
    # print("=" * 20)


def test_get_all_records_for_many_players():
    global players
    global metrics

    _players = list(players)
    random.shuffle(_players)
    bench = BenchMark()

    batch_size = 10
    for i in range(0, 100, batch_size):
        batch = _players[i : i + batch_size]
        if not batch:
            break
        data = bench.get_all_records_for_many_players(players=batch)
        if i % 10 == 0:
            metrics["test_get_all_records_for_many_players"].append((i, time.time()))
    # print("get_all_records_for_many_players", data[:: len(data) - 1])
    # print("=" * 20)


def test_get_latest_record_for_many_players():
    global players
    global metrics

    _players = list(players)
    random.shuffle(_players)
    bench = BenchMark()

    batch_size = 10
    for i in range(0, 100, batch_size):
        batch = _players[i : i + batch_size]
        if not batch:
            break
        data = bench.get_latest_record_for_many_players(players=batch)
        if i % 10 == 0:
            metrics["test_get_latest_record_for_many_players"].append((i, time.time()))
    # print("get_latest_record_for_many_players", data[:: len(data) - 1])
    # print("=" * 20)


def test_write_to_textfile():
    global metrics
    _file = os.path.basename(__file__).replace(".py", "")
    with open(f"metrics/metrics_{_file}.json", "w") as file:
        json.dump(metrics, file, indent=2)
