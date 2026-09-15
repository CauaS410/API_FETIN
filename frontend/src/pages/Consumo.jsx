import { useEffect, useState } from 'react';
import { medicaoService } from '../services/medicaoService';
import InfoCard from '../components/InfoCard';
import PageHeader from '../components/PageHeader';
import '../styles/cards.css';

function Consumo() {
  const [litros, setLitros] = useState({ data: null, loading: true, error: false });
  const [m3, setM3] = useState({ data: null, loading: true, error: false });

  const [analise, setAnalise] = useState({ data: null, loading: true, error: false });

  useEffect(() => {
    medicaoService.getConsumoTotal()
      .then((res) => setLitros({ data: res.data, loading: false, error: false }))
      .catch(() => setLitros({ data: null, loading: false, error: true }));

    medicaoService.getConsumoCubicMeters()
      .then((res) => setM3({ data: res.data, loading: false, error: false }))
      .catch(() => setM3({ data: null, loading: false, error: true }));
    // Faz a requisição para a nossa nova rota 
    fetch('http://localhost:8000/medicoes/analise/1') 
      .then((res) => res.json())
      .then((data) => {
        setAnalise({ data: data, loading: false, error: false });
        
        // Se for atípico, dispara o pop-up na tela do celular/PC
        if (data.alerta_atipico) {
          alert(` ALERTA DE CONSUMO ATÍPICO \n\nSeu consumo atual (${data.consumo_atual}L) ultrapassou bastante a sua média de ${data.media_consumo}L.\n\nVerifique possíveis vazamentos!`);
        }
      })
      .catch(() => setAnalise({ data: null, loading: false, error: true }));
    }, []);

  return (
    <div>
      <PageHeader
        title="Consumo de água"
        description="Consulte o volume total de água já utilizado, tanto em litros quanto em metros cúbicos, calculado a partir de todas as medições registradas pelo sensor."
      />
      <div className="info-grid" style={{ maxWidth: 500 }}>
        <InfoCard
          title="Média de Consumo"
          value={analise.data ? analise.data.media_consumo : '--'}
          unit="L"
          loading={analise.loading}
          error={analise.error}
          highlight={analise.data ? analise.data.alerta_atipico : false}
        />
        <InfoCard
          title="Consumo total"
          value={litros.data ? litros.data.totalLiters.toFixed(3) : '--'}
          unit="L"
          loading={litros.loading}
          error={litros.error}
          highlight
        />
        <InfoCard
          title="Consumo em m³"
          value={m3.data ? m3.data.totalCubicMeters.toFixed(3) : '--'}
          unit="m³"
          loading={m3.loading}
          error={m3.error}
        />
      </div>
    </div>
  );
}

export default Consumo;