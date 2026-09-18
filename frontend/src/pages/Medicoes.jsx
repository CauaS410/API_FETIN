import { useEffect, useState } from 'react';
import { medicaoService } from '../services/medicaoService';
import PageHeader from '../components/PageHeader';
import { formatDuration, formatDateTime, calcInicio } from '../utils/format';
import './Medicoes.css';

function Medicoes() {
  const [ultima, setUltima] = useState({ data: null, loading: true, error: false });
  const [historico, setHistorico] = useState({ data: [], loading: true, error: false });

  useEffect(() => {
    medicaoService.getUltimaMedicao()
      .then((res) => setUltima({ data: res.data, loading: false, error: false }))
      .catch(() => setUltima({ data: null, loading: false, error: true }));

    medicaoService.listMedicoes({ limit: 10 })
      .then((res) => setHistorico({ data: res.data, loading: false, error: false }))
      .catch(() => setHistorico({ data: [], loading: false, error: true }));
  }, []);

  return (
    <div>
      <PageHeader
        title="Medições"
        description="Acompanhe cada utilização de água detectada pelo sensor, com o volume registrado, a duração da utilização e o momento em que ela começou."
      />

      <section style={{ marginBottom: 36 }}>
        <h3 className="section-title">Última medição</h3>

        {ultima.loading && <p className="section-state">Carregando...</p>}
        {!ultima.loading && ultima.error && (
          <p className="section-state section-state--error">Nenhuma medição registrada ainda.</p>
        )}

        {!ultima.loading && !ultima.error && ultima.data && (
          <div className="last-measurement-card">
            <div className="last-measurement-card__main">
              <span className="last-measurement-card__label">Volume</span>
              <span className="last-measurement-card__value">
                {ultima.data.volume.toFixed(3)} <span className="last-measurement-card__unit">L</span>
              </span>
            </div>

            <div className="last-measurement-card__details">
              <div className="last-measurement-card__detail">
                <span className="last-measurement-card__detail-label">Início</span>
                <span className="last-measurement-card__detail-value">
                  {formatDateTime(calcInicio(ultima.data.timestamp, ultima.data.intervalSeconds))}
                </span>
              </div>
              <div className="last-measurement-card__detail">
                <span className="last-measurement-card__detail-label">Duração</span>
                <span className="last-measurement-card__detail-value">
                  {formatDuration(ultima.data.intervalSeconds)}
                </span>
              </div>
              <div className="last-measurement-card__detail">
                <span className="last-measurement-card__detail-label">Fim</span>
                <span className="last-measurement-card__detail-value">
                  {formatDateTime(ultima.data.timestamp)}
                </span>
              </div>
              <div className="last-measurement-card__detail">
                <span className="last-measurement-card__detail-label">Vazão média</span>
                <span className="last-measurement-card__detail-value">
                  {ultima.data.flowRate.toFixed(2)} L/min
                </span>
              </div>
            </div>
          </div>
        )}
      </section>

      <section>
        <h3 className="section-title">Histórico recente</h3>

        {historico.loading && <p className="section-state">Carregando...</p>}
        {!historico.loading && historico.error && (
          <p className="section-state section-state--error">Não foi possível carregar o histórico.</p>
        )}
        {!historico.loading && !historico.error && historico.data.length === 0 && (
          <p className="section-state">Nenhuma medição registrada ainda.</p>
        )}

        {!historico.loading && !historico.error && historico.data.length > 0 && (
          <div className="measurement-list">
            {historico.data.map((medicao) => (
              <div className="measurement-item" key={medicao.id}>
                <div className="measurement-item__volume">{medicao.volume.toFixed(3)} L</div>
                <div className="measurement-item__meta">
                  <span>Início: {formatDateTime(calcInicio(medicao.timestamp, medicao.intervalSeconds))}</span>
                  <span>Duração: {formatDuration(medicao.intervalSeconds)}</span>
                  <span>Vazão: {medicao.flowRate.toFixed(2)} L/min</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default Medicoes;