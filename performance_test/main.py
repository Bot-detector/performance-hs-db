import importlib
import os
import random
import sys
import time
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from performance_test.metrics import Metrics  # noqa: E402
from src import (  # noqa: E402
    ActivitiesRecord,
    BenchmarkABC,
    HiscoreRecord,
    SkillsRecord,
)

players = set()


def create_batch(data: list, batch_size: int):
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


def batch_data(data: dict[str, list[datetime]], batch_size: int) -> list[HiscoreRecord]:
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

        skills = SkillsRecord()
        skills.random()

        activities = ActivitiesRecord()
        activities.random()

        record = HiscoreRecord(
            scrape_ts=earliest_record,
            scrape_date=earliest_record.isoformat(),
            player_id=player_id,
            skills=skills,
            activities=activities,
        )
        batch.append(record)

        if not records:
            data.pop(player_id)

    return batch


def insert_data(
    data: dict,
    bench: BenchmarkABC,
    metrics: Metrics,
    batch_size: int,
    iterations: int,
    players: set,
):
    for i in range(iterations):
        batch = batch_data(data=data, batch_size=batch_size)

        start_time = time.time()
        bench.insert_many_records(records=batch)
        duration = int((time.time() - start_time) * 1000)
        metrics.add(f"test_insert_duration_ms_{batch_size}", duration)
        metrics.add(f"test_insert_{batch_size}", i * batch_size)

        if i * batch_size % 1000 == 0:
            print(f"{i=}, inserted: {i*batch_size}, players left: {len(data)}")

        for b in batch:
            players.add(b.player_id)

        if len(data) == 0:
            break
    return players


def get_total_size(bench: BenchmarkABC, metrics: Metrics):
    table_sizes = bench.get_size()
    total_size_mb = sum(row[1] for row in table_sizes)
    print(f"{total_size_mb=}, {table_sizes=}")
    metrics.add("total_size_mb", str(total_size_mb))
    return


def get_all_records(
    bench: BenchmarkABC,
    metrics: Metrics,
    players: set,
    iterations: int = 100,
):
    _players = list(players)
    random.shuffle(_players)

    for i, player in enumerate(_players[:iterations]):
        start_time = time.time()
        _ = bench.get_all_records_for_player(player_id=player)
        duration = int((time.time() - start_time) * 1000)
        metrics.add("get_all_records", i)
        metrics.add("get_all_records_duration_ms", duration)


def get_latest_record(
    bench: BenchmarkABC,
    metrics: Metrics,
    players: set,
    iterations: int = 100,
):
    _players = list(players)
    random.shuffle(_players)

    for i, player in enumerate(_players[:iterations]):
        start_time = time.time()
        _ = bench.get_latest_record_for_player(player_id=player)
        duration = int((time.time() - start_time) * 1000)
        metrics.add("get_latest_record", i)
        metrics.add("get_latest_record_duration_ms", duration)


def get_all_records_batch(
    bench: BenchmarkABC,
    metrics: Metrics,
    players: set,
    iterations: int = 100,
    batch_size: int = 10,
):
    _players = list(players)
    random.shuffle(_players)

    batch_gen = create_batch(_players, batch_size)
    for i, batch in enumerate(batch_gen):
        if i >= iterations:
            break
        if not batch:
            break

        start_time = time.time()
        x = bench.get_all_records_for_many_players(players=batch)
        duration = int((time.time() - start_time) * 1000)
        if i % 10 == 0:
            print(
                x[0].get("player_id"),
                x[0].get("scrape_date"),
                x[-1].get("player_id"),
                x[-1].get("scrape_date"),
            )
        metrics.add("get_all_records_batch", i)
        metrics.add(f"get_all_records_batch_duration_ms_{batch_size}", duration)


def get_latest_record_batch(
    bench: BenchmarkABC,
    metrics: Metrics,
    players: set,
    iterations: int = 100,
    batch_size: int = 10,
):
    _players = list(players)
    random.shuffle(_players)

    batch_gen = create_batch(_players, batch_size)
    for i, batch in enumerate(batch_gen):
        if i >= iterations:
            break
        if not batch:
            break

        start_time = time.time()
        x = bench.get_latest_record_for_many_players(players=batch)
        duration = int((time.time() - start_time) * 1000)
        metrics.add("get_latest_record_batch", i)
        metrics.add(f"get_latest_record_batch_duration_ms_{batch_size}", duration)


def metrics_to_file(metrics: Metrics):
    metrics.to_jsonl(file=__file__)


if __name__ == "__main__":
    LEN_PLAYERS = 100_000
    implementation = input("implementation: ") # TODO: take argument
    metrics = Metrics(implementation=implementation)
    module = importlib.import_module(f"src.{implementation}.main")
    benchmark: BenchmarkABC = getattr(module, "BenchMark")
    benchmark = benchmark()

    data = create_test_data(len_players=LEN_PLAYERS)
    players = set()
    batches = [(100_000, 1), (10, 10_000), (100, 1000), (1_000, 100), (10_000, 10)]
    for batch_size, iterations in batches:
        print(f"{len(players)=}, {batch_size=}, {iterations=}")
        players = insert_data(
            bench=benchmark,
            metrics=metrics,
            data=data,
            batch_size=batch_size,
            iterations=iterations,
            players=players,
        )

    get_total_size(bench=benchmark, metrics=metrics)
    get_all_records(
        bench=benchmark,
        metrics=metrics,
        players=players,
        iterations=100,
    )
    get_all_records_batch(
        bench=benchmark,
        metrics=metrics,
        players=players,
        iterations=100,
        batch_size=5000,
    )
    get_latest_record(
        bench=benchmark,
        metrics=metrics,
        players=players,
        iterations=100,
    )
    get_latest_record_batch(
        bench=benchmark,
        metrics=metrics,
        players=players,
        iterations=100,
        batch_size=5000,
    )
    metrics_to_file(metrics=metrics)
