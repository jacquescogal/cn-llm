import axios from 'axios';
import { ReviewDTO } from '../types/dto';

// Base URL configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // replace with actual server URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to get review card by ID
export const getReviewCardById = async (card_id: number): Promise<ReviewDTO> => {
  const response = await api.get<ReviewDTO>(`/review/card/${card_id}`);
  return response.data;
};
