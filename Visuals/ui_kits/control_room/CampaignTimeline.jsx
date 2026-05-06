// CampaignTimeline — horizontal strip 002–014. Color = status.
const CampaignTimeline = ({ campaigns, current }) => {
  const colors = {
    verified: { bg: "rgba(82,224,162,0.15)", bd: "rgba(82,224,162,0.4)",  glow: "rgba(82,224,162,0.4)",  fg: "var(--status-verified)" },
    active:   { bg: "rgba(0,209,255,0.15)",  bd: "rgba(0,209,255,0.4)",   glow: "rgba(0,209,255,0.5)",   fg: "var(--accent-trace)" },
    warning:  { bg: "rgba(255,184,0,0.15)",  bd: "rgba(255,184,0,0.4)",   glow: "rgba(255,184,0,0.4)",   fg: "var(--status-exploratory)" },
    failed:   { bg: "rgba(255,92,122,0.18)", bd: "rgba(255,92,122,0.45)", glow: "rgba(255,92,122,0.5)",  fg: "var(--status-falsified)" },
  };
  return (
    <div style={{ position: "relative", padding: "30px 8px 38px" }}>
      {/* baseline */}
      <div style={{
        position: "absolute", left: 24, right: 24, top: "50%",
        height: 1, background: "var(--border-2)",
      }}/>
      <div style={{ display: "flex", justifyContent: "space-between", position: "relative", gap: 4 }}>
        {campaigns.map((c, i) => {
          const co = colors[c.status] || colors.warning;
          const isCurrent = c.id === current;
          return (
            <div key={c.id} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6, flex: 1, minWidth: 0 }}>
              <div style={{ font: "500 9px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.4, height: 10 }}>
                {i % 2 === 0 ? c.id : ""}
              </div>
              <div style={{
                width: isCurrent ? 18 : 13, height: isCurrent ? 18 : 13, borderRadius: "50%",
                background: co.bg, border: `1.5px solid ${co.bd}`,
                boxShadow: `0 0 ${isCurrent ? 18 : 8}px ${co.glow}`,
                position: "relative",
              }}>
                {c.status === "failed" && (
                  <div style={{ position: "absolute", inset: 2, borderRadius: "50%", background: co.fg, opacity: 0.6 }}/>
                )}
                {c.status === "active" && (
                  <div style={{ position: "absolute", inset: 3, borderRadius: "50%", background: co.fg, animation: "pulse 1.5s infinite" }}/>
                )}
              </div>
              <div style={{ font: "500 9px/1 var(--font-mono)", color: i % 2 === 1 ? "var(--fg-3)" : "transparent", letterSpacing: 0.4 }}>{c.id}</div>
            </div>
          );
        })}
      </div>
      <style>{`@keyframes pulse { 0%,100%{opacity:.4} 50%{opacity:1} }`}</style>
    </div>
  );
};
window.CampaignTimeline = CampaignTimeline;
