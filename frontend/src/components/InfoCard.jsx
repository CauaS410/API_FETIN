function InfoCard({ title, value, unit, loading, error, highlight }) {
  return (
    <div className={`info-card ${highlight ? 'info-card--highlight' : ''}`}>
      <span className="info-card__title">{title}</span>

      {loading && <span className="info-card__state">Carregando...</span>}

      {!loading && error && (
        <span className="info-card__state info-card__state--error">
          Sem registro do sensor.
        </span>
      )}

      {!loading && !error && (
        <span className="info-card__value">
          {value}
          {unit && <span className="info-card__unit"> {unit}</span>}
        </span>
      )}
    </div>
  );
}

export default InfoCard;