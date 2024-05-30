import random
from dataclasses import dataclass, field
from datetime import date, datetime


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


@dataclass
class HiscoreRecord:
    scrape_ts: datetime
    scrape_date: date
    player_id: int
    skills: SkillsRecord = SkillsRecord()
    activities: ActivitiesRecord = ActivitiesRecord()
