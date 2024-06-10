import random
from dataclasses import dataclass, field, asdict, replace
from datetime import date, datetime
import json
from copy import deepcopy

@dataclass
class SkillsRecord:
    attack: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    defence: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    strength: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    hitpoints: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    ranged: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    prayer: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    magic: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    cooking: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    woodcutting: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    fletching: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    fishing: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    firemaking: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    crafting: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    smithing: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    mining: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    herblore: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    agility: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    thieving: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    slayer: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    farming: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    runecraft: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    hunter: int = field(default_factory=lambda: random.randint(0, 200_000_000))
    construction: int = field(default_factory=lambda: random.randint(0, 200_000_000))


@dataclass
class ActivitiesRecord:
    league: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    bounty_hunter_hunter: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    bounty_hunter_rogue: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    cs_all: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    cs_beginner: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    cs_easy: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    cs_medium: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    cs_hard: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    cs_elite: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    cs_master: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    lms_rank: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    soul_wars_zeal: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    abyssal_sire: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    alchemical_hydra: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    barrows_chests: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    bryophyta: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    callisto: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    cerberus: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    chambers_of_xeric: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    chambers_of_xeric_challenge_mode: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    chaos_elemental: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    chaos_fanatic: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    commander_zilyana: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    corporeal_beast: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    crazy_archaeologist: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    dagannoth_prime: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    dagannoth_rex: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    dagannoth_supreme: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    deranged_archaeologist: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    general_graardor: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    giant_mole: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    grotesque_guardians: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    hespori: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    kalphite_queen: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    king_black_dragon: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    kraken: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    kreearra: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    kril_tsutsaroth: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    mimic: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    nightmare: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    nex: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    phosanis_nightmare: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    obor: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    phantom_muspah: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    sarachnis: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    scorpia: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    skotizo: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    tempoross: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    the_gauntlet: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    the_corrupted_gauntlet: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    theatre_of_blood: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    theatre_of_blood_hard: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    thermonuclear_smoke_devil: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    tombs_of_amascut: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    tombs_of_amascut_expert: int = field(
        default_factory=lambda: random.randint(0, 1_000_000)
    )
    tzkal_zuk: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    tztok_jad: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    venenatis: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    vetion: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    vorkath: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    wintertodt: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    zalcano: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    zulrah: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    rifts_closed: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    artio: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    calvarion: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    duke_sucellus: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    spindel: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    the_leviathan: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    the_whisperer: int = field(default_factory=lambda: random.randint(0, 1_000_000))
    vardorvis: int = field(default_factory=lambda: random.randint(0, 1_000_000))


default_skills = SkillsRecord(
    attack=0, defence=0, strength=0, hitpoints=0, ranged=0, prayer=0, magic=0,
    cooking=0, woodcutting=0, fletching=0, fishing=0, firemaking=0, crafting=0,
    smithing=0, mining=0, herblore=0, agility=0, thieving=0, slayer=0,
    farming=0, runecraft=0, hunter=0, construction=0
)

default_activities = ActivitiesRecord(
    league=0, bounty_hunter_hunter=0, bounty_hunter_rogue=0, cs_all=0, cs_beginner=0,
    cs_easy=0, cs_medium=0, cs_hard=0, cs_elite=0, cs_master=0, lms_rank=0,
    soul_wars_zeal=0, abyssal_sire=0, alchemical_hydra=0, barrows_chests=0, bryophyta=0,
    callisto=0, cerberus=0, chambers_of_xeric=0, chambers_of_xeric_challenge_mode=0,
    chaos_elemental=0, chaos_fanatic=0, commander_zilyana=0, corporeal_beast=0,
    crazy_archaeologist=0, dagannoth_prime=0, dagannoth_rex=0, dagannoth_supreme=0,
    deranged_archaeologist=0, general_graardor=0, giant_mole=0, grotesque_guardians=0,
    hespori=0, kalphite_queen=0, king_black_dragon=0, kraken=0, kreearra=0,
    kril_tsutsaroth=0, mimic=0, nightmare=0, nex=0, phosanis_nightmare=0, obor=0,
    phantom_muspah=0, sarachnis=0, scorpia=0, skotizo=0, tempoross=0, the_gauntlet=0,
    the_corrupted_gauntlet=0, theatre_of_blood=0, theatre_of_blood_hard=0,
    thermonuclear_smoke_devil=0, tombs_of_amascut=0, tombs_of_amascut_expert=0,
    tzkal_zuk=0, tztok_jad=0, venenatis=0, vetion=0, vorkath=0, wintertodt=0, zalcano=0,
    zulrah=0, rifts_closed=0, artio=0, calvarion=0, duke_sucellus=0, spindel=0,
    the_leviathan=0, the_whisperer=0, vardorvis=0
)

@dataclass
class HiscoreRecord:
    scrape_ts: datetime
    scrape_date: date
    player_id: int
    skills: SkillsRecord = field(default_factory=lambda: SkillsRecord())
    activities: ActivitiesRecord = field(default_factory=lambda: ActivitiesRecord())

    def __post_init__(self):
        if self.skills is None or isinstance(self.skills, dict):
            self.skills = self.load_skills(self.skills)

        if self.activities is None or isinstance(self.activities, dict):
            self.activities = self.load_activities(self.activities)

    def get_skills(self):
        skills = asdict(self.skills)
        skills = {
            name : value
            for name, value in skills.items()
            if value != 0
        }
        return json.dumps(skills)
    def get_activities(self):
        activities = asdict(self.activities)
        activities = {
            name: value
            for name, value in activities.items()
            if value != 0
        }
        return json.dumps(activities)

    @staticmethod
    def load_skills(skills: dict):
        if skills is None:
            skills = {}

        skill_placeholder = deepcopy(default_skills)
        custom_skills = replace(skill_placeholder, **skills)
        return custom_skills

    @staticmethod
    def load_activities(activities: dict):
        if activities is None:
            activities = {}

        activity_placeholder = deepcopy(default_activities)
        custom_activities = replace(activity_placeholder, **activities)
        return custom_activities