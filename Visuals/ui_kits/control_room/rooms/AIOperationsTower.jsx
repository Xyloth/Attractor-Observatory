// ROOM 2 — AI Operations Tower
const AIOperationsTower = () => {
  const m = window.MOCK;
  return (
    <RoomShell>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        <Section span={8} title="Calibration trajectory" eyebrow="codex (25) + builder (19) · Δ vs estimate">
          <Panel><CalibrationTrajectory/></Panel>
        </Section>
        <Section span={4} title="Cross-architecture" eyebrow="convergence">
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            <AgentCard agent="codex"     arch="GPT-class"    calib={0.94} catches={47} status="verified"/>
            <AgentCard agent="builder"   arch="Sonnet-class" calib={0.91} catches={38} status="verified"/>
            <AgentCard agent="architect" arch="Sonnet-class" calib={null} catches={12} status="active"/>
            <AgentCard agent="gpt"       arch="GPT-class"    calib={null} catches={6}  status="verified"/>
            <AgentCard agent="human"     arch="—"            calib={null} catches={9}  status="verified"/>
          </div>
        </Section>

        <Section span={6} title="Defect catches by agent" eyebrow="per campaign · stacked">
          <Panel><CatchesBars/></Panel>
        </Section>
        <Section span={6} title="Estimate vs actual scatter" eyebrow="diagonal = perfect calibration">
          <Panel><ScatterChart/></Panel>
        </Section>

        <Section span={7} title="Mistake catalog" eyebrow="classes 1–12 · ratifying campaign">
          <Panel padded={false}>
            <div style={{ padding: 12, display: "flex", flexDirection: "column", gap: 6 }}>
              {[
                ["1","toy worlds","C002","verified"],["2","number-generator corpora","C002","verified"],
                ["3","engineered pass criteria","C002","verified"],["4","hardcoded science","C002","verified"],
                ["5","contaminated foundation","C006","verified"],["6","trivial gates","C006","verified"],
                ["7","unbounded substance","C007","verified"],["8","scenario-internal hardcoding","C007","verified"],
                ["9","engineered floor","C014","verified"],["10","scalar diversity","C009","verified"],
                ["11","post-hoc basis","C009","verified"],["12","decorative completeness","control_room","candidate"],
              ].map(([n, t, c, s]) => (
                <div key={n} style={{ display: "grid", gridTemplateColumns: "32px 1fr 80px 120px", alignItems: "center", gap: 10, padding: "4px 6px" }}>
                  <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)" }}>#{n}</span>
                  <span style={{ font: "400 12px/1 var(--font-ui)", color: "var(--fg-1)" }}>{t}</span>
                  <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-2)" }}>{c}</span>
                  <Pill status={s} size="sm">{s === "candidate" ? "candidate" : "ratified"}</Pill>
                </div>
              ))}
            </div>
          </Panel>
        </Section>

        <Section span={5} title="Audit disagreement ledger" eyebrow="who caught what">
          <Panel padded={false}>
            <div style={{ padding: 12, display: "flex", flexDirection: "column", gap: 8 }}>
              {[
                { catch: "BFG-PR confound", missed: ["builder"], caught: ["codex"], camp: "C013", sev: "high" },
                { catch: "Class 12 candidate", missed: ["codex","builder"], caught: ["human"], camp: "control_room", sev: "medium" },
                { catch: "C012 misclass", missed: ["codex"], caught: ["builder"], camp: "C012", sev: "medium" },
                { catch: "Engineered floor", missed: [], caught: ["codex","builder"], camp: "C014", sev: "high" },
              ].map((a, i) => (
                <div key={i} style={{ borderBottom: "1px solid var(--border-1)", paddingBottom: 8 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                    <span style={{ font: "500 12px/1 var(--font-ui)", color: "var(--fg-1)" }}>{a.catch}</span>
                    <Pill status={a.sev === "high" ? "falsified" : "warning"} size="sm">{a.sev}</Pill>
                  </div>
                  <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 6, font: "400 11px/1.4 var(--font-mono)", color: "var(--fg-3)" }}>
                    <span>missed by</span>
                    {a.missed.length === 0 ? <span style={{ color: "var(--fg-4)" }}>—</span>
                      : a.missed.map(ag => <AgentChip key={ag} agent={ag} variant="outline" size={9}/>)}
                    <span>· caught by</span>
                    {a.caught.map(ag => <AgentChip key={ag} agent={ag} size={9}/>)}
                    <span>· {a.camp}</span>
                  </div>
                </div>
              ))}
            </div>
          </Panel>
        </Section>

        <Section span={12} title="Agent activity stream" eyebrow="live">
          <Panel padded={false}>
            <div style={{ padding: 14, display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 10 }}>
              {m.recentEvents.map((e, i) => <EventRow key={i} e={e}/>)}
            </div>
          </Panel>
        </Section>
      </div>
    </RoomShell>
  );
};

const AgentCard = ({ agent, arch, calib, catches, status }) => {
  const a = window.AGENTS[agent];
  return (
  <div style={{
    background: "var(--surface-1)",
    border: `1px solid ${a.color}`,
    borderLeft: `3px solid ${a.color}`,
    borderRadius: "var(--radius-md)", padding: 12,
    display: "flex", alignItems: "center", gap: 12,
    boxShadow: status === "active" ? a.glow : "none",
  }}>
    <AgentAvatar agent={agent} size={36} glow={status === "active"}/>
    <div style={{ flex: 1, minWidth: 0 }}>
      <div style={{ font: "500 13px/1 var(--font-display)", color: "var(--fg-1)" }}>{a.label}</div>
      <div style={{ font: "500 10px/1 var(--font-mono)", color: a.color, marginTop: 4, letterSpacing: 0.5, opacity: 0.8 }}>{arch} · {a.role}</div>
    </div>
    <div style={{ textAlign: "right" }}>
      <div style={{ font: "500 14px/1 var(--font-mono)", color: "var(--fg-1)" }}>{calib != null ? calib.toFixed(2) : "—"}</div>
      <div style={{ font: "500 9px/1 var(--font-mono)", color: "var(--fg-3)", marginTop: 4, textTransform: "uppercase", letterSpacing: 1 }}>{catches} catches</div>
    </div>
  </div>
  );
};

const CalibrationTrajectory = () => {
  const W = 720, H = 220, pad = 32;
  // Codex synthesized: 25 tasks, converging to ~1.0 from ~0.5
  const codex = Array.from({ length: 25 }, (_, i) => 0.5 + (1 - Math.exp(-i/8)) * 0.5 + (Math.random() - 0.5) * 0.08);
  // Builder: 19 tasks, converging from ~0.3 to ~0.95
  const builder = Array.from({ length: 19 }, (_, i) => 0.3 + (1 - Math.exp(-i/5)) * 0.65 + (Math.random() - 0.5) * 0.08);
  const N = 25;
  const x = i => pad + (i / (N - 1)) * (W - pad * 2);
  const y = v => H - pad - ((v - 0) / 1.4) * (H - pad * 2);
  const path = (arr) => arr.map((v, i) => `${i === 0 ? "M" : "L"} ${x(i)} ${y(v)}`).join(" ");
  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", height: 220 }}>
      {[0.4, 0.7, 1.0, 1.3].map(g => (
        <g key={g}>
          <line x1={pad} y1={y(g)} x2={W - pad} y2={y(g)} stroke={g === 1.0 ? "var(--status-verified)" : "var(--border-2)"} strokeDasharray={g === 1.0 ? "0" : "2 4"} opacity={g === 1.0 ? 0.5 : 0.3}/>
          <text x={6} y={y(g) + 3} style={{ font: "500 9px var(--font-mono)", fill: g === 1.0 ? "var(--status-verified)" : "var(--fg-3)" }}>{g.toFixed(1)}</text>
        </g>
      ))}
      <path d={path(codex)} fill="none" stroke="var(--agent-codex)" strokeWidth="1.8" style={{ filter: "drop-shadow(0 0 3px var(--agent-codex))" }}/>
      <path d={path(builder)} fill="none" stroke="var(--agent-builder)" strokeWidth="1.8" style={{ filter: "drop-shadow(0 0 3px var(--agent-builder))" }}/>
      <text x={W - pad - 6} y={pad + 8} textAnchor="end" style={{ font: "500 10px var(--font-mono)", fill: "var(--agent-codex)" }}>codex (25)</text>
      <text x={W - pad - 6} y={pad + 22} textAnchor="end" style={{ font: "500 10px var(--font-mono)", fill: "var(--agent-builder)" }}>builder (19)</text>
      <text x={pad} y={H - 6} style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-3)" }}>task # →</text>
      <text x={pad} y={pad - 8} style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-3)" }}>↑ Δ (actual / estimated) — 1.0 = perfect</text>
    </svg>
  );
};

const CatchesBars = () => {
  const data = [
    { c: "C006", builder: 4, codex: 6, architect: 1 },
    { c: "C007", builder: 3, codex: 4, architect: 2 },
    { c: "C008", builder: 5, codex: 3, architect: 1 },
    { c: "C009", builder: 2, codex: 8, architect: 0 },
    { c: "C012", builder: 6, codex: 2, architect: 1 },
    { c: "C013", builder: 1, codex: 9, architect: 0 },
    { c: "C014", builder: 4, codex: 5, architect: 2 },
  ];
  const max = 16;
  const W = 360, H = 200, pad = 28;
  const bw = (W - pad * 2) / data.length - 6;
  const colors = { builder: "var(--agent-builder)", codex: "var(--agent-codex)", architect: "var(--agent-architect)" };
  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", height: 200 }}>
      {data.map((d, i) => {
        const xi = pad + i * ((W - pad * 2) / data.length);
        const total = d.builder + d.codex + d.architect;
        const scale = (H - pad * 1.5) / max;
        let yCur = H - pad;
        return (
          <g key={d.c}>
            {["builder", "codex", "architect"].map(k => {
              const h = d[k] * scale;
              yCur -= h;
              return <rect key={k} x={xi} y={yCur} width={bw} height={h} fill={colors[k]} opacity="0.8"/>;
            })}
            <text x={xi + bw/2} y={H - pad + 14} textAnchor="middle" style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-3)" }}>{d.c}</text>
          </g>
        );
      })}
      <g transform={`translate(${pad}, 8)`}>
        {["builder", "codex", "architect"].map((k, i) => (
          <g key={k} transform={`translate(${i * 80}, 0)`}>
            <rect width="10" height="10" fill={colors[k]}/>
            <text x="14" y="9" style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-2)" }}>{k}</text>
          </g>
        ))}
      </g>
    </svg>
  );
};

const ScatterChart = () => {
  const pts = window.MOCK.builderTasks;
  const W = 360, H = 200, pad = 28;
  const max = 10;
  const x = v => pad + (v / max) * (W - pad * 2);
  const y = v => H - pad - (v / max) * (H - pad * 2);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", height: 200 }}>
      <line x1={pad} y1={y(0)} x2={x(max)} y2={y(max)} stroke="var(--status-verified)" strokeDasharray="3 4" opacity="0.6"/>
      {[2,4,6,8].map(g => (
        <g key={g}>
          <line x1={pad} y1={y(g)} x2={W-pad} y2={y(g)} stroke="var(--border-2)" opacity="0.3"/>
          <line x1={x(g)} y1={pad} x2={x(g)} y2={H-pad} stroke="var(--border-2)" opacity="0.3"/>
        </g>
      ))}
      {pts.map((p, i) => {
        const earlyTask = i < 6;
        const c = earlyTask ? "var(--status-exploratory)" : "var(--accent-trace)";
        return <circle key={i} cx={x(p.est)} cy={y(p.act)} r="3.5" fill={c} opacity="0.85"/>;
      })}
      <text x={W/2} y={H-6} textAnchor="middle" style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-3)" }}>estimated (h) →</text>
      <text x={pad} y={pad-8} style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-3)" }}>↑ actual (h)</text>
    </svg>
  );
};

window.AIOperationsTower = AIOperationsTower;
