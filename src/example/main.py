from sqlalchemy import text

from .. import BenchmarkABC, HiscoreRecord, get_session


class BenchMark(BenchmarkABC):
    def insert_many_records(self, records: list[HiscoreRecord]) -> None:
        sql_insert_highscore_data = """
            INSERT ignore INTO highscore_data (
                scrape_ts, scrape_date, player_id, 
                attack, defence, strength, hitpoints, ranged, prayer, magic, cooking, woodcutting, fletching, fishing, firemaking, crafting, smithing, mining, herblore, agility, thieving, slayer, farming, runecraft, hunter, construction,
                league, bounty_hunter_hunter, bounty_hunter_rogue, cs_all, cs_beginner, cs_easy, cs_medium, cs_hard, cs_elite, cs_master, lms_rank, soul_wars_zeal, abyssal_sire, alchemical_hydra, barrows_chests, bryophyta, callisto, cerberus, chambers_of_xeric, chambers_of_xeric_challenge_mode, chaos_elemental, chaos_fanatic, commander_zilyana, corporeal_beast, crazy_archaeologist, dagannoth_prime, dagannoth_rex, dagannoth_supreme, deranged_archaeologist, general_graardor, giant_mole, grotesque_guardians, hespori, kalphite_queen, king_black_dragon, kraken, kreearra, kril_tsutsaroth, mimic, nightmare, nex, phosanis_nightmare, obor, phantom_muspah, sarachnis, scorpia, skotizo, tempoross, the_gauntlet, the_corrupted_gauntlet, theatre_of_blood, theatre_of_blood_hard, thermonuclear_smoke_devil, tombs_of_amascut, tombs_of_amascut_expert, tzkal_zuk, tztok_jad, venenatis, vetion, vorkath, wintertodt, zalcano, zulrah, rifts_closed, artio, calvarion, duke_sucellus, spindel, the_leviathan, the_whisperer, vardorvis
            )
            VALUES (
                :scrape_ts, :scrape_date, :player_id,
                :attack, :defence, :strength, :hitpoints, :ranged, :prayer, :magic, :cooking, :woodcutting, :fletching, :fishing, :firemaking, :crafting, :smithing, :mining, :herblore, :agility, :thieving, :slayer, :farming, :runecraft, :hunter, :construction,
                :league, :bounty_hunter_hunter, :bounty_hunter_rogue, :cs_all, :cs_beginner, :cs_easy, :cs_medium, :cs_hard, :cs_elite, :cs_master, :lms_rank, :soul_wars_zeal, :abyssal_sire, :alchemical_hydra, :barrows_chests, :bryophyta, :callisto, :cerberus, :chambers_of_xeric, :chambers_of_xeric_challenge_mode, :chaos_elemental, :chaos_fanatic, :commander_zilyana, :corporeal_beast, :crazy_archaeologist, :dagannoth_prime, :dagannoth_rex, :dagannoth_supreme, :deranged_archaeologist, :general_graardor, :giant_mole, :grotesque_guardians, :hespori, :kalphite_queen, :king_black_dragon, :kraken, :kreearra, :kril_tsutsaroth, :mimic, :nightmare, :nex, :phosanis_nightmare, :obor, :phantom_muspah, :sarachnis, :scorpia, :skotizo, :tempoross, :the_gauntlet, :the_corrupted_gauntlet, :theatre_of_blood, :theatre_of_blood_hard, :thermonuclear_smoke_devil, :tombs_of_amascut, :tombs_of_amascut_expert, :tzkal_zuk, :tztok_jad, :venenatis, :vetion, :vorkath, :wintertodt, :zalcano, :zulrah, :rifts_closed, :artio, :calvarion, :duke_sucellus, :spindel, :the_leviathan, :the_whisperer, :vardorvis
            )
        """

        params = []
        for record in records:
            record_dict = record.__dict__
            skills = record_dict.pop("skills")
            activities = record_dict.pop("activities")
            record_dict = record_dict | skills.__dict__ | activities.__dict__
            params.append(record_dict)

        with get_session() as session:
            session.execute(text(sql_insert_highscore_data), params=params)
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
