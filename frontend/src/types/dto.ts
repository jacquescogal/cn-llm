export enum State {
    New = 0,
    Learning = 1,
    Review = 2,
    Relearning = 3
}
export enum SearchBy {
    Hanzi,
    Pinyin,
    Meaning,
}
export enum HSKLevel {
    HSK1 = 1,
    HSK2 = 2,
    HSK3 = 3,
    HSK4 = 4,
    HSK5 = 5,
    HSK6 = 6
}
export enum CardType {
    Meaning = 1,
    Pinyin = 2,
    Hanzi = 3,
    MCQ = 4,
    OCR = 5
}

export interface WordDTO{
    word_id: number;
    hanzi: string;
    pinyin: string;
    meaning: string
    hsk_level: number;
    is_compound: boolean;
    is_learnt: boolean;
}

export interface FSRSCardDTO {
    due:  Date;
    stability: number;
    difficulty: number;
    elapsed_days: number;
    scheduled_days: number;
    reps: number;
    lapses: number;
    state: State;
    last_review: Date;
}

export interface CardDTO {
    card_id: number;
    fsrs: FSRSCardDTO;
    card_type: CardType;
    is_disabled: boolean;
}

export interface ReadCardDTO {
    word: WordDTO;
    card: CardDTO[];
}

export interface RatingDTO {
    rating: number;
}

export interface PageMetaDTO{
    offset: number;
    limit: number;
    has_more: boolean;
}

export interface WordPageDTO{
    word_list: WordDTO[];
    page_meta: PageMetaDTO;
}

export interface WordSearchFilter {
    hsk?: number[];
    learnt?: boolean; 
}