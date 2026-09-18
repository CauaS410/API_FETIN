import { api } from '../API/api';

export const notificacaoService = {
  list: (limit = 20) => api.get('/notificacoes', { params: { limit } }),
  marcarComoLida: (id) => api.patch(`/notificacoes/${id}/ler`),
};