import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getCiphers = async () => {
  try {
    const response = await api.get('/ciphers');
    return response.data;
  } catch (error) {
    console.error('Error fetching ciphers:', error);
    throw error;
  }
};

export const runAudit = async (cipherId, customCode, rounds) => {
  try {
    const payload = {
      cipher_id: cipherId,
      rounds: rounds,
    };

    if (cipherId === 'custom') {
      payload.custom_code = customCode;
    }

    const response = await api.post('/audit', payload);
    return response.data;
  } catch (error) {
    console.error('Error running audit:', error);
    throw error;
  }
};
