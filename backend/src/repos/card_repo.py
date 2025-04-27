from src.repos.db.mysql_db import Database
from src.model import *
from typing import List
from aiomysql import Connection, Cursor
from src.model.dto import *
from typing import List, Tuple
from src.constants import *
class CardRepo:
    instance = None
    def __init__(self, database: Database):
        self.database = database
    
    async def create_card(self, card: CardModel) -> CardModel:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'INSERT INTO card_tab (card_type, review_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, card_content_json, is_disabled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (
                        card.card_type.value,
                        card.review_type.value,
                        card.due_dt_unix,
                        card.stability_int,
                        card.difficulty_int,
                        card.elapsed_days,
                        card.scheduled_days,
                        card.reps,
                        card.lapses,
                        card.state,
                        card.last_review_dt_unix,
                        card.card_content.get_json(),
                        card.is_disabled
                    )
                )
                # commit and get the last inserted id
                await conn.commit()
                card_id = cur.lastrowid
                card.card_id = card_id
                return card
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def read_card_by_id(self, card_id: int) -> CardModel:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT card_type, review_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, card_content_json, is_disabled FROM card_tab WHERE card_id = %s',
                    (card_id,)
                )
                fetched = await cur.fetchone()
                if fetched:
                    card = CardModel(
                        card_id=card_id,
                        card_type=fetched[0],
                        review_type=fetched[1],
                        due_dt_unix=fetched[2],
                        stability_int=fetched[3],
                        difficulty_int=fetched[4],
                        elapsed_days=fetched[5],
                        scheduled_days=fetched[6],
                        reps=fetched[7],
                        lapses=fetched[8],
                        state=fetched[9],
                        last_review_dt_unix=fetched[10],
                        card_content=MULTI_WORD_CONTENT_MAP.get((CardType(fetched[0]),ReviewType(fetched[1])), SingleAnswerCardContent).model_validate_json(fetched[11]),
                        is_disabled=fetched[12]
                    )
                    return card
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def read_card_of_type(self, card_id_list: List[int], card_type: CardType, review_type: ReviewType) -> CardModel:
        if len(card_id_list) == 0:
            return None
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                # Use the unpacking operator * to pass each card_id as an individual argument
                query = 'SELECT card_id, card_type, review_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, card_content_json, is_disabled FROM card_tab WHERE card_type = %s AND review_type = %s AND card_id IN (%s)' % (card_type.value, review_type.value, ','.join(['%s'] * len(card_id_list)))
                await cur.execute(query, tuple(card_id_list))  # pass the list as a tuple of parameters
                fetched = await cur.fetchone()
                print(fetched)
                if fetched:
                    card = CardModel(
                        card_id=fetched[0],
                        card_type=fetched[1],
                        review_type=fetched[2],
                        due_dt_unix=fetched[3],
                        stability_int=fetched[4],
                        difficulty_int=fetched[5],
                        elapsed_days=fetched[6],
                        scheduled_days=fetched[7],
                        reps=fetched[8],
                        lapses=fetched[9],
                        state=fetched[10],
                        last_review_dt_unix=fetched[11],
                        card_content=MULTI_WORD_CONTENT_MAP.get((CardType(fetched[1]),ReviewType(fetched[2])), SingleAnswerCardContent).model_validate_json(fetched[12]),
                        is_disabled=fetched[13]
                    )
                    return card
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def read_card_list_by_card_id_list(self, card_id_list: List[int]) -> List[CardModel]:
        if len(card_id_list) == 0:
            return []
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                # Use the unpacking operator * to pass each card_id as an individual argument
                query = 'SELECT card_id, card_type, review_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, card_content_json, is_disabled FROM card_tab WHERE card_id IN (%s)' % ','.join(['%s'] * len(card_id_list))
                await cur.execute(query, tuple(card_id_list))  # pass the list as a tuple of parameters
                fetched = await cur.fetchall()
                cards = []
                for f in fetched:
                    print(f)
                    card = CardModel(
                        card_id=f[0],
                        card_type=f[1],
                        review_type=f[2],
                        due_dt_unix=f[3],
                        stability_int=f[4],
                        difficulty_int=f[5],
                        elapsed_days=f[6],
                        scheduled_days=f[7],
                        reps=f[8],
                        lapses=f[9],
                        state=f[10],
                        last_review_dt_unix=f[11],
                        card_content=MULTI_WORD_CONTENT_MAP.get((CardType(f[1]),ReviewType(f[2])), SingleAnswerCardContent).model_validate_json(f[12]),
                        is_disabled=f[13]
                    )
                    cards.append(card)
                return cards
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def update_card(self, card: CardModel) -> bool:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'UPDATE card_tab SET due_dt_unix=%s, stability=%s, difficulty=%s, elapsed_days=%s, scheduled_days=%s, reps=%s, lapses=%s, card_state=%s, last_review_dt_unix=%s, card_content_json=%s, is_disabled=%s WHERE card_id=%s',
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
                        card.card_content.get_json(),
                        card.is_disabled,
                        card.card_id
                    )
                )
                await conn.commit()
                return True
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return False
    
    async def get_scheduled_card_list(self, limit:int) -> List[CardModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT card_id, card_type, review_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, card_content_json, is_disabled FROM card_tab WHERE is_disabled=false ORDER BY due_dt_unix ASC LIMIT %s',
                    (limit,)
                )
                fetched = await cur.fetchall()
                cards = []
                for f in fetched:
                    card = CardModel(
                        card_id=f[0],
                        card_type=f[1],
                        review_type=f[2],
                        due_dt_unix=f[3],
                        stability_int=f[4],
                        difficulty_int=f[5],
                        elapsed_days=f[6],
                        scheduled_days=f[7],
                        reps=f[8],
                        lapses=f[9],
                        state=f[10],
                        last_review_dt_unix=f[11],
                        card_content=MULTI_WORD_CONTENT_MAP.get((CardType(f[1]),ReviewType(f[2])), SingleAnswerCardContent).model_validate_json(f[12]),
                        is_disabled=f[13]
                    )
                    cards.append(card)
                return cards
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return []
        
    async def get_due_card_list(self) -> List[CardModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT card_id, card_type, review_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, card_content_json, is_disabled FROM card_tab WHERE is_disabled=false AND due_dt_unix <= UNIX_TIMESTAMP()'
                )
                fetched = await cur.fetchall()
                cards = []
                for f in fetched:
                    card = CardModel(
                        card_id=f[0],
                        card_type=f[1],
                        review_type=f[2],
                        due_dt_unix=f[3],
                        stability_int=f[4],
                        difficulty_int=f[5],
                        elapsed_days=f[6],
                        scheduled_days=f[7],
                        reps=f[8],
                        lapses=f[9],
                        state=f[10],
                        last_review_dt_unix=f[11],
                        card_content=MULTI_WORD_CONTENT_MAP.get((CardType(f[1]),ReviewType(f[2])), SingleAnswerCardContent).model_validate_json(f[12]),
                        is_disabled=f[13]
                    )
                    cards.append(card)
                return cards
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return []
    
    # async def get_card_list(self, offset:int, limit:int) -> Tuple[List[CardModel], PageMeta]:
    #     conn: Connection = await self.database.get_conn()
    #     try:
    #         async with conn.cursor() as cur:
    #             await cur.execute(
    #                 'SELECT card_id, word_id, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix FROM card_tab ORDER BY card_id ASC LIMIT %s OFFSET %s',
    #                 (limit+1, offset)
    #             )
    #             fetched = await cur.fetchall()
    #             has_more = False
    #             if len(fetched) > limit:
    #                 has_more = True
    #             cards = []
    #             for f in fetched:
    #                 if len(cards) == limit:
    #                     break
    #                 card = CardModel(
    #                     card_id=f[0],
    #                     word_id=f[1],
    #                     due_dt_unix=f[2],
    #                     stability_int=f[3],
    #                     difficulty_int=f[4],
    #                     elapsed_days=f[5],
    #                     scheduled_days=f[6],
    #                     reps=f[7],
    #                     lapses=f[8],
    #                     state=f[9],
    #                     last_review_dt_unix=f[10]
    #                 )
    #                 cards.append(card)
    #             return cards, PageMeta(offset=offset+len(cards), limit=limit, has_more=has_more)
    #     finally:
    #         # Release the connection back to the pool
    #         await self.database.release_connection(conn)
    #     return [], None