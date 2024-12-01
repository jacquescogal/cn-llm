import axios from 'axios';
import { CardType, ReadCardDTO} from '../types/dto';

// Base URL configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // replace with actual server URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Get card by ID
export const getCardById = async (word_id: number): Promise<ReadCardDTO> => {
  const response = await api.get<ReadCardDTO>(`/card/word/${word_id}`);
  return response.data;
};

// Create card
export const createCard = async (word_id: number, card_type: CardType): Promise<ReadCardDTO> => {
  const response = await api.post<ReadCardDTO>(`/card/word/${word_id}/type/${card_type}`);
  return response.data;
};

// Create card
export const createCardAll = async (word_id: number): Promise<ReadCardDTO> => {
  const response = await api.post<ReadCardDTO>(`/card/word/${word_id}`);
  return response.data;
};

// Delete card
export const deleteCardOfWordCardType = async (word_id: number, card_type: CardType): Promise<ReadCardDTO> => {
  const response = await api.delete<ReadCardDTO>(`/card/word/${word_id}/type/${card_type}`);
  return response.data;
};

// // Update card on review
// export const updateCardOnReview = async (id: number, ratingDTO: RatingDTO): Promise<boolean> => {
//   const response = await api.put<boolean>(`/card/${id}`, ratingDTO);
//   return response.data;
// };

// // Get due card list with limit
// export const getDueCardList = async (limit: number): Promise<StudyCardDTO[]> => {
//   const response = await api.get<StudyCardDTO[]>(`/card/due/limit/${limit}`);
//   return response.data;
// };

// // Get past due card list with limit
// export const getPastDueCardList = async (limit: number): Promise<StudyCardDTO[]> => {
//   const response = await api.get<StudyCardDTO[]>(`/card/past/due/limit/${limit}`);
//   return response.data;
// };

// // Get card list with offset and limit
// export const getCardList = async (offset: number, limit: number): Promise<{ cards: StudyCardDTO[], pageMeta: PageMetaDTO }> => {
//   const response = await api.get<{ cards: StudyCardDTO[], pageMeta: PageMetaDTO }>(`/card/offset/${offset}/limit/${limit}`);
//   return response.data;
// };
