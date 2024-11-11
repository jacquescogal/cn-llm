import axios from 'axios';
import { WordDTO, NextPageMetaDTO, WordPageDTO } from '../types/dto';

// Base URL configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // replace with actual server URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to get word by ID
export const getWordById = async (id: number): Promise<WordDTO> => {
  const response = await api.get<WordDTO>(`/word/${id}`);
  return response.data;
};

// Function to get parent words by child ID
export const getParentWordListByChildId = async (id: number): Promise<WordDTO[]> => {
  const response = await api.get<WordDTO[]>(`/word/${id}/parents`);
  return response.data;
};

// Function to get children words by parent ID
export const getChildrenWordListByParentId = async (id: number): Promise<WordDTO[]> => {
  const response = await api.get<WordDTO[]>(`/word/${id}/children`);
  return response.data;
};

// Function to get words by HSK level
export const getWordListOfHskLevel = async (level: number, pageMeta: NextPageMetaDTO): Promise<WordPageDTO> => {
  const response = await api.get<WordPageDTO>(`/word/hsk/${level}/offset/${pageMeta.last_id}/limit/${pageMeta.limit}`);
  return response.data;
};

// Function to get learnt words
export const getWordListLearnt = async (pageMeta: NextPageMetaDTO): Promise<WordPageDTO> => {
  const response = await api.get<WordPageDTO>(`/word/learnt/offset/${pageMeta.last_id}/limit/${pageMeta.limit}`);
  return response.data;
};

// Function to get not learnt words
export const getWordListNotLearnt = async (pageMeta: NextPageMetaDTO): Promise<WordPageDTO> => {
  const response = await api.get<WordPageDTO>(`/word/not-learnt/offset/${pageMeta.last_id}/limit/${pageMeta.limit}`);
  return response.data;
};

// Function to get all words
export const getWordList = async (pageMeta: NextPageMetaDTO): Promise<WordPageDTO> => {
  const response = await api.get<WordPageDTO>(`/word/offset/${pageMeta.last_id}/limit/${pageMeta.limit}`);
  return response.data;
};

// Function to get words by search query
export const getWordListBySearch = async (searchQuery: string, pageMeta: NextPageMetaDTO): Promise<WordPageDTO> => {
    const response = await api.get<WordPageDTO>(`/word/search/${searchQuery}/offset/${pageMeta.last_id}/limit/${pageMeta.limit}`);
    console.log(response);
    return response.data;
  };
  