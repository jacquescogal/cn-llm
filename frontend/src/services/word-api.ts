import axios from 'axios';
import { WordDTO, PageMetaDTO, WordPageDTO, WordSearchFilter } from '../types/dto';

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
export const getWordListOfHskLevel = async (level: number, pageMeta: PageMetaDTO): Promise<WordPageDTO> => {
  const response = await api.get<WordPageDTO>(`/word/hsk/${level}/offset/${pageMeta.offset}/limit/${pageMeta.limit}`);
  return response.data;
};

// Function to get learnt words
export const getWordListLearnt = async (pageMeta: PageMetaDTO): Promise<WordPageDTO> => {
  const response = await api.get<WordPageDTO>(`/word/learnt/offset/${pageMeta.offset}/limit/${pageMeta.limit}`);
  return response.data;
};

// Function to get not learnt words
export const getWordListNotLearnt = async (pageMeta: PageMetaDTO): Promise<WordPageDTO> => {
  const response = await api.get<WordPageDTO>(`/word/not-learnt/offset/${pageMeta.offset}/limit/${pageMeta.limit}`);
  return response.data;
};

// Function to get all words
export const getWordList = async (pageMeta: PageMetaDTO, wordSearchFilter: WordSearchFilter): Promise<WordPageDTO> => {
  const params = new URLSearchParams(wordSearchFilter as Record<string, string>).toString();
  console.log(params)
  const response = await api.get<WordPageDTO>(`/word/offset/${pageMeta.offset}/limit/${pageMeta.limit}?${params}`);
  return response.data;
};

// Function to get words by search query
export const getWordListBySearch = async (searchQuery: string, pageMeta: PageMetaDTO, wordSearchFilter: WordSearchFilter): Promise<WordPageDTO> => {

  const params = new URLSearchParams(wordSearchFilter as Record<string, string>).toString();
    const response = await api.get<WordPageDTO>(`/word/search/${searchQuery}/offset/${pageMeta.offset}/limit/${pageMeta.limit}?${params}`);
    return response.data;
  };
  