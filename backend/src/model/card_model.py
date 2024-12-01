from pydantic import BaseModel, Field
from fsrs import Card as fsrsCard, State, FSRS, Rating, ReviewLog
from datetime import datetime, timezone
from src.model.word_model import WordModel
from src.enums import *
from typing import Optional


class FSRSCardModel(BaseModel):
    due:  Optional[datetime] = Field(default=None)
    stability: float
    difficulty: float
    elapsed_days: int
    scheduled_days: int
    reps: int
    lapses: int
    state: State
    last_review: Optional[datetime] = Field(default=None)

    def get_fsrs_card(self) -> fsrsCard:
        return fsrsCard(
            due=self.due,
            stability=self.stability,
            difficulty=self.difficulty,
            elapsed_days=self.elapsed_days,
            scheduled_days=self.scheduled_days,
            reps=self.reps,
            lapses=self.lapses,
            state=self.state,
            last_review=self.last_review
        )

    @classmethod
    def from_fsrs_card(cls, card: fsrsCard) -> 'FSRSCardModel':
        print(card.to_dict())
        return cls(
            due=card.to_dict().get('due', None),
            stability=card.stability,
            difficulty=card.difficulty,
            elapsed_days=card.elapsed_days,
            scheduled_days=card.scheduled_days,
            reps=card.reps,
            lapses=card.lapses,
            state=card.state,
            last_review=card.to_dict().get('last_review', None)
        )
    
class CardModel(BaseModel):
    card_id: Optional[int] = Field(default=0)
    word_id: int
    card_type: CardType
    due_dt_unix: Optional[int] = Field(default=None)
    stability_int: Optional[int] = Field(default=None)
    difficulty_int: Optional[int] = Field(default=None)
    elapsed_days: Optional[int] = Field(default=None)
    scheduled_days: Optional[int] = Field(default=None)
    reps: Optional[int] = Field(default=None)
    lapses: Optional[int] = Field(default=None)
    state: Optional[State] = Field(default=None)
    last_review_dt_unix: Optional[int] = Field(default=None)
    is_disabled: Optional[bool] = Field(default=False)
    
    @classmethod
    def make_card_template(self, word_id:int, card_type: CardType) -> 'CardModel':
        return CardModel(
            word_id=word_id,
            card_type=card_type,
            due_dt_unix=None,
            stability_int=None,
            difficulty_int=None,
            elapsed_days=None,
            scheduled_days=None,
            reps=None,
            lapses=None,
            state=None,
            last_review_dt_unix=None,
            is_disabled=False,
        )
    def get_card_id(self) -> int:
        return self.card_id

    def get_word_id(self) -> int:
        return self.word_id
    
    def get_card_type(self) -> CardType:
        return self.card_type

    def get_fsrs_card_model(self) -> FSRSCardModel:
        return FSRSCardModel(
            due=datetime.fromtimestamp(self.due_dt_unix, timezone.utc) if self.due_dt_unix is not None else None,
            stability=self._to_float(self.stability_int),
            difficulty=self._to_float(self.difficulty_int),
            elapsed_days=self.elapsed_days,
            scheduled_days=self.scheduled_days,
            reps=self.reps,
            lapses=self.lapses,
            state=self.state,
            last_review_dt=datetime.fromtimestamp(self.last_review_dt_unix, timezone.utc) if self.last_review_dt_unix is not None else None
        )
    
    def review(self, fsrs: FSRS, rating: int) -> 'CardModel':
        fsrs_card = self.get_fsrs_card_model()
        fsrs_card, review_log = fsrs.review_card(fsrs_card.get_fsrs_card(), Rating(rating))
        # update
        self.inject_fsrs(fsrs_card)
        return self
    
    def _to_float(cls, an_int: int) -> float:
        # implemented with int 7 right-most digits are decimal places
        return an_int / 10**7
    
    def _from_float(cls, a_float: float) -> int:
        return int(a_float * 10**7)
    
    def inject_fsrs(self, card: FSRSCardModel) -> 'CardModel':
        self.due_dt_unix = int(card.due.timestamp()) if card.due is not None else None
        self.stability_int = self._from_float(card.stability)
        self.difficulty_int = self._from_float(card.difficulty)
        self.elapsed_days = card.elapsed_days
        self.scheduled_days = card.scheduled_days
        self.reps = card.reps
        self.lapses = card.lapses
        self.state = card.state
        self.last_review_dt_unix = int(card.last_review.timestamp()) if card.last_review is not None else None
        return self