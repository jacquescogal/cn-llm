-- Create the hanzi_db database
CREATE DATABASE IF NOT EXISTS hanzi_db;

-- Use the hanzi_db database
USE hanzi_db;

-- Create the word_tab table
CREATE TABLE IF NOT EXISTS word_tab (
    word_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,                       
    word_hanzi NVARCHAR(20) NOT NULL,
    pinyin NVARCHAR(21) NOT NULL, -- Analysed the pin yin and found the longest pinyin is 21 characters
    meaning TEXT NOT NULL,
    hsk_level INT UNSIGNED NOT NULL
); -- word_tab

CREATE INDEX idx_word_hanzi ON word_tab(word_hanzi);
CREATE INDEX idx_pinyin ON word_tab(pinyin);

-- Create the char_tab table
CREATE TABLE IF NOT EXISTS char_tab (
    char_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,                       
    char_hanzi NCHAR(1) NOT NULL, -- NCHAR(1) is a single unicode character
    pinyin NVARCHAR(6) NOT NULL, -- Analysed the pin yin and found the longest pinyin is 6 characters
    meaning TEXT NOT NULL,
    hsk_level INT UNSIGNED NOT NULL
); -- char_tab

CREATE INDEX idx_char_hanzi ON char_tab(char_hanzi);
CREATE INDEX idx_pinyin ON char_tab(pinyin);

-- Create the word_char_map_tab table
CREATE TABLE IF NOT EXISTS word_char_map_tab (
    word_id INT UNSIGNED NOT NULL,
    char_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (word_id, char_id),
    FOREIGN KEY (word_id) REFERENCES word_tab(word_id) ON DELETE CASCADE,
    FOREIGN KEY (char_id) REFERENCES char_tab(char_id) ON DELETE CASCADE
); -- word_char_map_tab