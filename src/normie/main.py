# import logging
import copy
from dataclasses import asdict, dataclass
from datetime import date, datetime

import sqlalchemy as sqla
from sqlalchemy.orm import Session

from .. import BenchmarkABC, HiscoreRecord, get_session

# from .. import ActivitiesRecord, BenchmarkABC, HiscoreRecord, SkillsRecord, get_session

# logger = logging.getLogger(__name__)


@dataclass
class PlayerSkill:
    # player_skill_id: int
    skill_id: int
    skill_value: int


@dataclass
class PlayerActivity:
    # player_activity_id: int
    activity_id: int
    activity_value: int


@dataclass
class ScraperData:
    # scrape_id: int
    scrape_ts: datetime
    scrape_date: date
    player_id: int


@dataclass
class ScraperSkill:
    scrape_id: int
    player_skill_id: int


@dataclass
class ScraperActivity:
    scrape_id: int
    player_activity_id: int


@dataclass
class ScraperRecord:
    scaper_data: ScraperData
    player_activities: list[PlayerActivity]
    player_skills: list[PlayerSkill]


def insert_player_skill(session: Session, data: list[PlayerSkill]):
    sql = """
        insert into player_skills (skill_id, skill_value)
        values (:skill_id, :skill_value)
        on duplicate key update
            skill_id = values(skill_id),
            skill_value = values(skill_value)
        """
    session.execute(sqla.text(sql), [asdict(d) for d in data if d])
    return


def insert_player_activity(session: Session, data: list[PlayerActivity]):
    sql = """
        insert into player_activities (activity_id, activity_value)
        values (:activity_id, :activity_value)
        on duplicate key update
            activity_id = values(activity_id),
            activity_value = values(activity_value)
        """
    session.execute(sqla.text(sql), [asdict(d) for d in data if d])
    return


def insert_scraper_data(session: Session, data: list[ScraperData]):
    sql = """
        insert into scraper_data (scrape_ts, scrape_date, player_id)
        values (:scrape_ts, :scrape_date, :player_id)
        on duplicate key update
            scrape_date = values(scrape_date),
            player_id = values(player_id)
        """
    session.execute(sqla.text(sql), [asdict(d) for d in data])
    return


def insert_scraper_player_skill(session: Session, data: list[ScraperSkill]):
    sql = """
        insert into scraper_player_skills (scrape_id, player_skill_id)
        values (:scrape_id, :player_skill_id)
        on duplicate key update
            scrape_id = values(scrape_id),
            player_skill_id = values(player_skill_id)
        """
    session.execute(sqla.text(sql), [asdict(d) for d in data if d])
    return


def insert_scraper_player_activity(session: Session, data: list[ScraperSkill]):
    sql = """
        insert into scraper_player_activities (scrape_id, player_activity_id)
        values (:scrape_id, :player_activity_id)
        on duplicate key update
            scrape_id = values(scrape_id),
            player_activity_id = values(player_activity_id)
        """
    session.execute(sqla.text(sql), [asdict(d) for d in data if d])
    return


def select_player_skill(session: Session, data: PlayerSkill):
    sql = """
        select player_skill_id from player_skills 
        where 1=1
            and skill_id = :skill_id
            and skill_value = :skill_value
        """
    result = session.execute(sqla.text(sql), params=asdict(data))
    return result.first()


def select_player_activity(session: Session, data: PlayerActivity):
    sql = """
        select player_activity_id from player_activities 
        where 1=1
            and activity_id = :activity_id
            and activity_value = :activity_value
        """
    result = session.execute(sqla.text(sql), params=asdict(data))
    return result.first()


def select_scraper_data(session: Session, data: ScraperData):
    sql = """
        select scrape_id from scraper_data 
        where 1=1
            and player_id = :player_id
            and scrape_date = :scrape_date
        """
    result = session.execute(sqla.text(sql), params=asdict(data))
    return result.first()


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


def parse_hiscore_records(records: list[HiscoreRecord]) -> list[ScraperRecord]:
    scraper_records = []

    # iterate over batch records
    for record in records:
        player_skills = []
        player_activities = []

        for skill, v in asdict(record.skills).items():
            skill_id = skill_map.get(skill)
            if not skill_id:
                print(f"{skill=} not found, {record=}")
                continue
            elif not v:
                continue
            player_skills.append(
                PlayerSkill(
                    skill_id=skill_id,
                    skill_value=v,
                )
            )

        for activity, v in asdict(record.activities).items():
            activity_id = activity_map.get(activity)
            if not activity_id:
                print(f"{activity=} not found, {record=}")
                continue
            elif not v:
                continue

            player_activities.append(
                PlayerActivity(
                    activity_id=activity_id,
                    activity_value=v,
                )
            )

        scraper_data = ScraperData(
            scrape_ts=record.scrape_ts,
            scrape_date=record.scrape_date,
            player_id=record.player_id,
        )
        scraper_record = ScraperRecord(
            scaper_data=scraper_data,
            player_skills=copy.deepcopy(player_skills),
            player_activities=copy.deepcopy(player_activities),
        )
        scraper_records.append(scraper_record)
    return scraper_records


class BenchMark(BenchmarkABC):
    def insert_many_records(self, records: list[HiscoreRecord]) -> None:
        scraper_records = parse_hiscore_records(records=records)

        player_activities = []
        player_skills = []
        scraper_data = []

        for sr in scraper_records:
            player_activities.extend(sr.player_activities)
            player_skills.extend(sr.player_skills)
            scraper_data.append(sr.scaper_data)

        with get_session() as session:
            insert_player_activity(session=session, data=player_activities)
            insert_player_skill(session=session, data=player_skills)
            insert_scraper_data(session=session, data=scraper_data)

            scraper_skills = []
            scraper_activities = []
            for sr in scraper_records:
                # create list of scraper_player_activity

                # create list of scraper_player_skill
                scrape_id = select_scraper_data(session=session, data=sr.scaper_data)[0]
                assert isinstance(scrape_id, int)

                # select player_activity, player_skill, scraper_data
                for ps in sr.player_skills:
                    if not ps:
                        continue

                    player_skill_id = select_player_skill(session=session, data=ps)
                    player_skill_id = player_skill_id[0]
                    assert isinstance(player_skill_id, int)

                    scraper_skills.append(
                        ScraperSkill(
                            scrape_id=scrape_id,
                            player_skill_id=player_skill_id,
                        )
                    )

                for pa in sr.player_activities:
                    if not pa:
                        continue

                    player_act_id = select_player_activity(session=session, data=pa)
                    player_act_id = player_act_id[0]
                    assert isinstance(player_act_id, int)

                    scraper_activities.append(
                        ScraperActivity(
                            scrape_id=scrape_id,
                            player_activity_id=player_act_id,
                        )
                    )

            # insert scraper_player_skill
            if scraper_skills:
                insert_scraper_player_skill(session=session, data=scraper_skills)
            # insert scraper_player_activity
            if scraper_activities:
                insert_scraper_player_activity(session=session, data=scraper_activities)

            session.commit()

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
