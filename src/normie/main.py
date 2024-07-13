# import logging
from dataclasses import asdict, dataclass
from datetime import date, datetime

import sqlalchemy as sqla
from sqlalchemy.orm import Session

from .. import BenchmarkABC, HiscoreRecord, get_session


@dataclass
class ScraperPlayerSkill:
    skill_id: int
    skill_value: int
    scrape_ts: datetime
    scrape_date: date
    player_id: int


@dataclass
class ScraperPlayerActivity:
    activity_id: int
    activity_value: int
    scrape_ts: datetime
    scrape_date: date
    player_id: int


@dataclass
class ScraperRecord:
    skill_id: int
    skill_value: int
    activity_id: int
    activity_value: int
    scrape_ts: datetime
    scrape_date: date
    player_id: int


def bulk_normalized_insert(
    session: Session,
    skills: list[ScraperPlayerSkill],
    activities: list[ScraperPlayerActivity],
):
    # create temp (staging) tables
    sql_create_temp_skills = """
        CREATE TEMPORARY TABLE temp_skill (
            skill_id TINYINT, 
            skill_value INT, 
            scrape_ts DATETIME, 
            scrape_date DATE, 
            player_id INT
        ) ENGINE=MEMORY;
    """
    sql_create_temp_activities = """
        CREATE TEMPORARY TABLE temp_activity (
            activity_id TINYINT, 
            activity_value INT, 
            scrape_ts DATETIME, 
            scrape_date DATE, 
            player_id INT
        ) ENGINE=MEMORY;
    """
    # insert into temp (staging) tables
    sql_insert_temp_skills = """
        INSERT INTO temp_skill (skill_id, skill_value, scrape_ts, scrape_date, player_id) 
        VALUES (:skill_id, :skill_value, :scrape_ts, :scrape_date, :player_id);
    """
    sql_insert_temp_activities = """
        INSERT INTO temp_activity (activity_id, activity_value, scrape_ts, scrape_date, player_id) 
        VALUES (:activity_id, :activity_value, :scrape_ts, :scrape_date, :player_id);
    """

    # insert into the normalized tables
    sql_insert_pl_skill = """
        INSERT IGNORE INTO player_skill (skill_id, skill_value)
        SELECT DISTINCT skill_id, skill_value FROM temp_skill tp
        WHERE NOT EXISTS (
            SELECT 1 FROM player_skill ps
            WHERE 1
                AND tp.skill_id = ps.skill_id
                AND tp.skill_value = ps.skill_value
        );
    """
    sql_insert_pl_activity = """
        INSERT IGNORE INTO player_activity (activity_id, activity_value)
        SELECT DISTINCT activity_id, activity_value FROM temp_activity tp
        WHERE NOT EXISTS (
            SELECT 1 FROM player_activity pa
            WHERE 1
                AND tp.activity_id = pa.activity_id
                AND tp.activity_value = pa.activity_value
        );
    """

    sql_insert_sc_data = """
        INSERT IGNORE INTO scraper_data (scrape_ts, scrape_date, player_id)
        select DISTINCT scrape_ts, scrape_date, player_id from (
            SELECT scrape_ts, scrape_date, player_id FROM temp_skill ts
            UNION
            SELECT scrape_ts, scrape_date, player_id FROM temp_activity ta
        ) tp
        WHERE NOT EXISTS (
            SELECT 1 FROM scraper_data sd
            WHERE 1
                AND tp.scrape_date = sd.scrape_date
                AND tp.player_id = sd.player_id
        )
        ;
    """

    # insert into the joinging tables
    sql_insert_sc_pl_skill = """
        INSERT IGNORE INTO scraper_player_skill (scrape_id, player_skill_id)
        SELECT sd.scrape_id, ps.player_skill_id FROM temp_skill tp
        join scraper_data sd ON (
            tp.scrape_date = sd.scrape_date AND 
            tp.player_id = sd.player_id
        )
        JOIN player_skill ps ON (
            tp.skill_id = ps.skill_id AND
            tp.skill_value = ps.skill_value
        )
        WHERE NOT EXISTS (
            SELECT 1 FROM scraper_player_skill sps
            WHERE 1
                AND sps.scrape_id = sd.scrape_id
                AND sps.player_skill_id = ps.player_skill_id
        );
    """
    sql_insert_sc_pl_activity = """
        INSERT IGNORE INTO scraper_player_activity (scrape_id, player_activity_id)
        SELECT sd.scrape_id, pa.player_activity_id FROM temp_activity tp
        join scraper_data sd ON (
            tp.scrape_date = sd.scrape_date AND 
            tp.player_id = sd.player_id
        )
        JOIN player_activity pa ON (
            tp.activity_id = pa.activity_id AND
            tp.activity_value = pa.activity_value
        )
        WHERE NOT EXISTS (
            SELECT 1 FROM scraper_player_activity spa
            WHERE 1
                AND spa.scrape_id = sd.scrape_id
                AND spa.player_activity_id = pa.player_activity_id
        );
    """
    # cleanup
    session.execute(sqla.text("DROP TABLE IF EXISTS temp_skill"))
    session.execute(sqla.text("DROP TABLE IF EXISTS temp_activity"))
    # create temp (staging) tables
    session.execute(sqla.text(sql_create_temp_skills))
    session.execute(sqla.text(sql_create_temp_activities))

    # parse data into dict
    _skills = [asdict(s) for s in skills]
    _activities = [asdict(a) for a in activities]

    # insert into temp (staging) tables
    if len(_skills) > 0:
        session.execute(sqla.text(sql_insert_temp_skills), params=_skills)
    if len(_activities) > 0:
        session.execute(sqla.text(sql_insert_temp_activities), params=_activities)

    # insert data into normalized table
    session.execute(sqla.text(sql_insert_sc_data))
    session.execute(sqla.text(sql_insert_pl_skill))
    session.execute(sqla.text(sql_insert_pl_activity))

    # insert data into linking table
    session.execute(sqla.text(sql_insert_sc_pl_skill))
    session.execute(sqla.text(sql_insert_sc_pl_activity))
    # cleanup
    session.execute(sqla.text("DROP TABLE IF EXISTS temp_skill"))
    session.execute(sqla.text("DROP TABLE IF EXISTS temp_activity"))


skill_map = {
    "attack": 1,
    "defence": 2,
    "strength": 3,
    "hitpoints": 4,
    "ranged": 5,
    "prayer": 6,
    "magic": 7,
    "cooking": 8,
    "woodcutting": 9,
    "fletching": 10,
    "fishing": 11,
    "firemaking": 12,
    "crafting": 13,
    "smithing": 14,
    "mining": 15,
    "herblore": 16,
    "agility": 17,
    "thieving": 18,
    "slayer": 19,
    "farming": 20,
    "runecraft": 21,
    "hunter": 22,
    "construction": 23,
}

activity_map = {
    "league": 1,
    "bounty_hunter_hunter": 2,
    "bounty_hunter_rogue": 3,
    "cs_all": 4,
    "cs_beginner": 5,
    "cs_easy": 6,
    "cs_medium": 7,
    "cs_hard": 8,
    "cs_elite": 9,
    "cs_master": 10,
    "lms_rank": 11,
    "soul_wars_zeal": 12,
    "abyssal_sire": 13,
    "alchemical_hydra": 14,
    "barrows_chests": 15,
    "bryophyta": 16,
    "callisto": 17,
    "cerberus": 18,
    "chambers_of_xeric": 19,
    "chambers_of_xeric_challenge_mode": 20,
    "chaos_elemental": 21,
    "chaos_fanatic": 22,
    "commander_zilyana": 23,
    "corporeal_beast": 24,
    "crazy_archaeologist": 25,
    "dagannoth_prime": 26,
    "dagannoth_rex": 27,
    "dagannoth_supreme": 28,
    "deranged_archaeologist": 29,
    "general_graardor": 30,
    "giant_mole": 31,
    "grotesque_guardians": 32,
    "hespori": 33,
    "kalphite_queen": 34,
    "king_black_dragon": 35,
    "kraken": 36,
    "kreearra": 37,
    "kril_tsutsaroth": 38,
    "mimic": 39,
    "nightmare": 40,
    "nex": 41,
    "phosanis_nightmare": 42,
    "obor": 43,
    "phantom_muspah": 44,
    "sarachnis": 45,
    "scorpia": 46,
    "skotizo": 47,
    "tempoross": 48,
    "the_gauntlet": 49,
    "the_corrupted_gauntlet": 50,
    "theatre_of_blood": 51,
    "theatre_of_blood_hard": 52,
    "thermonuclear_smoke_devil": 53,
    "tombs_of_amascut": 54,
    "tombs_of_amascut_expert": 55,
    "tzkal_zuk": 56,
    "tztok_jad": 57,
    "venenatis": 58,
    "vetion": 59,
    "vorkath": 60,
    "wintertodt": 61,
    "zalcano": 62,
    "zulrah": 63,
    "rifts_closed": 64,
    "artio": 65,
    "calvarion": 66,
    "duke_sucellus": 67,
    "spindel": 68,
    "the_leviathan": 69,
    "the_whisperer": 70,
    "vardorvis": 71,
}


def parse_hiscore_records(
    records: list[HiscoreRecord],
) -> tuple[list[ScraperPlayerSkill], list[ScraperPlayerActivity]]:
    skills = []
    activities = []

    # iterate over batch records
    for record in records:
        for skill_key, skill_value in asdict(record.skills).items():
            skill_id = skill_map.get(skill_key)
            if skill_id is None:
                # print(f"{skill_id=}, {record=}")
                continue
            elif skill_value is None or skill_value == 0:
                continue
            _skill = ScraperPlayerSkill(
                skill_id=skill_id,
                skill_value=skill_value,
                scrape_ts=record.scrape_ts,
                scrape_date=record.scrape_date,
                player_id=record.player_id,
            )
            # print(f"appending, {_skill=}")
            skills.append(_skill)
        for activity_key, activity_value in asdict(record.activities).items():
            activity_id = activity_map.get(activity_key)
            if activity_id is None:
                # print(f"{activity_id=}, {record=}")
                continue
            elif activity_value is None or activity_value == 0:
                continue
            _activity = ScraperPlayerActivity(
                activity_id=activity_id,
                activity_value=activity_value,
                scrape_ts=record.scrape_ts,
                scrape_date=record.scrape_date,
                player_id=record.player_id,
            )
            # print(f"appending, {_activity=}")
            activities.append(_activity)
    return skills, activities


class BenchMark(BenchmarkABC):
    def insert_many_records(self, records: list[HiscoreRecord]) -> None:
        skills, activities = parse_hiscore_records(records=records)

        with get_session() as session:
            bulk_normalized_insert(
                session=session,
                skills=skills,
                activities=activities,
            )
            session.commit()

    def get_latest_record_for_player(
        self,
        player_id: int,
    ) -> HiscoreRecord:
        sql = """
            SELECT 
                sd.scrape_date, sd.scrape_ts,
                sk.skill_name, ps.skill_value
            FROM scraper_data sd
            JOIN scraper_player_skill sps ON sps.scrape_id = sd.scrape_id
            JOIN player_skill ps ON sps.player_skill_id = ps.player_skill_id
            JOIN skill sk on ps.skill_id = sk.skill_id
            WHERE 1
                AND sd.scrape_id = (
                    SELECT 
                        scrape_id 
                    from scraper_data
                    WHERE player_id = :player_id
                    ORDER BY scrape_date DESC
                    LIMIT 1
                )
        """
        with get_session() as session:
            result = session.execute(sqla.text(sql), params={"player_id": player_id})
            session.commit()
        return result.first()

    def get_latest_record_for_many_players(
        self,
        players: list[int],
    ) -> list[HiscoreRecord]:
        sql = """
            SELECT 
                sd.scrape_date, sd.scrape_ts, sd.player_id,
                sk.skill_name, 
                ps.skill_value
            FROM scraper_data sd
            JOIN scraper_player_skill sps ON sps.scrape_id = sd.scrape_id
            JOIN player_skill ps ON sps.player_skill_id = ps.player_skill_id
            JOIN skill sk on ps.skill_id = sk.skill_id
            JOIN (
                SELECT 
                    player_id, MAX(scrape_date) max_sd
                FROM scraper_data
                WHERE player_id IN :players
                GROUP BY player_id
            ) a ON sd.player_id = a.player_id AND sd.scrape_date = a.max_sd
        """
        with get_session() as session:
            result = session.execute(sqla.text(sql), params={"players": players})
        return [r._mapping for r in result.fetchall()]

    def get_all_records_for_player(
        self,
        player_id: int,
    ) -> list[HiscoreRecord]:
        sql = """
            SELECT 
                sd.scrape_date, sd.scrape_ts, sd.player_id,
                sk.skill_name, 
                ps.skill_value
            FROM scraper_data sd
            JOIN scraper_player_skill sps ON sps.scrape_id = sd.scrape_id
            JOIN player_skill ps ON sps.player_skill_id = ps.player_skill_id
            JOIN skill sk on ps.skill_id = sk.skill_id
            WHERE 1
                AND sd.player_id = :player_id
        """
        with get_session() as session:
            result = session.execute(sqla.text(sql), params={"player_id": player_id})
        return [r._mapping for r in result.fetchall()]

    def get_all_records_for_many_players(
        self,
        players: list[int],
    ) -> list[HiscoreRecord]:
        sql = """
            SELECT 
                sd.scrape_date, sd.scrape_ts, sd.player_id,
                sk.skill_name, 
                ps.skill_value
            FROM scraper_data sd
            JOIN scraper_player_skill sps ON sps.scrape_id = sd.scrape_id
            JOIN player_skill ps ON sps.player_skill_id = ps.player_skill_id
            JOIN skill sk on ps.skill_id = sk.skill_id
            WHERE 1
                AND sd.player_id IN :players
        """
        with get_session() as session:
            result = session.execute(sqla.text(sql), params={"players": players})
        return [r._mapping for r in result.fetchall()]
