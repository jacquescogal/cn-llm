export enum State {
    New = 0,
    Learning = 1,
    Review = 2,
    Relearning = 3
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
export interface StudyCardDTO {
    word: WordDTO;
    fsrs_card: FSRSCardDTO;
}

export interface RatingDTO {
    rating: number;
}

export interface NextPageMetaDTO{
    last_id: number;
    limit: number;
    has_more: boolean;
}

export interface WordPageDTO{
    word_list: WordDTO[];
    next_page_meta: NextPageMetaDTO;
}