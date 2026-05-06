// BasinFloor — schematic basin surface with floor metric overlays.
// Two visual modes: "broad" (flat-bottomed valley), "point" (sharp pit), "rugged".
const BasinFloor = ({ kind = "broad", title = "basin Φ₂", points = [], status = "verified", height = 180, width = 320 }) => {
  const colors = {
    verified:  "var(--status-verified)",
    warning:   "var(--status-exploratory)",
    falsified: "var(--status-falsified)",
    failed:    "var(--status-falsified)",
  };
  const stroke = colors[status] || colors.verified;

  let path;
  if (kind === "broad") {
    path = `M 10 50 Q 40 70 70 130 L 240 130 Q 280 100 310 50`;
  } else if (kind === "point") {
    path = `M 10 50 Q 70 60 140 75 L 160 165 L 180 75 Q 250 60 310 50`;
  } else { // rugged
    path = `M 10 50 Q 30 70 50 90 T 90 110 Q 100 95 120 105 T 150 130 T 180 110 Q 200 130 230 115 T 280 90 Q 295 80 310 50`;
  }

  return (
    <div style={{
      background: "var(--bg-base)",
      border: `1px solid ${status === "failed" || status === "falsified" ? "rgba(255,92,122,0.35)" : "var(--border-1)"}`,
      borderRadius: "var(--radius-md)",
      padding: 14, position: "relative", overflow: "hidden",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
        <div>
          <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.2, color: "var(--fg-3)", textTransform: "uppercase" }}>basin floor</div>
          <div style={{ font: "500 13px/1.2 var(--font-display)", color: "var(--fg-1)", marginTop: 4 }}>{title}</div>
        </div>
        <Pill status={status} size="sm">{kind}</Pill>
      </div>
      <svg width="100%" height={height} viewBox={`0 0 ${width} 180`} style={{ display: "block" }}>
        <defs>
          <linearGradient id={`fill-${kind}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%"  stopColor={stroke} stopOpacity="0"/>
            <stop offset="100%" stopColor={stroke} stopOpacity="0.18"/>
          </linearGradient>
          <pattern id={`grid-${kind}`} width="32" height="20" patternUnits="userSpaceOnUse">
            <path d="M 32 0 L 0 0 0 20" fill="none" stroke="var(--border-2)" strokeWidth="0.5" opacity="0.4"/>
          </pattern>
        </defs>
        <rect width="100%" height={height} fill={`url(#grid-${kind})`}/>
        {/* fill underneath */}
        <path d={`${path} L ${width} 180 L 0 180 Z`} fill={`url(#fill-${kind})`}/>
        {/* contour line */}
        <path d={path} fill="none" stroke={stroke} strokeWidth="1.8" style={{ filter: `drop-shadow(0 0 4px ${stroke})` }}/>
        {/* perturbation points */}
        {points.map((p, i) => (
          <g key={i}>
            <circle cx={p.x} cy={p.y} r="3.5" fill={p.outcome === "O1" ? "var(--status-verified)" : p.outcome === "O5" ? "var(--status-falsified)" : "var(--status-exploratory)"} opacity="0.9"/>
            <circle cx={p.x} cy={p.y} r="6" fill="none" stroke={p.outcome === "O1" ? "var(--status-verified)" : p.outcome === "O5" ? "var(--status-falsified)" : "var(--status-exploratory)"} opacity="0.4"/>
          </g>
        ))}
        {/* axes labels */}
        <text x="6" y={height - 6} style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-3)", letterSpacing: 0.5 }}>perturbation amplitude →</text>
        <text x="6" y={14} style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-3)", letterSpacing: 0.5 }}>↑ recovery distance</text>
      </svg>
    </div>
  );
};
window.BasinFloor = BasinFloor;
