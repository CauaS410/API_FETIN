import { api } from '../API/api';

export const consumoAtipicoService = {
  getStatusHoje: () => api.get('/consumo-atipico/hoje'),
  getHistorico: (dias = 14) => api.get('/consumo-atipico/historico', { params: { dias } }),
};