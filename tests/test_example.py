# from src.example.main import BenchMark
import importlib
import json
import os
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from uuid import uuid4

from src import BenchmarkABC, HiscoreRecord


@dataclass
class Metric:
    key: str
    value: int
    _time: float
    _id: str
    _implementation: str


@dataclass
class Metrics:
    implementation: str
    metrics: list[Metric] = field(default_factory=list)
    run_id: str = str(uuid4())

    def add(self, key: str, value: int):
        self.metrics.append(
            Metric(
                key=key,
                value=value,
                _time=time.time(),
                _id=self.run_id,
                _implementation=self.implementation,
            )
        )

    def to_jsonl(self):
        _metrics = [m.__dict__ for m in self.metrics]
        _file = os.path.basename(__file__).replace(".py", "")
        # Get the current POSIX timestamp
        ts = int(time.time())
        # Set hours, minutes, and seconds to zero to get the start of the day timestamp
        ts = ts - (ts % 86400)
        file_path = f"metrics/{ts}_{_file}_metrics.jsonl"
        with open(file_path, "a") as file:
            for _metric in _metrics:
                file.write(json.dumps(_metric) + "\n")


module = importlib.import_module("src.example.main")
BenchMark: BenchmarkABC = getattr(module, "BenchMark")
# my_instance = my_class()

metrics = Metrics(implementation="example")


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
        batch = data_to_batch(data=data, batch_size=batch_size)

        bench.insert_many_records(records=batch)

        if i % 10 == 0:
            print(f"{i=}, inserted: {i*batch_size}, players left: {len(data)}")
            metrics.add("test_insert", i)

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
        _ = bench.get_all_records_for_player(player_id=player)

        if i % 10 == 0:
            metrics.add("test_get_all_records_for_player", i)


def test_get_latest_record_for_player():
    global players
    global metrics

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

    metrics.to_jsonl()
