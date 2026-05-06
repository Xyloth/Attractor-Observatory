// MotifNode — luminous node for the constellation map.
const MotifNode = ({ motif, x, y, r = 14, onHover }) => {
  const colors = {
    verified:    { core: "var(--accent-motif)", ring: "var(--status-verified)", glow: "rgba(82,224,162,0.5)" },
    warning:     { core: "var(--accent-motif)", ring: "var(--status-exploratory)", glow: "rgba(255,184,0,0.5)" },
    candidate:   { core: "var(--accent-motif)", ring: "var(--status-exploratory)", glow: "rgba(255,184,0,0.5)" },
    failed:      { core: "var(--status-falsified)", ring: "var(--status-falsified)", glow: "rgba(255,92,122,0.6)" },
    falsified:   { core: "var(--status-falsified)", ring: "var(--status-falsified)", glow: "rgba(255,92,122,0.6)" },
  };
  const c = colors[motif.status] || colors.warning;
  return (
    <g style={{ cursor: "pointer" }}>
      <circle cx={x} cy={y} r={r * 1.8} fill={c.glow} opacity="0.25" filter="blur(6px)"/>
      <circle cx={x} cy={y} r={r} fill={c.core} fillOpacity="0.18" stroke={c.ring} strokeWidth="1.5"/>
      <circle cx={x} cy={y} r={r * 0.4} fill={c.ring} opacity="0.9"/>
      {motif.status === "failed" && (
        <g stroke={c.ring} strokeWidth="1.5" strokeLinecap="round">
          <line x1={x - r * 0.7} y1={y - r * 0.7} x2={x + r * 0.7} y2={y + r * 0.7}/>
          <line x1={x + r * 0.7} y1={y - r * 0.7} x2={x - r * 0.7} y2={y + r * 0.7}/>
        </g>
      )}
      <text x={x} y={y + r + 14} textAnchor="middle"
        style={{ font: "500 10px var(--font-mono)", fill: "var(--fg-2)", letterSpacing: 0.3 }}>
        {motif.id}
      </text>
    </g>
  );
};
window.MotifNode = MotifNode;
