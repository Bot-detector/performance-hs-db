-- Step 1: Create the table for HiscoreRecord
USE playerdata;

CREATE TABLE skill (
    skill_id tinyint unsigned NOT NULL AUTO_INCREMENT,
    skill_name varchar(50) NOT NULL,
    PRIMARY KEY (skill_id),
    UNIQUE KEY unique_skill_name (skill_name)
);

CREATE TABLE activity (
    activity_id tinyint unsigned NOT NULL AUTO_INCREMENT,
    activity_name varchar(50) NOT NULL,
    PRIMARY KEY (activity_id),
    UNIQUE KEY unique_activity_name (activity_name)
);

CREATE TABLE player_skill (
    player_skill_id BIGINT unsigned NOT NULL AUTO_INCREMENT,
    skill_id tinyint unsigned NOT NULL,
    skill_value int unsigned NOT NULL DEFAULT '0',
    PRIMARY KEY (player_skill_id),
    UNIQUE KEY unique_skill_value (skill_id, skill_value)
);

CREATE TABLE player_activity (
    player_activity_id bigint unsigned NOT NULL AUTO_INCREMENT,
    activity_id tinyint unsigned NOT NULL,
    activity_value int unsigned NOT NULL DEFAULT '0',
    PRIMARY KEY (player_activity_id),
    UNIQUE KEY unique_activity_value (activity_id, activity_value)
);

CREATE TABLE scraper_data (
    scrape_id bigint unsigned NOT NULL AUTO_INCREMENT,
    scrape_ts DATETIME NOT NULL,
    scrape_date DATE NOT NULL,
    player_id INT NOT NULL,
    PRIMARY KEY (scrape_id),
    UNIQUE KEY unique_player_scrape (player_id, scrape_date),
    INDEX idx_scrape_ts (scrape_ts)
);

CREATE TABLE scraper_player_skill (
    scrape_id BIGINT unsigned NOT NULL,
    player_skill_id BIGINT unsigned NOT NULL,
    PRIMARY KEY (scrape_id, player_skill_id),
    KEY idx_scrape_id (scrape_id),
    KEY idx_player_skill_id (player_skill_id)
)
PARTITION BY HASH (scrape_id) PARTITIONS 10;

CREATE TABLE scraper_player_activity (
    scrape_id BIGINT unsigned NOT NULL,
    player_activity_id BIGINT unsigned NOT NULL,
    PRIMARY KEY (scrape_id, player_activity_id),
    KEY idx_scrape_id (scrape_id),
    KEY idx_player_activity_id (player_activity_id)
)
PARTITION BY HASH (scrape_id) PARTITIONS 10;
