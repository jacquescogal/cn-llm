from src.db.mysql_db import Database
from src.model import *
from typing import List
from aiomysql import Connection, Cursor
from src.dto import NextPageMetaDTO
from typing import List, Tuple

class CardRepo:
    instance = None
    def __init__(self, database: Database):
        self.database = database
    
    async def create_card(self, card: CardModel) -> int:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'INSERT INTO card_tab (word_id, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (
                        card.word_id,
                        card.due_dt_unix,
                        card.stability_int,
                        card.difficulty_int,
                        card.elapsed_days,
                        card.scheduled_days,
                        card.reps,
                        card.lapses,
                        card.state,
                        card.last_review_dt_unix
                    )
                )  
                await conn.commit()
                return cur.lastrowid
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return 0
    
    async def read_card_by_id(self, card_id: int) -> CardModel:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT card_id, word_id, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix FROM card_tab WHERE card_id = %s',
                    (card_id,)
                )
                fetched = await cur.fetchone()
                if fetched:
                    card = CardModel(
                        card_id=fetched[0],
                        word_id=fetched[1],
                        due_dt_unix=fetched[2],
                        stability_int=fetched[3],
                        difficulty_int=fetched[4],
                        elapsed_days=fetched[5],
                        scheduled_days=fetched[6],
                        reps=fetched[7],
                        lapses=fetched[8],
                        state=fetched[9],
                        last_review_dt_unix=fetched[10]
                    )
                    return card
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def read_card_by_word_id(self, word_id: int) -> CardModel:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT card_id, word_id, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix FROM card_tab WHERE word_id = %s',
                    (word_id,)
                )
                fetched = await cur.fetchone()
                if fetched:
                    card = CardModel(
                        card_id=fetched[0],
                        word_id=fetched[1],
                        due_dt_unix=fetched[2],
                        stability_int=fetched[3],
                        difficulty_int=fetched[4],
                        elapsed_days=fetched[5],
                        scheduled_days=fetched[6],
                        reps=fetched[7],
                        lapses=fetched[8],
                        state=fetched[9],
                        last_review_dt_unix=fetched[10]
                    )
                    return card
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def update_card(self, card: CardModel) -> bool:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'UPDATE card_tab SET due_dt_unix=%s, stability=%s, difficulty=%s, elapsed_days=%s, scheduled_days=%s, reps=%s, lapses=%s, card_state=%s, last_review_dt_unix=%s WHERE card_id=%s',
                    (
                        card.due_dt_unix,
                        card.stability_int,
                        card.difficulty_int,
                        card.elapsed_days,
                        card.scheduled_days,
                        card.reps,
                        card.lapses,
                        card.state,
                        card.last_review_dt_unix,
                        card.card_id
                    )
                )
                await conn.commit()
                return True
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return False
    
    async def get_due_card_list(self, limit:int) -> List[CardModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT card_id, word_id, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix FROM card_tab ORDER BY due_dt_unix ASC LIMIT %s',
                    (limit,)
                )
                fetched = await cur.fetchall()
                cards = []
                for f in fetched:
                    card = CardModel(
                        card_id=f[0],
                        word_id=f[1],
                        due_dt_unix=f[2],
                        stability_int=f[3],
                        difficulty_int=f[4],
                        elapsed_days=f[5],
                        scheduled_days=f[6],
                        reps=f[7],
                        lapses=f[8],
                        state=f[9],
                        last_review_dt_unix=f[10]
                    )
                    cards.append(card)
                return cards
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return []
        
    async def get_past_due_card_list(self) -> List[CardModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT card_id, word_id, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix FROM card_tab WHERE due_dt_unix <= UNIX_TIMESTAMP()'
                )
                fetched = await cur.fetchall()
                cards = []
                for f in fetched:
                    card = CardModel(
                        card_id=f[0],
                        word_id=f[1],
                        due_dt_unix=f[2],
                        stability_int=f[3],
                        difficulty_int=f[4],
                        elapsed_days=f[5],
                        scheduled_days=f[6],
                        reps=f[7],
                        lapses=f[8],
                        state=f[9],
                        last_review_dt_unix=f[10]
                    )
                    cards.append(card)
                return cards
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return []
    
    async def get_card_list(self, last_id:int, limit:int) -> Tuple[List[CardModel], NextPageMetaDTO]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT card_id, word_id, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix FROM card_tab WHERE card_id > %s ORDER BY card_id ASC LIMIT %s',
                    (last_id, limit+1)
                )
                fetched = await cur.fetchall()
                has_more = False
                if len(fetched) > limit:
                    has_more = True
                cards = []
                new_last_id = last_id
                for f in fetched:
                    new_last_id = f[0]
                    if len(cards) == limit:
                        break
                    card = CardModel(
                        card_id=f[0],
                        word_id=f[1],
                        due_dt_unix=f[2],
                        stability_int=f[3],
                        difficulty_int=f[4],
                        elapsed_days=f[5],
                        scheduled_days=f[6],
                        reps=f[7],
                        lapses=f[8],
                        state=f[9],
                        last_review_dt_unix=f[10]
                    )
                    cards.append(card)
                return cards, NextPageMetaDTO(last_id=new_last_id, limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None