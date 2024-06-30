import importlib
import os
import random
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src import (  # noqa: E402
    ActivitiesRecord,
    BenchmarkABC,
    HiscoreRecord,
    SkillsRecord,
)

random.seed(42)

players = set()


def create_test_data(
    len_players: int = 1_000, max_len_days=60
) -> dict[str, list[datetime]]:
    print("creating sample data")
    return {
        player_id: [
            datetime.now() - timedelta(days=i)
            for i in range(random.randint(0, max_len_days))
        ]
        for player_id in range(len_players)
    }


def create_test_batch(
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

        skills = SkillsRecord()
        skills.random()

        activities = ActivitiesRecord()
        activities.random()

        record = HiscoreRecord(
            scrape_ts=earliest_record,
            scrape_date=earliest_record.date(),
            player_id=player_id,
            skills=skills,
            activities=activities,
        )
        batch.append(record)

        if not records:
            data.pop(player_id)

    return batch


def test_e2e():
    implementation = os.environ.get("implementation")
    if not implementation:
        implementation = input("implementation: ")

    module = importlib.import_module(f"src.{implementation}.main")
    bench: BenchmarkABC = getattr(module, "BenchMark")
    bench = bench()

    test_data = create_test_data(len_players=1_000)
    batch = create_test_batch(data=test_data, batch_size=10)
    bench.insert_many_records(records=batch)
