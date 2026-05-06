// WorldCard — used across Pulse, World Observatory, etc.
const densityLabels = {
  skeleton: "skeleton",
  trace_valid_sparse: "trace-valid sparse",
  exploratory_densified: "exploratory densified",
  calibration_backed: "calibration-backed",
  claim_ready_densified: "claim-ready densified",
};
const densityToStatus = {
  skeleton: "missing",
  trace_valid_sparse: "exploratory",
  exploratory_densified: "exploratory",
  calibration_backed: "verified",
  claim_ready_densified: "verified",
};

const WorldCard = ({ world, compact = false, onClick }) => {
  const status = densityToStatus[world.density] || "missing";
  const isSkeleton = world.density === "skeleton";
  const hueColor = `var(${world.hue})`;
  return (
    <div onClick={onClick} style={{
      background: "var(--surface-1)",
      border: `1px solid ${isSkeleton ? "var(--border-2)" : "var(--border-1)"}`,
      borderRadius: "var(--radius-md)",
      padding: compact ? 12 : 14,
      display: "flex", flexDirection: "column", gap: 10,
      position: "relative", overflow: "hidden",
      cursor: onClick ? "pointer" : "default",
      opacity: isSkeleton ? 0.7 : 1,
    }}>
      {/* hue accent */}
      {!isSkeleton && <div style={{
        position: "absolute", top: 0, left: 0, right: 0, height: 1,
        background: `linear-gradient(90deg, transparent, ${hueColor}, transparent)`,
        opacity: 0.6,
      }}/>}
      <div style={{ display: "flex", alignItems: "flex-start", gap: 10 }}>
        <div style={{
          width: 36, height: 36, flexShrink: 0,
          borderRadius: "var(--radius-sm)",
          background: `radial-gradient(circle at 30% 30%, ${hueColor}22, transparent)`,
          border: `1px solid ${hueColor}33`,
          display: "flex", alignItems: "center", justifyContent: "center",
          color: hueColor,
        }}>
          <WorldGlyph id={world.id} size={28} color={hueColor}/>
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 6 }}>
            <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.6 }}>{world.id}</span>
            <span style={{ font: "500 13.5px/1.1 var(--font-ui)", color: "var(--fg-1)", letterSpacing: 0.1 }}>{world.name}</span>
          </div>
          <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.2, color: "var(--fg-3)", textTransform: "uppercase", marginTop: 5 }}>
            {world.family}
          </div>
        </div>
        <Pill status={status} size="sm">{densityLabels[world.density]}</Pill>
      </div>
      {!compact && (
        <div style={{ display: "flex", gap: 14, fontSize: 11, color: "var(--fg-2)", borderTop: "1px solid var(--border-1)", paddingTop: 10 }}>
          <Stat label="traces"  value={world.traces} mono/>
          <Stat label="motifs"  value={world.motifs} mono/>
          <Stat label="κ"       value={world.kappa == null ? "—" : world.kappa.toFixed(2)} mono/>
          <Stat label="falsif." value={world.falsifiers} mono fail={world.falsifiers > 0}/>
        </div>
      )}
    </div>
  );
};

const Stat = ({ label, value, mono, fail }) => (
  <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 3 }}>
    <span style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.2, color: "var(--fg-3)", textTransform: "uppercase" }}>{label}</span>
    <span style={{ font: `500 12px/1 ${mono ? "var(--font-mono)" : "var(--font-ui)"}`, color: fail ? "var(--status-falsified)" : "var(--fg-1)" }}>{value}</span>
  </div>
);

window.WorldCard = WorldCard;
