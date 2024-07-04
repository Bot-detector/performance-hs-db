import random
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class SkillsRecord:
    attack: int = None
    defence: int = None
    strength: int = None
    hitpoints: int = None
    ranged: int = None
    prayer: int = None
    magic: int = None
    cooking: int = None
    woodcutting: int = None
    fletching: int = None
    fishing: int = None
    firemaking: int = None
    crafting: int = None
    smithing: int = None
    mining: int = None
    herblore: int = None
    agility: int = None
    thieving: int = None
    slayer: int = None
    farming: int = None
    runecraft: int = None
    hunter: int = None
    construction: int = None

    def __yield_gauss(self, mu, sigma, min_value, max_value, rounded: int = 1_000):
        while True:
            num = int(round(random.gauss(mu, sigma), 0))
            # yield min value if lower
            # keep trying until num is between min & max value
            if num <= min_value:
                yield min_value
            elif min_value <= num <= max_value:
                yield int(num / rounded) * rounded

    def __random_keys(self, mu: int, sigma: int, min_value: int, max_value: int):
        """
        mu: gaussian average
        sigma: guassian spread
        min_value: min cutoff spread
        max_value: max cutoff spread
        """
        num_fields = int(next(self.__yield_gauss(mu, sigma, min_value, max_value)))

        fields = [f for f in self.__dataclass_fields__]
        fields_to_keep = random.sample(fields, num_fields)
        return fields_to_keep

    def random(self):
        mlen = len(self.__dataclass_fields__)
        fields = self.__random_keys(mu=5, sigma=5, min_value=0, max_value=mlen)
        gauss_gen = self.__yield_gauss(
            mu=3_301_035,  # Average OSRS skill exp (e.g., attack, defence, etc.)
            sigma=8_560_358,  # Standard deviation for skill exp
            min_value=0,  # Minimum possible skill exp
            max_value=200_000_000,  # Maximum possible skill exp
        )
        for _field in fields:
            value = int(next(gauss_gen))
            setattr(self, _field, value)


@dataclass
class ActivitiesRecord:
    league: int = None
    bounty_hunter_hunter: int = None
    bounty_hunter_rogue: int = None
    cs_all: int = None
    cs_beginner: int = None
    cs_easy: int = None
    cs_medium: int = None
    cs_hard: int = None
    cs_elite: int = None
    cs_master: int = None
    lms_rank: int = None
    soul_wars_zeal: int = None
    abyssal_sire: int = None
    alchemical_hydra: int = None
    barrows_chests: int = None
    bryophyta: int = None
    callisto: int = None
    cerberus: int = None
    chambers_of_xeric: int = None
    chambers_of_xeric_challenge_mode: int = None
    chaos_elemental: int = None
    chaos_fanatic: int = None
    commander_zilyana: int = None
    corporeal_beast: int = None
    crazy_archaeologist: int = None
    dagannoth_prime: int = None
    dagannoth_rex: int = None
    dagannoth_supreme: int = None
    deranged_archaeologist: int = None
    general_graardor: int = None
    giant_mole: int = None
    grotesque_guardians: int = None
    hespori: int = None
    kalphite_queen: int = None
    king_black_dragon: int = None
    kraken: int = None
    kreearra: int = None
    kril_tsutsaroth: int = None
    mimic: int = None
    nightmare: int = None
    nex: int = None
    phosanis_nightmare: int = None
    obor: int = None
    phantom_muspah: int = None
    sarachnis: int = None
    scorpia: int = None
    skotizo: int = None
    tempoross: int = None
    the_gauntlet: int = None
    the_corrupted_gauntlet: int = None
    theatre_of_blood: int = None
    theatre_of_blood_hard: int = None
    thermonuclear_smoke_devil: int = None
    tombs_of_amascut: int = None
    tombs_of_amascut_expert: int = None
    tzkal_zuk: int = None
    tztok_jad: int = None
    venenatis: int = None
    vetion: int = None
    vorkath: int = None
    wintertodt: int = None
    zalcano: int = None
    zulrah: int = None
    rifts_closed: int = None
    artio: int = None
    calvarion: int = None
    duke_sucellus: int = None
    spindel: int = None
    the_leviathan: int = None
    the_whisperer: int = None
    vardorvis: int = None

    def __yield_gauss(self, mu, sigma, min_value, max_value, rounded: int = 10):
        while True:
            num = int(round(random.gauss(mu, sigma), 0))
            # yield min value if lower
            # keep trying until num is between min & max value
            if num <= min_value:
                yield min_value
            elif min_value <= num <= max_value:
                yield int(num / rounded) * rounded

    def __random_keys(self, mu: int, sigma: int, min_value: int, max_value: int):
        """
        mu: gaussian average
        sigma: guassian spread
        min_value: min cutoff spread
        max_value: max cutoff spread
        """
        num_fields = int(next(self.__yield_gauss(mu, sigma, min_value, max_value)))

        fields = [f for f in self.__dataclass_fields__]
        fields_to_keep = random.sample(fields, num_fields)
        return fields_to_keep

    def random(self):
        mlen = len(self.__dataclass_fields__)
        fields = self.__random_keys(mu=5, sigma=5, min_value=0, max_value=mlen)
        gauss_gen = self.__yield_gauss(
            mu=48,  # Average OSRS activity score (e.g., league, bounty_hunter_hunter, etc.)
            sigma=270,  # Standard deviation for activity score
            min_value=0,  # Minimum possible activity score
            max_value=65_000,  # Maximum possible activity score
            rounded=100,
        )
        for _field in fields:
            value = int(next(gauss_gen))
            setattr(self, _field, value)


@dataclass
class HiscoreRecord:
    scrape_ts: datetime
    scrape_date: date
    player_id: int
    skills: SkillsRecord
    activities: ActivitiesRecord
