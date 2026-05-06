// DoctrineTablet — signed rule card. Fraunces serif for the rule
// title only. Treatment evokes "signed scientific law" (engraved
// surface, content-hash seal, ratifying-campaign mark, invocation
// count) — NOT fantasy parchment. Body copy stays sober.
//
// Two surfaces:
//   compact  — used in lists / drawers
//   full     — Doctrine Console centerpiece. Engraved card, hash seal,
//              ratifying campaign badge, invocation counter.

const DoctrineTablet = ({ d, compact = false }) => {
  const isCandidate = d.mode === "candidate";
  const accent = isCandidate ? "var(--status-exploratory)" : "var(--fg-2)";
  const accentSoft = isCandidate ? "rgba(245,166,35,0.06)" : "rgba(248,249,250,0.02)";
  // Pseudo-deterministic invocation count from id; mock-only.
  const invocations = d.id === "D22" ? 14 : d.id === "D17" ? 9 : (parseInt(d.id.replace(/\D/g,"")) * 3 + 7);

  if (compact) {
    return (
      <div style={{
        background: accentSoft,
        border: `1px ${isCandidate ? "dashed" : "solid"} ${isCandidate ? "rgba(245,166,35,0.35)" : "var(--border-1)"}`,
        borderLeft: `3px solid ${isCandidate ? "var(--status-exploratory)" : "var(--fg-3)"}`,
        borderRadius: "var(--radius-md)",
        padding: 12,
        display: "flex", flexDirection: "column", gap: 6,
      }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 8 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10, minWidth: 0 }}>
            <span style={{
              font: "500 13px/1 var(--font-mono)", color: "var(--fg-1)", letterSpacing: 0.4,
              padding: "3px 7px", border: "1px solid var(--border-2)", borderRadius: 4,
              flexShrink: 0,
            }}>{d.id}</span>
            <span style={{
              font: "500 14px/1.25 var(--font-display-serif)", color: "var(--fg-1)",
              fontStyle: "italic", letterSpacing: 0.05,
            }}>{d.title}</span>
          </div>
          <Pill status={isCandidate ? "candidate" : "verified"} size="sm">{d.mode}</Pill>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      position: "relative",
      background: `
        linear-gradient(180deg, rgba(248,249,250,0.025) 0%, transparent 30%),
        ${accentSoft},
        var(--surface-1)
      `,
      border: `1px ${isCandidate ? "dashed" : "solid"} ${isCandidate ? "rgba(245,166,35,0.4)" : "var(--border-2)"}`,
      borderRadius: "var(--radius-lg)",
      padding: "18px 20px 16px",
      display: "flex", flexDirection: "column", gap: 12,
      boxShadow: isCandidate
        ? "0 1px 0 rgba(255,255,255,0.04) inset, 0 12px 32px -16px rgba(0,0,0,0.5)"
        : "0 1px 0 rgba(255,255,255,0.05) inset, 0 1px 0 rgba(0,0,0,0.4) inset, 0 12px 32px -16px rgba(0,0,0,0.55)",
    }}>
      {/* Engraved hairline frame */}
      <div aria-hidden style={{
        position: "absolute", inset: 6, borderRadius: 8,
        border: `1px solid ${isCandidate ? "rgba(245,166,35,0.12)" : "rgba(248,249,250,0.04)"}`,
        pointerEvents: "none",
      }}/>

      {/* Header — id chip · title · mode */}
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, position: "relative" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, minWidth: 0, flex: 1 }}>
          <span style={{
            font: "500 14px/1 var(--font-mono)", color: accent, letterSpacing: 0.6,
            padding: "5px 9px",
            border: `1px solid ${isCandidate ? "rgba(245,166,35,0.5)" : "var(--border-2)"}`,
            borderRadius: 4,
            background: isCandidate ? "rgba(245,166,35,0.08)" : "rgba(248,249,250,0.03)",
            flexShrink: 0,
            boxShadow: "0 1px 0 rgba(0,0,0,0.3) inset",
          }}>{d.id}</span>
          <div style={{ minWidth: 0 }}>
            <div style={{
              font: "500 18px/1.25 var(--font-display-serif)",
              fontStyle: "italic",
              color: "var(--fg-1)",
              letterSpacing: 0.1,
            }}>{d.title}</div>
            <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.6, color: "var(--fg-3)", textTransform: "uppercase", marginTop: 5 }}>
              {isCandidate ? "candidate · awaiting ratification" : "ratified · binding"}
            </div>
          </div>
        </div>
        <Pill status={isCandidate ? "candidate" : "verified"} size="sm">{d.mode}</Pill>
      </div>

      {/* Failure (motivating) — sober body type */}
      <div style={{
        font: "400 12.5px/1.55 var(--font-ui)", color: "var(--fg-2)",
        borderLeft: `2px solid ${isCandidate ? "rgba(245,166,35,0.35)" : "var(--border-2)"}`,
        paddingLeft: 12,
      }}>
        <span style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", textTransform: "uppercase", display: "block", marginBottom: 4 }}>motivating failure</span>
        {d.failure}
      </div>

      {/* Footer — seal · ratifying campaign · invocations */}
      <div style={{
        display: "grid", gridTemplateColumns: "1fr 1fr 1fr",
        gap: 0,
        borderTop: `1px solid ${isCandidate ? "rgba(245,166,35,0.18)" : "var(--border-1)"}`,
        paddingTop: 10,
        marginTop: 2,
      }}>
        <FooterCell label="seal" value={d.hash} mono accent={isCandidate ? "var(--status-exploratory)" : "var(--fg-2)"}/>
        <FooterCell label="ratifying" value={d.campaign} mono accent={isCandidate ? "var(--status-exploratory)" : "var(--fg-2)"}/>
        <FooterCell label="invocations" value={isCandidate ? "—" : invocations.toString()} mono accent={isCandidate ? "var(--status-exploratory)" : "var(--fg-1)"}/>
      </div>
    </div>
  );
};

const FooterCell = ({ label, value, mono, accent }) => (
  <div style={{ display: "flex", flexDirection: "column", gap: 3, paddingRight: 10 }}>
    <span style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", textTransform: "uppercase" }}>{label}</span>
    <span style={{ font: `500 11.5px/1 ${mono ? "var(--font-mono)" : "var(--font-ui)"}`, color: accent, letterSpacing: 0.3 }}>{value}</span>
  </div>
);

window.DoctrineTablet = DoctrineTablet;
