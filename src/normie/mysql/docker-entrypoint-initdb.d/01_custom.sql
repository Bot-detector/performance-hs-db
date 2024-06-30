-- Step 1: Create the table for HiscoreRecord
USE playerdata;

CREATE TABLE skills (
    skill_id tinyint unsigned NOT NULL AUTO_INCREMENT,
    skill_name varchar(50) NOT NULL,
    PRIMARY KEY (skill_id),
    UNIQUE KEY unique_skill_name (skill_name)
);

CREATE TABLE activities (
    activity_id tinyint unsigned NOT NULL AUTO_INCREMENT,
    activity_name varchar(50) NOT NULL,
    PRIMARY KEY (activity_id),
    UNIQUE KEY unique_activity_name (activity_name)
);

CREATE TABLE player_skills (
    player_skill_id BIGINT unsigned NOT NULL AUTO_INCREMENT,
    skill_id tinyint unsigned NOT NULL,
    skill_value int unsigned NOT NULL DEFAULT '0',
    PRIMARY KEY (player_skill_id),
    UNIQUE KEY unique_skill_value (skill_id, skill_value)
    -- ERROR 1506: Foreign keys are not yet supported in conjunction with partitioning SQL Statement
    -- CONSTRAINT player_skills_ibfk FOREIGN KEY (skill_id) REFERENCES skills (skill_id) ON DELETE CASCADE
)
;

CREATE TABLE player_activities (
    player_activity_id bigint unsigned NOT NULL,
    activity_id tinyint unsigned NOT NULL,
    activity_value int unsigned NOT NULL DEFAULT '0',
    PRIMARY KEY (player_activity_id),
    KEY idx_activity_id_value (activity_id, activity_value)
    -- ERROR 1506: Foreign keys are not yet supported in conjunction with partitioning SQL Statement
    -- CONSTRAINT player_activities_ibfk FOREIGN KEY (activity_id) REFERENCES activities (activity_id) ON DELETE CASCADE
)
;

CREATE TABLE scraper_data (
    scrape_id bigint unsigned NOT NULL,
    scrape_ts DATETIME NOT NULL,
    scrape_date DATE NOT NULL,
    player_id INT NOT NULL,
    PRIMARY KEY (player_id, scrape_date),
    INDEX idx_scrape_ts (scrape_ts)
)
PARTITION BY
    HASH (player_id) PARTITIONS 10;

CREATE TABLE scraper_player_skills (
    scrape_id BIGINT unsigned NOT NULL,
    player_skill_id BIGINT unsigned NOT NULL,
    PRIMARY KEY (scrape_id, player_skill_id),
    KEY idx_scrape_id (scrape_id),
    KEY idx_player_skill_id (player_skill_id)
    -- ERROR 1506: Foreign keys are not yet supported in conjunction with partitioning SQL Statement
    -- CONSTRAINT scraper_player_skills_scraper_ibfk FOREIGN KEY (scrape_id) REFERENCES scraper_data (scrape_id) ON DELETE CASCADE,
    -- CONSTRAINT scraper_player_skills_skill_ibfk FOREIGN KEY (player_skill_id) REFERENCES player_skills (player_skill_id) ON DELETE CASCADE
)
PARTITION BY
    HASH (scrape_id) PARTITIONS 10;

CREATE TABLE scraper_player_activities (
    scrape_id BIGINT unsigned NOT NULL,
    player_activity_id BIGINT unsigned NOT NULL,
    PRIMARY KEY (
        scrape_id,
        player_activity_id
    ),
    KEY idx_scrape_id (scrape_id),
    KEY idx_player_activity_id (player_activity_id)
    -- ERROR 1506: Foreign keys are not yet supported in conjunction with partitioning SQL Statement
    -- CONSTRAINT scraper_player_activities_scraper_ibfk FOREIGN KEY (scrape_id) REFERENCES scraper_data (scrape_id) ON DELETE CASCADE,
    -- CONSTRAINT scraper_player_activities_activity_ibfk FOREIGN KEY (player_activity_id) REFERENCES player_activities (player_activity_id) ON DELETE CASCADE
)
PARTITION BY
    HASH (scrape_id) PARTITIONS 10;
