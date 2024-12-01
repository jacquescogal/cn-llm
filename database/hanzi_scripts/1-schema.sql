-- Create the hanzi_db database
CREATE DATABASE IF NOT EXISTS hanzi_db;

-- Use the hanzi_db database
USE hanzi_db;

-- Create the word_tab table
CREATE TABLE IF NOT EXISTS word_tab (
    word_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,                       
    hanzi NVARCHAR(20) NOT NULL, -- Analysed the hanzi and found the longest hanzi is 20 characters
    pinyin NVARCHAR(21) NOT NULL, -- Analysed the pin yin and found the longest pinyin is 21 characters
    meaning TEXT NOT NULL,
    hsk_level INT UNSIGNED NOT NULL,
    is_compound BOOLEAN NOT NULL -- low parity column
); -- word_tab

CREATE INDEX idx_word_hanzi ON word_tab(hanzi);
CREATE INDEX idx_pinyin ON word_tab(pinyin);
CREATE INDEX idx_hsk_level ON word_tab(hsk_level);

-- Create the word_map_tab table
CREATE TABLE IF NOT EXISTS word_map_tab (
    parent_id INT UNSIGNED NOT NULL,
    child_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (parent_id, child_id),
    FOREIGN KEY (parent_id) REFERENCES word_tab(word_id) ON DELETE CASCADE,
    FOREIGN KEY (child_id) REFERENCES word_tab(word_id) ON DELETE CASCADE
); -- word_char_map_tab

-- Create card_tab table
CREATE TABLE IF NOT EXISTS card_tab (
    card_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    word_id INT UNSIGNED NOT NULL,
    card_type INT UNSIGNED NOT NULL, 
    due_dt_unix BIGINT,
    stability INT UNSIGNED NOT NULL, -- use 7 dp for the stability. [0, 100]
    difficulty INT UNSIGNED NOT NULL, -- use 7 dp for the difficulty. [0, 1]
    elapsed_days INT UNSIGNED NOT NULL,
    scheduled_days INT UNSIGNED NOT NULL,
    reps INT UNSIGNED NOT NULL,
    lapses INT UNSIGNED NOT NULL,
    card_state INT UNSIGNED NOT NULL, -- 0: new, 1: learning, 2: reviewing, 3: relearning
    last_review_dt_unix BIGINT ,
    is_disabled BOOLEAN NOT NULL, 
    FOREIGN KEY (word_id) REFERENCES word_tab(word_id) ON DELETE CASCADE
); -- card_tab

CREATE INDEX idx_due_dt_unix ON card_tab(due_dt_unix);
CREATE INDEX idx_word_id_card_type ON card_tab(word_id, card_type);

