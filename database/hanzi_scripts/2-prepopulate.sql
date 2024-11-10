-- Prepopulate word_tab from CSV file
LOAD DATA INFILE '/var/lib/mysql-files/hsk3_all_words.csv'
INTO TABLE word_tab
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES -- skip the header row
(word_id, hanzi, pinyin, meaning, hsk_level, is_compound);


-- Prepopulate word_map_tab from CSV file
LOAD DATA INFILE '/var/lib/mysql-files/hsk3_word_map.csv'
INTO TABLE word_map_tab
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES -- skip the header row
(parent_id, child_id);
