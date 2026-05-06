// ==================== ROOMS ====================

// Shared layout helpers
const RoomShell = ({ children, intro }) => (
  <div style={{ flex: 1, overflow: "auto", padding: 20 }}>
    {intro}
    {children}
  </div>
);

const Section = ({ title, eyebrow, action, children, span = 12 }) => (
  <div style={{ gridColumn: `span ${span}`, display: "flex", flexDirection: "column", gap: 10 }}>
    {(title || eyebrow) && (
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 8 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
          {eyebrow && <span style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", textTransform: "uppercase" }}>{eyebrow}</span>}
          {title && <span style={{ font: "500 14.5px/1 var(--font-display)", color: "var(--fg-1)", letterSpacing: 0.1 }}>{title}</span>}
        </div>
        {action}
      </div>
    )}
    {children}
  </div>
);

// ==================== ROOM 1 — PULSE DECK ====================
//
// Hierarchy contract (per design direction):
//   First glance  — health badge, branch, latest tests, current task,
//                   plus a "needs attention" lane for any red/amber items.
//   Second glance — gate grid, calibration trend, recent falsifiers,
//                   audit catches.
//   Deep glance   — handled by other rooms (drilldown).
//
// We achieve hierarchy with size + color + position, not by removing data.
const PulseDeck = () => {
  const m = window.MOCK;
  const alerts = m.recentEvents.filter(e => e.kind === "failed" || e.kind === "warning").slice(0, 3);
  const failedCampaigns = m.campaigns.filter(c => c.status === "failed").length;
  const warnCampaigns   = m.campaigns.filter(c => c.status === "warning").length;
  return (
    <RoomShell>
      {/* ============ FIRST GLANCE ============ */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        {/* Big health badge — centerpiece. */}
        <div style={{ gridColumn: "span 4" }}>
          <Panel padded={false} glow="verified">
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "20px 16px 24px" }}>
              <HealthBadge score={m.health.score}/>
              <div style={{ display: "flex", gap: 4, marginTop: 16, flexWrap: "wrap", justifyContent: "center" }}>
                {m.health.components.map(c => (
                  <Pill key={c.name} status={c.status} size="sm" dot={false}>{c.name.replace("_", " ")} · {c.score.toFixed(2)}</Pill>
                ))}
              </div>
            </div>
          </Panel>
        </div>

        {/* Vital signs lane: branch / commit / tests / task + needs-attention */}
        <div style={{ gridColumn: "span 8", display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <MiniCard eyebrow="active branch" mono value={m.branch.name}
              meta={`+${m.branch.aheadOfMain} ahead · ${m.branch.dirty ? "dirty" : "clean"}`} status="active"/>
            <MiniCard eyebrow="latest commit" mono value={m.branch.lastCommit.sha}
              meta={`${m.branch.lastCommit.msg} · ${m.branch.lastCommit.author} · ${m.branch.lastCommit.agoMin}m ago`} status="verified"/>
            <MiniCard eyebrow="latest tests" mono value={`${m.tests.passed}p / ${m.tests.failed}f`}
              meta={`${(m.tests.runtimeMs/1000).toFixed(1)}s · ${m.tests.knownFailuresExcluded} known excluded`} status="verified"/>
            <MiniCard eyebrow="builder task" mono value={m.currentTask.id}
              meta={`${m.currentTask.elapsedH.toFixed(1)}h / ${m.currentTask.estimatedH.toFixed(1)}h · Δ ${m.currentTask.deltaForecast.toFixed(2)}`} status="active" agent="builder"/>
          </div>

          {/* Needs-attention lane — bright red/amber, jumps out, but compact. */}
          <NeedsAttention alerts={alerts} failed={failedCampaigns} warn={warnCampaigns}/>
        </div>

        {/* ============ SECOND GLANCE ============ */}

        <Section span={7} title="Gate status" eyebrow="campaigns × gates">
          <Panel padded><GateGrid campaigns={m.campaigns.slice(0, 9)}/></Panel>
        </Section>

        <Section span={5} title="What changed since last session" eyebrow="delta">
          <Panel>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {m.recentEvents.slice(0, 6).map((e, i) => <EventRow key={i} e={e}/>)}
            </div>
          </Panel>
        </Section>

        <Section span={12} title="Estimate vs actual · last 19 builder tasks" eyebrow="calibration">
          <Panel><CalibrationChart tasks={m.builderTasks}/></Panel>
        </Section>

        <Section span={6} title="Recent falsifiers" eyebrow="last 10 events">
          <Panel padded={false}>
            <div style={{ padding: 12, display: "flex", flexDirection: "column", gap: 10 }}>
              {m.falsifiers.map(f => <FalsifierEvent key={f.id} f={f} compact/>)}
            </div>
          </Panel>
        </Section>

        <Section span={6} title="Recent audit catches" eyebrow="cross-architecture">
          <Panel padded={false}>
            <div style={{ padding: 12, display: "flex", flexDirection: "column", gap: 8 }}>
              {[
                { agent: "codex",     catch: "BFG-PR confound · D18 violation",    sev: "high",   t: "4h" },
                { agent: "builder",   catch: "Class 12 candidate · stocked rooms", sev: "medium", t: "1d" },
                { agent: "architect", catch: "C012 biology shadow misclass.",      sev: "medium", t: "2d" },
                { agent: "codex",     catch: "C008 engineered floor (D17.5)",      sev: "high",   t: "5d" },
                { agent: "builder",   catch: "K7 calib drift outside band",        sev: "low",    t: "7d" },
              ].map((a, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <span style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)", width: 24 }}>{a.t}</span>
                  <AgentChip agent={a.agent} size={9}/>
                  <span style={{ font: "400 12px/1.4 var(--font-ui)", color: "var(--fg-2)", flex: 1 }}>{a.catch}</span>
                  <Pill status={a.sev === "high" ? "falsified" : a.sev === "medium" ? "warning" : "active"} size="sm" dot/>
                </div>
              ))}
            </div>
          </Panel>
        </Section>
      </div>
    </RoomShell>
  );
};

// "Needs attention" lane — visually loud so red/amber items jump.
// Lives directly under the vital-signs grid. Empty state is OK
// (D22 binding) — it should say "all clear" honestly.
const NeedsAttention = ({ alerts, failed, warn }) => {
  const map = { failed: "var(--status-falsified)", warning: "var(--status-exploratory)" };
  const allClear = alerts.length === 0;
  return (
    <div style={{
      background: allClear ? "var(--surface-1)" : "linear-gradient(90deg, rgba(255,84,104,0.06), rgba(245,166,35,0.04) 60%, transparent)",
      border: `1px solid ${allClear ? "var(--border-1)" : "var(--status-falsified)"}`,
      borderLeft: `3px solid ${allClear ? "var(--status-verified)" : "var(--status-falsified)"}`,
      borderRadius: "var(--radius-md)",
      padding: "10px 14px",
      display: "flex", alignItems: "center", gap: 14, minHeight: 52,
    }}>
      <span style={{
        font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, textTransform: "uppercase",
        color: allClear ? "var(--status-verified)" : "var(--status-falsified)",
        flexShrink: 0,
      }}>{allClear ? "all clear" : "needs attention"}</span>
      <span style={{
        font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.4,
        borderLeft: "1px solid var(--border-2)", paddingLeft: 12,
      }}>
        {failed} failed · {warn} warning
      </span>
      <div style={{ display: "flex", gap: 14, flex: 1, flexWrap: "wrap", overflow: "hidden" }}>
        {allClear ? (
          <span style={{ font: "400 12px/1.4 var(--font-ui)", color: "var(--fg-3)" }}>No falsifier or warning events in the last 24h. Background watchers green.</span>
        ) : alerts.map((e, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span style={{ width: 6, height: 6, borderRadius: "50%", background: map[e.kind], boxShadow: `0 0 6px ${map[e.kind]}` }}/>
            <span style={{ font: "400 12px/1.4 var(--font-ui)", color: "var(--fg-1)" }}>{e.text}</span>
            <span style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-4)", letterSpacing: 0.4 }}>{e.t}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const MiniCard = ({ eyebrow, value, meta, status, mono, agent }) => {
  const a = agent ? window.AGENTS[agent] : null;
  return (
  <div style={{
    background: "var(--surface-1)",
    border: "1px solid var(--border-1)",
    borderLeft: a ? `3px solid ${a.color}` : "1px solid var(--border-1)",
    borderRadius: "var(--radius-md)",
    padding: 12,
    display: "flex", flexDirection: "column", gap: 6,
    position: "relative", overflow: "hidden",
  }}>
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <span style={{ display: "flex", alignItems: "center", gap: 6, font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", textTransform: "uppercase" }}>
        {a && <AgentGlyph agent={agent} size={11}/>}
        {eyebrow}
      </span>
      <Pill status={status} size="sm" dot/>
    </div>
    <div style={{
      font: `500 16px/1.2 ${mono ? "var(--font-mono)" : "var(--font-display)"}`,
      color: "var(--fg-1)", letterSpacing: 0.1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
    }}>{value}</div>
    <div style={{ font: "400 11px/1.4 var(--font-mono)", color: "var(--fg-2)", letterSpacing: 0.2 }}>{meta}</div>
  </div>
  );
};

const EventRow = ({ e }) => {
  const map = { verified: "var(--status-verified)", active: "var(--accent-trace)", warning: "var(--status-exploratory)", failed: "var(--status-falsified)" };
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
      <span style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)", width: 30, letterSpacing: 0.4 }}>{e.t}</span>
      <span style={{ width: 6, height: 6, borderRadius: "50%", background: map[e.kind], boxShadow: `0 0 6px ${map[e.kind]}` }}/>
      <span style={{ font: "400 12px/1.4 var(--font-ui)", color: "var(--fg-2)", flex: 1 }}>{e.text}</span>
    </div>
  );
};

const CalibrationChart = ({ tasks }) => {
  const W = 600, H = 140, pad = 24;
  const maxY = 10;
  const x = i => pad + (i / (tasks.length - 1)) * (W - pad * 2);
  const y = v => H - pad - (v / maxY) * (H - pad * 2);
  const estPath = tasks.map((t, i) => `${i === 0 ? "M" : "L"} ${x(i)} ${y(t.est)}`).join(" ");
  const actPath = tasks.map((t, i) => `${i === 0 ? "M" : "L"} ${x(i)} ${y(t.act)}`).join(" ");
  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", height: 140 }}>
      {[2, 4, 6, 8].map(g => (
        <g key={g}>
          <line x1={pad} y1={y(g)} x2={W - pad} y2={y(g)} stroke="var(--border-2)" strokeDasharray="2 4" opacity="0.4"/>
          <text x={6} y={y(g) + 3} style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-3)" }}>{g}h</text>
        </g>
      ))}
      <path d={estPath} fill="none" stroke="var(--fg-3)" strokeWidth="1.5" strokeDasharray="3 3"/>
      <path d={actPath} fill="none" stroke="var(--agent-builder)" strokeWidth="2" style={{ filter: "drop-shadow(0 0 4px var(--agent-builder))" }}/>
      {tasks.map((t, i) => (
        <circle key={i} cx={x(i)} cy={y(t.act)} r="2.5" fill="var(--agent-builder)"/>
      ))}
      <g transform={`translate(${W - 180}, 12)`}>
        <line x1="0" y1="6" x2="14" y2="6" stroke="var(--fg-3)" strokeDasharray="3 3"/>
        <text x="20" y="9" style={{ font: "500 10px var(--font-mono)", fill: "var(--fg-3)" }}>estimated</text>
        <line x1="86" y1="6" x2="100" y2="6" stroke="var(--agent-builder)" strokeWidth="2"/>
        <text x="106" y="9" style={{ font: "500 10px var(--font-mono)", fill: "var(--agent-builder)" }}>actual (builder)</text>
      </g>
    </svg>
  );
};

window.PulseDeck = PulseDeck;
window.RoomShell = RoomShell;
window.Section = Section;
window.MiniCard = MiniCard;
window.EventRow = EventRow;
window.CalibrationChart = CalibrationChart;
