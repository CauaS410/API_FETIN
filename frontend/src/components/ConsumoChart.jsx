import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
} from 'recharts';

function formatDataCurta(isoDate) {
  const [, mes, dia] = isoDate.split('-');
  return `${dia}/${mes}`;
}

function calcularDominioY(dados, referenciaLitros) {
  const maiorConsumo = Math.max(...dados.map((d) => d.consumoLitros), 0);
  const referencia = referenciaLitros || 0;
  const maiorValor = Math.max(maiorConsumo, referencia);

  if (maiorValor === 0) return [0, 10];

  const comFolga = maiorValor * 1.2;
  const passo = Math.pow(10, Math.floor(Math.log10(comFolga)));
  const maximoArredondado = Math.ceil(comFolga / passo) * passo;

  return [0, maximoArredondado];
}

function ConsumoChart({ serie, referenciaDiariaLitros }) {
  const dados = serie.map((item) => ({
    data: formatDataCurta(item.data),
    consumoLitros: item.consumoLitros,
  }));

  const dominioY = calcularDominioY(dados, referenciaDiariaLitros);

  return (
    <div style={{ background: 'white', borderRadius: 16, padding: 24, boxShadow: '0 8px 24px rgba(15,23,42,.06)' }}>
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={dados}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="data" stroke="#64748b" fontSize={12} />
          <YAxis stroke="#64748b" fontSize={12} unit=" L" domain={dominioY} allowDecimals={false} />
          <Tooltip formatter={(value) => [`${value} L`, 'Consumo']} />
          {referenciaDiariaLitros != null && (
            <ReferenceLine
              y={referenciaDiariaLitros}
              stroke="#ef4444"
              strokeDasharray="4 4"
              label={{ value: 'Referência', position: 'insideTopRight', fill: '#ef4444', fontSize: 12 }}
            />
          )}
          <Line type="monotone" dataKey="consumoLitros" stroke="#334155" strokeWidth={2} dot={{ r: 3 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ConsumoChart;