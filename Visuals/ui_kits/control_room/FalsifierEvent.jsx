// FalsifierEvent — entry in falsifier feed/timeline. Failed honestly badge.
const FalsifierEvent = ({ f, compact = false }) => {
  return (
    <div style={{
      display: "flex", alignItems: "flex-start", gap: 12,
      padding: compact ? "10px 12px" : 14,
      background: "rgba(255,92,122,0.04)",
      border: "1px solid rgba(255,92,122,0.20)",
      borderRadius: "var(--radius-md)",
      position: "relative",
    }}>
      <div style={{
        width: 40, height: 40, flexShrink: 0,
        borderRadius: 6,
        background: "rgba(255,92,122,0.10)",
        border: "1px solid rgba(255,92,122,0.30)",
        display: "flex", alignItems: "center", justifyContent: "center",
        color: "var(--status-falsified)",
      }}>
        <RoomGlyph id="falsifier" size={20}/>
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
          <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--status-falsified)", letterSpacing: 0.5 }}>{f.id}</span>
          <span style={{ font: "500 12.5px/1 var(--font-ui)", color: "var(--fg-1)" }}>{f.motif}</span>
          <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)" }}>· {f.campaign}</span>
          <Pill status="falsified" size="sm">{f.severity}</Pill>
        </div>
        <div style={{ font: "400 12px/1.4 var(--font-ui)", color: "var(--fg-2)", marginTop: 8 }}>
          verdict — <span style={{ color: "var(--fg-1)" }}>{f.verdict}</span>
        </div>
        {!compact && (
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 10 }}>
            <span style={{
              display: "inline-flex", alignItems: "center", gap: 6,
              padding: "3px 8px", borderRadius: 4,
              background: "rgba(255,184,0,0.08)", border: "1px solid rgba(255,184,0,0.25)",
              color: "var(--status-exploratory)",
              font: "500 10px/1 var(--font-mono)", letterSpacing: 0.6, textTransform: "uppercase",
            }}>
              ✓ failed honestly
            </span>
            <span style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.4 }}>
              downgrade · {f.downgrade}
            </span>
          </div>
        )}
      </div>
      <div style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.5, flexShrink: 0 }}>{f.t}</div>
    </div>
  );
};
window.FalsifierEvent = FalsifierEvent;
