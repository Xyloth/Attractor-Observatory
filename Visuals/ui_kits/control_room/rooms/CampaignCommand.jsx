// ROOM 3 — Campaign Command
const CampaignCommand = () => {
  const m = window.MOCK;
  const [selected, setSelected] = React.useState("C014");
  const sel = m.campaigns.find(c => c.id === selected);
  return (
    <RoomShell>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        <Section span={12} title="Campaign timeline" eyebrow="002 → 014">
          <Panel padded={false}>
            <CampaignTimeline campaigns={m.campaigns} current={selected}/>
          </Panel>
        </Section>

        <Section span={5} title={`${sel.id} · ${sel.title}`} eyebrow="campaign detail">
          <Panel>
            <div style={{ display: "flex", gap: 10, marginBottom: 14 }}>
              <Pill status={sel.status} size="md">{sel.status}</Pill>
              <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.4, alignSelf: "center" }}>
                {sel.date}
              </span>
            </div>
            <div style={{ marginBottom: 14 }}>
              <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", textTransform: "uppercase", marginBottom: 8 }}>gates</div>
              <GateGrid campaigns={[sel]}/>
            </div>
            <div>
              <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", textTransform: "uppercase", marginBottom: 8 }}>linked reports</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                {[
                  `reports/${sel.id}_substance_audit.md`,
                  `reports/${sel.id}_falsification_summary.md`,
                  `reports/${sel.id}_calibration_corpus.json`,
                ].map(r => (
                  <div key={r} style={{
                    padding: "6px 10px", borderRadius: 4,
                    background: "var(--bg-base)", border: "1px solid var(--border-1)",
                    font: "500 11px/1 var(--font-mono)", color: "var(--accent-trace)", letterSpacing: 0.3,
                  }}>{r}</div>
                ))}
              </div>
            </div>
          </Panel>
        </Section>

        <Section span={7} title="Campaign list" eyebrow="status · gates · audit">
          <Panel padded={false}>
            <div style={{ padding: 10 }}>
              <div style={{ display: "grid", gridTemplateColumns: "60px 1fr 100px 90px 90px", gap: 10, padding: "6px 10px",
                font: "500 9px/1 var(--font-mono)", letterSpacing: 1.2, color: "var(--fg-3)", textTransform: "uppercase",
                borderBottom: "1px solid var(--border-1)" }}>
                <span>id</span><span>title</span><span>status</span><span>passing</span><span>audits</span>
              </div>
              {m.campaigns.map(c => (
                <div key={c.id} onClick={() => setSelected(c.id)} style={{
                  display: "grid", gridTemplateColumns: "60px 1fr 100px 90px 90px", gap: 10,
                  padding: "8px 10px", borderRadius: 4,
                  background: c.id === selected ? "rgba(0,209,255,0.06)" : "transparent",
                  cursor: "pointer", alignItems: "center",
                }}>
                  <span style={{ font: "500 11.5px/1 var(--font-mono)", color: "var(--fg-2)", letterSpacing: 0.4 }}>{c.id}</span>
                  <span style={{ font: "400 12px/1 var(--font-ui)", color: "var(--fg-1)" }}>{c.title}</span>
                  <Pill status={c.status} size="sm">{c.status}</Pill>
                  <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-2)" }}>
                    {c.gates.filter(g => g === 1).length}/{c.gates.length}
                  </span>
                  <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)" }}>
                    {Math.floor(Math.random() * 8) + 2}
                  </span>
                </div>
              ))}
            </div>
          </Panel>
        </Section>

        <Section span={6} title="Branch lineage" eyebrow="campaigns as nodes">
          <Panel><BranchLineage/></Panel>
        </Section>
        <Section span={6} title="Stop-condition events" eyebrow="campaign halts + causes">
          <Panel padded={false}>
            <div style={{ padding: 12, display: "flex", flexDirection: "column", gap: 8 }}>
              {[
                { t: "2026-04-29", camp: "C014", cause: "FALSIFIER · floor_connectivity point-attractor", sev: "high" },
                { t: "2026-04-26", camp: "C013", cause: "Codex audit · BFG-PR confound (D18 violation)",  sev: "high" },
                { t: "2026-04-25", camp: "C012", cause: "Builder catch · biology shadow misclass.",       sev: "medium" },
                { t: "2026-03-29", camp: "C008", cause: "Codex+Builder · engineered floor (D17.5)",       sev: "high" },
              ].map((e, i) => (
                <div key={i} style={{
                  display: "flex", alignItems: "center", gap: 12,
                  padding: 10, borderRadius: 4,
                  background: "rgba(255,92,122,0.04)", border: "1px solid rgba(255,92,122,0.18)",
                }}>
                  <span style={{ width: 4, height: 36, background: "var(--status-falsified)", borderRadius: 2 }}/>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
                      <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)" }}>{e.t}</span>
                      <span style={{ font: "500 12px/1 var(--font-mono)", color: "var(--status-falsified)" }}>{e.camp}</span>
                    </div>
                    <div style={{ font: "400 12px/1.4 var(--font-ui)", color: "var(--fg-2)", marginTop: 4 }}>{e.cause}</div>
                  </div>
                  <Pill status={e.sev === "high" ? "falsified" : "warning"} size="sm">{e.sev}</Pill>
                </div>
              ))}
            </div>
          </Panel>
        </Section>

        <Section span={12} title="Fake-green risk" eyebrow="high pass rate + low audit coverage">
          <Panel>
            <EmptyState kind="not-yet-measured" reason="audit-coverage scoring not yet wired into campaign metadata"
              hint="planned for D17.5 follow-up · campaign C015"/>
          </Panel>
        </Section>
      </div>
    </RoomShell>
  );
};

const BranchLineage = () => {
  const W = 460, H = 200;
  const nodes = [
    { id: "C002", x: 30, y: 100, status: "verified" },
    { id: "C003", x: 90, y: 60,  status: "verified" },
    { id: "C004", x: 90, y: 140, status: "verified" },
    { id: "C006", x: 160, y: 100, status: "verified" },
    { id: "C008", x: 230, y: 60,  status: "verified" },
    { id: "C009", x: 290, y: 100, status: "active" },
    { id: "C010", x: 290, y: 40,  status: "verified" },
    { id: "C013", x: 360, y: 100, status: "verified" },
    { id: "C014", x: 420, y: 100, status: "failed" },
  ];
  const edges = [
    ["C002","C003"],["C002","C004"],["C003","C006"],["C004","C006"],
    ["C006","C008"],["C008","C009"],["C009","C010"],["C009","C013"],["C013","C014"],
  ];
  const colors = {
    verified: "var(--status-verified)",
    active: "var(--accent-trace)",
    failed: "var(--status-falsified)",
  };
  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", height: 200 }}>
      {edges.map(([a, b], i) => {
        const A = nodes.find(n => n.id === a), B = nodes.find(n => n.id === b);
        return <path key={i} d={`M${A.x} ${A.y} C ${A.x + 30} ${A.y}, ${B.x - 30} ${B.y}, ${B.x} ${B.y}`}
          fill="none" stroke="var(--border-2)" strokeWidth="1.2" opacity="0.7"/>;
      })}
      {nodes.map(n => (
        <g key={n.id}>
          <circle cx={n.x} cy={n.y} r="10" fill={colors[n.status]} fillOpacity="0.18" stroke={colors[n.status]} strokeWidth="1.5"
            style={{ filter: `drop-shadow(0 0 6px ${colors[n.status]})` }}/>
          <text x={n.x} y={n.y + 24} textAnchor="middle" style={{ font: "500 9.5px var(--font-mono)", fill: "var(--fg-2)", letterSpacing: 0.3 }}>{n.id}</text>
        </g>
      ))}
    </svg>
  );
};

window.CampaignCommand = CampaignCommand;
