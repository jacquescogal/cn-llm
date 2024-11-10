from pydantic import BaseModel, Field
from fsrs import Card as fsrsCard, State
from datetime import datetime, timezone
from src.model.word_model import WordModel
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
    card_id: int
    word_id: int
    due_dt_unix: Optional[int] = Field(default=None)
    stability_int: int 
    difficulty_int: int
    elapsed_days: int
    scheduled_days: int
    reps: int
    lapses: int
    state: State
    last_review_dt_unix: Optional[int] = Field(default=None)

    def get_card_id(self) -> int:
        return self.card_id
    
    def get_word_id(self) -> int:
        return self.word_id

    def get_fsrs_card(self) -> FSRSCardModel:
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
    
    @classmethod
    def _to_float(cls, an_int: int) -> float:
        # implemented with int 7 right-most digits are decimal places
        return an_int / 10**7
    
    @classmethod
    def _from_float(cls, a_float: float) -> int:
        return int(a_float * 10**7)
    
    @classmethod
    def from_fsrs_card(cls, card_id: int, word_id: int, card: FSRSCardModel) -> 'CardModel':
        return cls(
            card_id=card_id,
            word_id=word_id,
            due_dt_unix= int(card.due.timestamp()) if card.due is not None else None,
            stability_int=cls._from_float(card.stability),
            difficulty_int=cls._from_float(card.difficulty),
            elapsed_days=card.elapsed_days,
            scheduled_days=card.scheduled_days,
            reps=card.reps,
            lapses=card.lapses,
            state=card.state,
            last_review_dt_unix= int(card.last_review.timestamp()) if card.last_review is not None else None
        )