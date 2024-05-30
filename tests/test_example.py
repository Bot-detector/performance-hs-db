from datetime import date, datetime

from src import HiscoreRecord
from src.example.main import BenchMark


def test_benchmark():
    now = datetime.now()
    record = HiscoreRecord(scrape_ts=now, scrape_date=date.isoformat(now), player_id=1)
    bench = BenchMark()
    bench.insert_many_records(records=[record])
