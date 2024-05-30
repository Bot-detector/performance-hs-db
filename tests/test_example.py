import random
from datetime import date, datetime, timedelta

from src import HiscoreRecord
from src.example.main import BenchMark

random.seed(7)


def create_test_data(len_players: int = 1_000_000):
    print("creating sample data")
    return {
        player_id: [
            datetime.now() - timedelta(days=i) for i in range(random.randint(0, 60))
        ]
        for player_id in range(len_players)
    }


def create_batch(data: dict, batch_size: int) -> list[HiscoreRecord]:
    print("creating batch")
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
    bench = BenchMark()
    len_players = 10_000

    data = create_test_data(len_players=len_players)
    # inserting singles

    total_records = 100_000
    batch_size = 100
    for i in range(int(total_records / batch_size)):
        print(f"{i=}, inserted: {i*batch_size}, players left: {len(data)}")
        batch = create_batch(data=data, batch_size=batch_size)

        bench.insert_many_records(records=batch)
        for b in batch:
            players.add(b.player_id)
        if len(data) == 0:
            break

    # easy bench :D
    table_sizes = bench.get_size()
    # # Sum up the sizes of all tables
    total_size_mb = sum(row[1] for row in table_sizes)
    print(total_size_mb, table_sizes)


def test_get_latest_record_for_player():
    global players
    _players = list(players)
    bench = BenchMark()

    data = bench.get_all_records_for_player(player_id=_players[0])
    print(data)
    data = bench.get_latest_record_for_player(player_id=_players[0])
    print(data)
    data = bench.get_all_records_for_many_players(players=_players[:10])
    print(data)
    data = bench.get_latest_record_for_many_players(players=_players[:10])
    print(data)
