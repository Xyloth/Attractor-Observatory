// Sidebar — left rail. 10 rooms + project graph. Active state indicator.
const Sidebar = ({ current, onChange }) => {
  const rooms = [
    { id: "pulse",      label: "Pulse Deck",        glyph: "pulse" },
    { id: "ai_ops",     label: "AI Operations",     glyph: "ai_ops" },
    { id: "campaign",   label: "Campaign Command",  glyph: "campaign" },
    { id: "world",      label: "World Observatory", glyph: "world" },
    { id: "motif",      label: "Motif Atlas",       glyph: "motif" },
    { id: "basin",      label: "Basin-Floor Lab",   glyph: "basin" },
    { id: "falsifier",  label: "Falsifier Ledger",  glyph: "falsifier" },
    { id: "doctrine",   label: "Doctrine Console",  glyph: "doctrine" },
    { id: "factory",    label: "Factory Intake",    glyph: "factory", warn: true },
    { id: "portfolio",  label: "Portfolio / Demo",  glyph: "portfolio" },
  ];
  return (
    <aside style={{
      width: 232, flexShrink: 0,
      background: "var(--surface-1)",
      borderRight: "1px solid var(--border-1)",
      display: "flex", flexDirection: "column",
      padding: "16px 0",
      position: "relative",
    }}>
      {/* Brand */}
      <div style={{ padding: "0 18px 18px", borderBottom: "1px solid var(--border-1)", marginBottom: 14 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 28, height: 28, borderRadius: 6,
            background: "radial-gradient(circle at 30% 30%, var(--accent-trace), var(--accent-motif) 80%)",
            display: "flex", alignItems: "center", justifyContent: "center",
            boxShadow: "0 0 16px -4px rgba(0,209,255,0.5)",
          }}>
            <div style={{ width: 8, height: 8, borderRadius: "50%", background: "var(--bg-base)" }} />
          </div>
          <div>
            <div style={{ font: "600 13px/1 var(--font-display)", letterSpacing: 0.4, color: "var(--fg-1)" }}>Attractor</div>
            <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", marginTop: 4, textTransform: "uppercase" }}>Observatory · v0.14</div>
          </div>
        </div>
      </div>
      {/* Room nav */}
      <div style={{ display: "flex", flexDirection: "column", gap: 1, padding: "0 8px", flex: 1 }}>
        <div style={{
          font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4,
          color: "var(--fg-3)", textTransform: "uppercase",
          padding: "4px 10px 8px",
        }}>Rooms</div>
        {rooms.map((r, i) => {
          const active = current === r.id;
          return (
            <button key={r.id} onClick={() => onChange(r.id)} style={{
              display: "flex", alignItems: "center", gap: 11,
              padding: "8px 10px", borderRadius: "var(--radius-sm)",
              background: active ? "rgba(0, 209, 255, 0.08)" : "transparent",
              border: "none", textAlign: "left", cursor: "pointer",
              color: active ? "var(--fg-1)" : "var(--fg-2)",
              font: "500 12.5px/1 var(--font-ui)", letterSpacing: 0.1,
              position: "relative",
            }}>
              {active && <span style={{
                position: "absolute", left: -8, top: 6, bottom: 6, width: 2,
                background: "var(--accent-trace)", borderRadius: 2,
                boxShadow: "0 0 8px var(--accent-trace)",
              }} />}
              <span style={{
                width: 22, height: 22, display: "flex", alignItems: "center", justifyContent: "center",
                color: active ? "var(--accent-trace)" : "var(--fg-3)",
              }}>
                <RoomGlyph id={r.glyph} size={18} />
              </span>
              <span style={{ flex: 1 }}>{r.label}</span>
              <span style={{ font: "500 9px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.6 }}>0{i+1}</span>
              {r.warn && <span style={{
                width: 5, height: 5, borderRadius: "50%", background: "var(--status-exploratory)",
                boxShadow: "0 0 6px var(--status-exploratory)",
              }}/>}
            </button>
          );
        })}
        <div style={{
          font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4,
          color: "var(--fg-3)", textTransform: "uppercase",
          padding: "16px 10px 8px",
        }}>Cross-cut</div>
        <button onClick={() => onChange("graph")} style={{
          display: "flex", alignItems: "center", gap: 11,
          padding: "8px 10px", borderRadius: "var(--radius-sm)",
          background: current === "graph" ? "rgba(176, 132, 255, 0.10)" : "transparent",
          border: "none", textAlign: "left", cursor: "pointer",
          color: current === "graph" ? "var(--fg-1)" : "var(--fg-2)",
          font: "500 12.5px/1 var(--font-ui)",
        }}>
          <span style={{ color: "var(--accent-motif)", display: "flex" }}>
            <RoomGlyph id="graph" size={18}/>
          </span>
          <span style={{ flex: 1 }}>Project Graph</span>
          <Pill status="active" size="sm" dot={false}>live</Pill>
        </button>
      </div>
      {/* Footer — agent presence */}
      <div style={{ padding: "12px 16px", borderTop: "1px solid var(--border-1)" }}>
        <div style={{
          font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4,
          color: "var(--fg-3)", textTransform: "uppercase", marginBottom: 8,
        }}>Agents online</div>
        {[
          { name: "Architect",  status: "verified" },
          { name: "Builder",    status: "active"   },
          { name: "Codex",      status: "verified" },
          { name: "Human PI",   status: "verified" },
        ].map(a => (
          <div key={a.name} style={{
            display: "flex", alignItems: "center", gap: 8,
            padding: "4px 0", font: "500 11px/1 var(--font-mono)",
            color: "var(--fg-2)", letterSpacing: 0.3,
          }}>
            <span style={{
              width: 6, height: 6, borderRadius: "50%",
              background: a.status === "active" ? "var(--accent-trace)" : "var(--status-verified)",
              boxShadow: `0 0 6px ${a.status === "active" ? "var(--accent-trace)" : "var(--status-verified)"}`,
            }}/>
            {a.name}
          </div>
        ))}
      </div>
    </aside>
  );
};
window.Sidebar = Sidebar;
