from .. import BenchmarkABC, HiscoreRecord


class ExampleBenchMark(BenchmarkABC):
    def insert_many_records(self, records: list[HiscoreRecord]) -> None:
        return super().insert_many_records(records)

    def get_latest_record_for_player(
        self,
        player_id: int,
    ) -> HiscoreRecord:
        return super().get_latest_record_for_player(player_id)

    def get_latest_record_for_many_players(
        self,
        players: list[int],
    ) -> list[HiscoreRecord]:
        return super().get_latest_record_for_many_players(players)

    def get_all_records_for_player(
        self,
        player_id: int,
    ) -> list[HiscoreRecord]:
        return super().get_all_records_for_player(player_id)

    def get_all_records_for_many_players(
        self,
        players: list[int],
    ) -> list[HiscoreRecord]:
        return super().get_all_records_for_many_players(players)
