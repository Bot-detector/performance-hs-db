from dataclasses import asdict

from sqlalchemy import (
    insert,
    text,
)

from .. import ActivitiesRecord, BenchmarkABC, HiscoreRecord, SkillsRecord, get_session


class BenchMark(BenchmarkABC):
    def insert_many_records(self, records: list[HiscoreRecord]) -> None: ...

    def get_latest_record_for_player(
        self,
        player_id: int,
    ) -> HiscoreRecord: ...

    def get_latest_record_for_many_players(
        self,
        players: list[int],
    ) -> list[HiscoreRecord]: ...

    def get_all_records_for_player(
        self,
        player_id: int,
    ) -> list[HiscoreRecord]: ...

    def get_all_records_for_many_players(
        self,
        players: list[int],
    ) -> list[HiscoreRecord]: ...
