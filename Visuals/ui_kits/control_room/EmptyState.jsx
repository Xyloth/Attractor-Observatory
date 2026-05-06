// EmptyState — single source of truth. D22: empty rooms beat stocked rooms.
// Visually unmistakable: dashed border, muted, with a precise reason.
const EmptyState = ({ kind = "no-data", reason, hint, compact = false }) => {
  const kinds = {
    "no-data":           { label: "no data",        icon: "○" },
    "campaign-needed":   { label: "campaign needed",icon: "▢" },
    "artifact-missing":  { label: "artifact missing",icon: "✕" },
    "adapter-degraded":  { label: "adapter degraded",icon: "△" },
    "skeleton":          { label: "skeleton",       icon: "·" },
    "not-yet-measured":  { label: "not yet measured",icon: "?" },
  };
  const k = kinds[kind] || kinds["no-data"];
  if (compact) {
    return (
      <div style={{
        display: "inline-flex", alignItems: "center", gap: 8,
        padding: "8px 12px", borderRadius: "var(--radius-md)",
        border: "1px dashed var(--border-2)",
        background: "rgba(120, 138, 168, 0.04)",
        color: "var(--fg-3)", font: "500 11px/1 var(--font-mono)",
        letterSpacing: 0.5,
      }}>
        <span style={{ color: "var(--status-missing)" }}>{k.icon}</span>
        <span style={{ textTransform: "uppercase" }}>{k.label}</span>
        {reason && <span style={{ color: "var(--fg-2)", textTransform: "none", letterSpacing: 0 }}>· {reason}</span>}
      </div>
    );
  }
  return (
    <div style={{
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      minHeight: 120, padding: 24, textAlign: "center",
      borderRadius: "var(--radius-md)",
      border: "1px dashed var(--border-2)",
      background: "repeating-linear-gradient(135deg, rgba(120,138,168,0.02) 0 8px, transparent 8px 16px)",
      color: "var(--fg-3)",
    }}>
      <div style={{
        font: "300 28px/1 var(--font-mono)", color: "var(--status-missing)",
        marginBottom: 10, opacity: 0.6,
      }}>{k.icon}</div>
      <div style={{
        font: "500 10px/1 var(--font-mono)", color: "var(--status-missing)",
        letterSpacing: 1.4, textTransform: "uppercase", marginBottom: 6,
      }}>{k.label}</div>
      {reason && <div style={{ font: "400 13px/1.4 var(--font-ui)", color: "var(--fg-2)", maxWidth: 320 }}>{reason}</div>}
      {hint && <div style={{ font: "400 11px/1.4 var(--font-mono)", color: "var(--fg-3)", marginTop: 10, opacity: 0.7 }}>{hint}</div>}
    </div>
  );
};

window.EmptyState = EmptyState;
