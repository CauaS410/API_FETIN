import { api } from '../API/api';

export const contaAguaService = {
  create: (data) => api.post('/contas-agua', data),
  list: () => api.get('/contas-agua'),
  getReferenciaDiaria: () => api.get('/contas-agua/referencia-diaria'),
};