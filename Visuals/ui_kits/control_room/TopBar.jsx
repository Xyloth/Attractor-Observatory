// TopBar — every room. Compact: project health + branch + tests + builder task.
// Plus search and snapshot export.
const TopBar = ({ room }) => {
  const m = window.MOCK;
  return (
    <header style={{
      height: 56, flexShrink: 0,
      display: "flex", alignItems: "center", gap: 12,
      padding: "0 18px",
      background: "var(--surface-1)",
      borderBottom: "1px solid var(--border-1)",
    }}>
      {/* Room title */}
      <div style={{ display: "flex", alignItems: "baseline", gap: 10, minWidth: 280 }}>
        <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", textTransform: "uppercase" }}>{room.eyebrow}</div>
        <div style={{ font: "500 16px/1 var(--font-display)", color: "var(--fg-1)", letterSpacing: 0.2 }}>{room.title}</div>
      </div>

      {/* Search */}
      <div style={{
        flex: 1, maxWidth: 480,
        display: "flex", alignItems: "center", gap: 8,
        height: 32, padding: "0 12px",
        background: "var(--bg-base)", border: "1px solid var(--border-1)",
        borderRadius: "var(--radius-md)",
      }}>
        <span style={{ color: "var(--fg-3)" }}><RoomGlyph id="search" size={14}/></span>
        <input placeholder="search worlds, motifs, campaigns, doctrine, mistakes…" style={{
          flex: 1, background: "transparent", border: "none", outline: "none",
          color: "var(--fg-1)", font: "400 12px/1 var(--font-ui)",
        }}/>
        <kbd style={{
          font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)",
          padding: "3px 6px", border: "1px solid var(--border-2)", borderRadius: 4,
        }}>⌘K</kbd>
      </div>

      <div style={{ flex: 1 }}/>

      {/* Compact status strip */}
      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        <StatItem label="health" value={`${m.health.score}/100`} status="verified"/>
        <Sep/>
        <StatItem label="branch" value={m.branch.name.split("/").pop()} status="active" mono/>
        <Sep/>
        <StatItem label="tests" value={`${m.tests.passed}p / ${m.tests.failed}f`} status={m.tests.failed ? "failed" : "verified"} mono/>
        <Sep/>
        <StatItem label="task" value={m.currentTask.id} status="active" mono/>
      </div>

      <div style={{ width: 1, height: 24, background: "var(--border-1)", margin: "0 4px" }}/>

      {/* Snapshot button */}
      <button style={{
        display: "flex", alignItems: "center", gap: 6,
        height: 32, padding: "0 12px", borderRadius: "var(--radius-md)",
        background: "rgba(0, 209, 255, 0.08)",
        border: "1px solid rgba(0, 209, 255, 0.25)",
        color: "var(--accent-trace)",
        font: "500 11px/1 var(--font-mono)", letterSpacing: 0.5,
        textTransform: "uppercase", cursor: "pointer",
      }}>
        <RoomGlyph id="snapshot" size={14}/>
        snapshot
      </button>
    </header>
  );
};

const Sep = () => <span style={{ width: 1, height: 14, background: "var(--border-2)" }}/>;

const StatItem = ({ label, value, status, mono }) => {
  const colorMap = {
    verified: "var(--status-verified)",
    active:   "var(--accent-trace)",
    failed:   "var(--status-falsified)",
    warning:  "var(--status-exploratory)",
  };
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 3, lineHeight: 1 }}>
      <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.2, color: "var(--fg-3)", textTransform: "uppercase" }}>{label}</div>
      <div style={{
        font: `500 11.5px/1 ${mono ? "var(--font-mono)" : "var(--font-ui)"}`,
        color: colorMap[status] || "var(--fg-1)",
      }}>{value}</div>
    </div>
  );
};

window.TopBar = TopBar;
