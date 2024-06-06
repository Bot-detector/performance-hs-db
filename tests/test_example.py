# from src.example.main import BenchMark
import importlib
import random
from datetime import datetime, timedelta

from src import BenchmarkABC, HiscoreRecord

from .metrics import Metrics

module = importlib.import_module("src.example.main")
BenchMark: BenchmarkABC = getattr(module, "BenchMark")
metrics = Metrics(implementation="example")
players = set()


def batch_data(data: list, batch_size: int):
    """
    Generator to yield batches from a list of data.

    :param data: List of input data
    :param batch_size: Size of each batch
    :yield: Batches of data
    """
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]


def create_test_data(len_players: int = 1_000_000):
    print("creating sample data")
    return {
        player_id: [
            datetime.now() - timedelta(days=i) for i in range(random.randint(0, 60))
        ]
        for player_id in range(len_players)
    }


def data_to_batch(
    data: dict[str, list[datetime]], batch_size: int
) -> list[HiscoreRecord]:
    players = list(data.keys())
    random.shuffle(players)
    selected_players = players[:batch_size]
    batch = []

    for player_id in selected_players:
        records = data.get(player_id)
        if not records:
            data.pop(player_id, None)
            continue

        earliest_record = records.pop(-1)

        batch.append(
            HiscoreRecord(
                scrape_ts=earliest_record,
                scrape_date=earliest_record.isoformat(),
                player_id=player_id,
            )
        )

        if not records:
            data.pop(player_id)

    return batch


def test_insert():
    global players
    global metrics
    global BenchMark

    bench = BenchMark()
    len_players = 10_000

    data = create_test_data(len_players=len_players)
    # inserting singles

    total_records = 100_000
    batch_size = 100

    for i in range(int(total_records / batch_size)):
        batch = data_to_batch(data=data, batch_size=batch_size)

        bench.insert_many_records(records=batch)

        if i % 10 == 0:
            print(f"{i=}, inserted: {i*batch_size}, players left: {len(data)}")
            metrics.add("test_insert", i)

        for b in batch:
            players.add(b.player_id)
        if len(data) == 0:
            break


def test_get_all_records_for_player():
    global players
    global metrics
    global BenchMark

    _players = list(players)
    random.shuffle(_players)
    bench = BenchMark()

    for i, player in enumerate(_players[:100]):
        _ = bench.get_all_records_for_player(player_id=player)

        if i % 10 == 0:
            metrics.add("test_get_all_records_for_player", i)


def test_get_latest_record_for_player():
    global players
    global metrics
    global BenchMark

    _players = list(players)
    random.shuffle(_players)
    bench = BenchMark()

    for i, player in enumerate(_players[:100]):
        _ = bench.get_latest_record_for_player(player_id=player)

        if i % 10 == 0:
            metrics.add("test_get_latest_record_for_player", i)


def test_get_all_records_for_many_players():
    global players
    global metrics
    global BenchMark

    _players = list(players)
    random.shuffle(_players)
    bench = BenchMark()

    batch_size = 10
    for i in range(0, 100, batch_size):
        batch = _players[i : i + batch_size]
        if not batch:
            break
        _ = bench.get_all_records_for_many_players(players=batch)

        if i % 10 == 0:
            metrics.add("test_get_all_records_for_many_players", i)


def test_get_latest_record_for_many_players():
    global players
    global metrics
    global BenchMark

    _players = list(players)
    random.shuffle(_players)
    bench = BenchMark()

    batch_size = 10
    for i in range(0, 100, batch_size):
        batch = _players[i : i + batch_size]
        if not batch:
            break
        _ = bench.get_latest_record_for_many_players(players=batch)

        if i % 10 == 0:
            metrics.add("test_get_latest_record_for_many_players", i)


def test_write_to_file():
    global metrics

    metrics.to_jsonl(file=__file__)
