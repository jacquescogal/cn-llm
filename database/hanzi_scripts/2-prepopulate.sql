-- Prepopulate word_tab from CSV file
LOAD DATA INFILE '/var/lib/mysql-files/hsk3_all_words.csv'
INTO TABLE word_tab
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES -- skip the header row
(word_id, word_hanzi, pinyin, meaning, hsk_level);

-- Prepopulate char_tab from CSV file
LOAD DATA INFILE '/var/lib/mysql-files/hsk3_all_characters.csv'
INTO TABLE char_tab
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES -- skip the header row
(char_id, char_hanzi, pinyin, meaning, hsk_level);


-- Prepopulate word_char_map_tab from CSV file
LOAD DATA INFILE '/var/lib/mysql-files/hsk3_char_word_map_tab.csv'
INTO TABLE word_char_map_tab
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES -- skip the header row
(char_id, word_id);
