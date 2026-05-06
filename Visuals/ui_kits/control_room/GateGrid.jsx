// GateGrid — campaigns × gates. R/Y/G + missing.
const GateGrid = ({ campaigns, gateLabels = ["det","calib","prov","detect","claim","subst"] }) => {
  const colors = {
    0: { bg: "rgba(120,138,168,0.05)", border: "var(--border-1)", glyph: null },
    1: { bg: "rgba(82,224,162,0.10)",  border: "rgba(82,224,162,0.30)", glyph: "✓", color: "var(--status-verified)" },
    2: { bg: "rgba(255,184,0,0.10)",   border: "rgba(255,184,0,0.30)",  glyph: "○", color: "var(--status-exploratory)" },
    3: { bg: "rgba(255,92,122,0.12)",  border: "rgba(255,92,122,0.40)", glyph: "✕", color: "var(--status-falsified)" },
  };
  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <div style={{
        display: "grid", gridTemplateColumns: `120px repeat(${gateLabels.length}, 1fr)`,
        gap: 6, marginBottom: 6,
      }}>
        <div/>
        {gateLabels.map(g => (
          <div key={g} style={{
            font: "500 9px/1 var(--font-mono)", letterSpacing: 1.2,
            color: "var(--fg-3)", textTransform: "uppercase", textAlign: "center", padding: "4px 0",
          }}>{g}</div>
        ))}
      </div>
      {campaigns.map(c => (
        <div key={c.id} style={{
          display: "grid", gridTemplateColumns: `120px repeat(${gateLabels.length}, 1fr)`,
          gap: 6, marginBottom: 4,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 7, padding: "0 4px" }}>
            <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.4 }}>{c.id}</span>
            <span style={{ font: "400 11px/1 var(--font-ui)", color: "var(--fg-2)", letterSpacing: 0.1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{c.title}</span>
          </div>
          {c.gates.map((v, i) => {
            const c2 = colors[v];
            return (
              <div key={i} style={{
                height: 22, borderRadius: 3,
                background: c2.bg, border: `1px solid ${c2.border}`,
                display: "flex", alignItems: "center", justifyContent: "center",
                font: "500 11px/1 var(--font-mono)", color: c2.color || "var(--fg-3)",
              }}>{c2.glyph || ""}</div>
            );
          })}
        </div>
      ))}
    </div>
  );
};
window.GateGrid = GateGrid;
