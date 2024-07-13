import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Skill:
    skill_id: int
    skill_name: str


@dataclass
class Activity:
    activity_id: int
    activity_name: str


@dataclass
class PlayerSkill:
    player_skill_id: int
    skill_id: int
    skill_value: int = 0


@dataclass
class PlayerActivity:
    player_activity_id: int
    activity_id: int
    activity_value: int = 0


@dataclass
class ScraperData:
    scrape_id: int
    scrape_ts: datetime
    scrape_date: date
    player_id: int


@dataclass
class ScraperPlayerSkill:
    scrape_id: int
    player_skill_id: int


@dataclass
class ScraperPlayerActivity:
    scrape_id: int
    player_activity_id: int
