import axios from 'axios';
import { StudyCardDTO, RatingDTO, NextPageMetaDTO } from '../types/dto';

// Base URL configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // replace with actual server URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Get card by ID
export const getCardById = async (id: number): Promise<StudyCardDTO> => {
  const response = await api.get<StudyCardDTO>(`/card/${id}`);
  return response.data;
};

// Get card by word ID
export const getCardByWordId = async (id: number): Promise<StudyCardDTO> => {
  const response = await api.get<StudyCardDTO>(`/card/word/${id}`);
  return response.data;
};

// Create card
export const createCard = async (id: number): Promise<StudyCardDTO> => {
  const response = await api.post<StudyCardDTO>(`/card/${id}`);
  return response.data;
};

// Update card on review
export const updateCardOnReview = async (id: number, ratingDTO: RatingDTO): Promise<boolean> => {
  const response = await api.put<boolean>(`/card/${id}`, ratingDTO);
  return response.data;
};

// Get due card list with limit
export const getDueCardList = async (limit: number): Promise<StudyCardDTO[]> => {
  const response = await api.get<StudyCardDTO[]>(`/card/due/limit/${limit}`);
  return response.data;
};

// Get past due card list with limit
export const getPastDueCardList = async (limit: number): Promise<StudyCardDTO[]> => {
  const response = await api.get<StudyCardDTO[]>(`/card/past/due/limit/${limit}`);
  return response.data;
};

// Get card list with offset and limit
export const getCardList = async (offset: number, limit: number): Promise<{ cards: StudyCardDTO[], pageMeta: NextPageMetaDTO }> => {
  const response = await api.get<{ cards: StudyCardDTO[], pageMeta: NextPageMetaDTO }>(`/card/offset/${offset}/limit/${limit}`);
  return response.data;
};
