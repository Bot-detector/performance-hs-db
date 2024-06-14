from dataclasses import asdict

from sqlalchemy import (
    JSON,
    Column,
    Date,
    DateTime,
    Integer,
    MetaData,
    Table,
    insert,
    text,
)

from .. import ActivitiesRecord, BenchmarkABC, HiscoreRecord, SkillsRecord, get_session

# Define the table structure
metadata = MetaData()

highscore_data = Table(
    "highscore_data",
    metadata,
    Column("scrape_ts", DateTime, nullable=False),
    Column("scrape_date", Date, nullable=False),
    Column("player_id", Integer, nullable=False),
    Column("skills", JSON, nullable=True),
    Column("activities", JSON, nullable=True),
    primary_key=("player_id", "scrape_date"),
    extend_existing=True,
)


class BenchMark(BenchmarkABC):
    def insert_many_records(self, records: list[HiscoreRecord]) -> None:
        records_to_insert = []

        for record in records:
            record_dict = record.__dict__

            skills: SkillsRecord = record_dict.pop("skills")
            skills: dict = asdict(skills)
            skills = {k: v for k, v in skills.items() if v}

            activities: ActivitiesRecord = record_dict.pop("activities")
            activities: dict = asdict(activities)
            activities = {k: v for k, v in activities.items() if v}

            record_data = {
                "scrape_ts": record.scrape_ts,
                "scrape_date": record.scrape_date,
                "player_id": record.player_id,
                "skills": skills,
                "activities": activities,
            }
            records_to_insert.append(record_data)

        with get_session() as session:
            session.execute(insert(highscore_data), records_to_insert)
            session.commit()

    def get_latest_record_for_player(
        self,
        player_id: int,
    ) -> HiscoreRecord:
        sql = "SELECT * FROM highscore_data WHERE player_id = :player_id ORDER BY scrape_date DESC LIMIT 1"
        with get_session() as session:
            result = session.execute(text(sql), params={"player_id": player_id})
            session.commit()
        return result.first()

    def get_latest_record_for_many_players(
        self,
        players: list[int],
    ) -> list[HiscoreRecord]:
        sql = """
            SELECT *
            FROM highscore_data
            WHERE player_id IN :players
            AND scrape_date IN (
                SELECT MAX(scrape_date)
                FROM highscore_data
                WHERE player_id IN :players
                GROUP BY player_id
            )
        """
        with get_session() as session:
            result = session.execute(text(sql), params={"players": players})
            session.commit()
        return [r._mapping for r in result.fetchall()]

    def get_all_records_for_player(
        self,
        player_id: int,
    ) -> list[HiscoreRecord]:
        sql = "SELECT * FROM highscore_data WHERE player_id = :player_id"
        with get_session() as session:
            result = session.execute(text(sql), params={"player_id": player_id})
            session.commit()
        return [r._mapping for r in result.fetchall()]

    def get_all_records_for_many_players(
        self,
        players: list[int],
    ) -> list[HiscoreRecord]:
        sql = "SELECT * FROM highscore_data WHERE player_id IN :players"
        with get_session() as session:
            result = session.execute(text(sql), params={"players": players})
            session.commit()
        return [r._mapping for r in result.fetchall()]
