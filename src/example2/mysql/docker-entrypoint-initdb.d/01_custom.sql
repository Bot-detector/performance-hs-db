-- Step 1: Create the table for HiscoreRecord
USE playerdata;
CREATE TABLE highscore_data (
    scrape_ts DATETIME NOT NULL,
    scrape_date DATE NOT NULL,
    player_id INT NOT NULL,
    skills JSON,
    activities JSON, -- NULL means empty dict
    PRIMARY KEY (player_id, scrape_date),
    INDEX idx_scrape_ts (scrape_ts)
)
PARTITION BY HASH(player_id) PARTITIONS 10;
