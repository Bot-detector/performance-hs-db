from datetime import date, datetime

from src import HiscoreRecord
from src.example.main import BenchMark


def test_benchmark():
    bench = BenchMark()
    now = datetime.now()

    # inserting singles
    for _ in range(1000):
        record = HiscoreRecord(
            scrape_ts=now, scrape_date=date.isoformat(now), player_id=1
        )
        bench.insert_many_records(records=[record])

    # easy bench :D
    table_sizes = bench.get_size()
    # Sum up the sizes of all tables
    total_size_mb = sum(row[1] for row in table_sizes)
    print(total_size_mb, table_sizes)
