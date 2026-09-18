import { api } from '../API/api';

export const medicaoService = {
  getConsumoTotal: () => api.get('/medicoes/consumption'),
  getConsumoCubicMeters: () => api.get('/medicoes/consumption/cubic-meters'),
  getCusto: () => api.get('/medicoes/consumption/cost'),
  getUltimaMedicao: () => api.get('/medicoes/latest'),
  listMedicoes: (params = {}) => api.get('/medicoes', { params }),
};