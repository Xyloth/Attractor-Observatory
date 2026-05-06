// HealthBadge — Pulse Deck centerpiece. 0–100 score with glow.
const HealthBadge = ({ score = 87, size = 180 }) => {
  const status = score >= 85 ? "verified" : score >= 70 ? "warning" : "failed";
  const colors = {
    verified: { ring: "var(--status-verified)", glow: "rgba(82,224,162,0.4)" },
    warning:  { ring: "var(--status-exploratory)", glow: "rgba(255,184,0,0.4)" },
    failed:   { ring: "var(--status-falsified)", glow: "rgba(255,92,122,0.4)" },
  }[status];
  const C = 2 * Math.PI * 72;
  const offset = C - (score / 100) * C;
  return (
    <div style={{ position: "relative", width: size, height: size, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{
        position: "absolute", inset: 0, borderRadius: "50%",
        background: `radial-gradient(circle, ${colors.glow} 0%, transparent 70%)`,
        opacity: 0.6, filter: "blur(8px)",
      }}/>
      <svg width={size} height={size} viewBox="0 0 180 180" style={{ position: "relative" }}>
        <circle cx="90" cy="90" r="72" fill="none" stroke="var(--border-1)" strokeWidth="2"/>
        <circle cx="90" cy="90" r="72" fill="none" stroke={colors.ring} strokeWidth="3"
          strokeDasharray={C} strokeDashoffset={offset}
          strokeLinecap="round" transform="rotate(-90 90 90)"
          style={{ filter: `drop-shadow(0 0 6px ${colors.glow})` }}/>
        {/* tick marks */}
        {Array.from({length: 60}).map((_, i) => (
          <line key={i} x1="90" y1="14" x2="90" y2="20"
            stroke={i % 5 === 0 ? "var(--fg-3)" : "var(--border-2)"} strokeWidth="1"
            transform={`rotate(${i * 6} 90 90)`}/>
        ))}
      </svg>
      <div style={{ position: "absolute", textAlign: "center" }}>
        <div style={{
          font: "500 9px/1 var(--font-mono)", letterSpacing: 1.6, color: "var(--fg-3)",
          textTransform: "uppercase", marginBottom: 8,
        }}>Project Health</div>
        <div style={{
          font: "500 56px/1 var(--font-display)", color: colors.ring, letterSpacing: -1,
        }}>{score}</div>
        <div style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 1, marginTop: 6 }}>/ 100</div>
      </div>
    </div>
  );
};
window.HealthBadge = HealthBadge;
