// ROOM 6 — Basin-Floor Geometry Lab
const BasinFloorLab = () => {
  return (
    <RoomShell>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        <Section span={6} title="Φ₂ closure · W1 CRN" eyebrow="floor: broad">
          <BasinFloor kind="broad" title="closure attractor" status="verified"
            points={[
              { x: 100, y: 130, outcome: "O1" }, { x: 150, y: 132, outcome: "O1" },
              { x: 200, y: 130, outcome: "O1" }, { x: 80, y: 90, outcome: "O3" },
              { x: 240, y: 100, outcome: "O3" },
            ]}/>
        </Section>
        <Section span={6} title="floor_connectivity · W13 (FALSIFIED)" eyebrow="floor: point-attractor">
          <BasinFloor kind="point" title="floor_connectivity" status="failed"
            points={[
              { x: 100, y: 80, outcome: "O5" }, { x: 160, y: 165, outcome: "O1" },
              { x: 240, y: 90, outcome: "O5" }, { x: 60, y: 70, outcome: "O5" },
            ]}/>
        </Section>
        <Section span={6} title="repair · W2 protocell" eyebrow="floor: rugged">
          <BasinFloor kind="rugged" title="repair manifold" status="warning"
            points={[
              { x: 70, y: 95, outcome: "O3" }, { x: 130, y: 130, outcome: "O3" },
              { x: 200, y: 115, outcome: "O3" }, { x: 270, y: 90, outcome: "O3" },
            ]}/>
        </Section>
        <Section span={6} title="Floor metrics" eyebrow="per-attractor"><Panel>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 80px 80px 80px 80px", gap: 8, alignItems: "center" }}>
            <div/>
            {["floor","width","dim","conf"].map(c => <div key={c} style={{ font: "500 9px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 1.2, textTransform: "uppercase", textAlign: "center" }}>{c}</div>)}
            {[
              ["closure",  "broad",  "0.42", "2.1", "0.86"],
              ["boundary", "broad",  "0.31", "1.8", "0.79"],
              ["repair",   "rugged", "0.28", "2.4", "0.61"],
              ["memory",   "—",      "—",    "—",   "—"],
              ["floor_connectivity", "point", "0.04", "0.0", "0.91 (falsified)"],
            ].map(([n, ...vals]) => (
              <React.Fragment key={n}>
                <div style={{ font: "400 12px/1 var(--font-ui)", color: "var(--fg-1)" }}>{n}</div>
                {vals.map((v, i) => (
                  <div key={i} style={{ font: "500 11px/1 var(--font-mono)",
                    color: v.includes("falsified") ? "var(--status-falsified)" : v === "—" ? "var(--fg-3)" : "var(--fg-1)",
                    textAlign: "center", padding: "6px 4px", borderRadius: 3,
                    background: v === "point" ? "rgba(255,92,122,0.10)" : "transparent" }}>{v}</div>
                ))}
              </React.Fragment>
            ))}
          </div>
        </Panel></Section>

        <Section span={12} title="Floor connectivity falsification arc" eyebrow="crown jewel narrative">
          <Panel><FalsificationArc/></Panel>
        </Section>

        <Section span={6} title="O1–O5 outcome distribution" eyebrow="closure (W1)"><Panel><OutcomeBars/></Panel></Section>
        <Section span={6} title="3D basin surface" eyebrow="W1 closure"><Panel>
          <EmptyState kind="not-yet-measured" reason="3D rendering requires perturbation density ≥ 200 points; currently 142"
            hint="exploratory · do not use for claims"/>
        </Panel></Section>
      </div>
    </RoomShell>
  );
};

const FalsificationArc = () => {
  const steps = [
    { t: "C010", label: "candidate", text: "floor_connectivity proposed", status: "exploratory" },
    { t: "C013", label: "replication", text: "candidate replicated", status: "verified" },
    { t: "CB-002", label: "confound", text: "BFG-PR confound flagged", status: "warning" },
    { t: "CODEX_AUDIT_002", label: "catch", text: "Codex catches D18 violation", status: "warning" },
    { t: "CB-003", label: "validation", text: "confound validated", status: "warning" },
    { t: "C014", label: "falsification", text: "point-attractor verdict · motif falsified", status: "falsified" },
  ];
  const colors = { exploratory: "var(--status-exploratory)", verified: "var(--status-verified)", warning: "var(--status-exploratory)", falsified: "var(--status-falsified)" };
  return (
    <div style={{ display: "flex", alignItems: "stretch", gap: 0, position: "relative" }}>
      {steps.map((s, i) => (
        <div key={i} style={{ flex: 1, display: "flex", flexDirection: "column", gap: 8, position: "relative", paddingRight: 8 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6, height: 16 }}>
            <span style={{ width: 12, height: 12, borderRadius: "50%", background: colors[s.status], boxShadow: `0 0 8px ${colors[s.status]}` }}/>
            {i < steps.length - 1 && <span style={{ flex: 1, height: 1, background: "var(--border-2)" }}/>}
          </div>
          <div style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.6 }}>{s.t}</div>
          <div style={{ font: "500 11px/1 var(--font-display)", color: colors[s.status], letterSpacing: 0.2, textTransform: "uppercase" }}>{s.label}</div>
          <div style={{ font: "400 11px/1.4 var(--font-ui)", color: "var(--fg-2)" }}>{s.text}</div>
        </div>
      ))}
    </div>
  );
};

const OutcomeBars = () => {
  const data = [
    { o: "O1 · recover",  n: 78, c: "var(--status-verified)" },
    { o: "O2 · drift",    n: 38, c: "var(--accent-trace)" },
    { o: "O3 · neighbor", n: 22, c: "var(--status-exploratory)" },
    { o: "O4 · novel",    n: 8,  c: "var(--accent-motif)" },
    { o: "O5 · escape",   n: 4,  c: "var(--status-falsified)" },
  ];
  const max = 80;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      {data.map(d => (
        <div key={d.o}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
            <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-2)", letterSpacing: 0.4 }}>{d.o}</span>
            <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-1)" }}>{d.n}</span>
          </div>
          <div style={{ height: 6, borderRadius: 3, background: "var(--bg-base)", overflow: "hidden" }}>
            <div style={{ width: `${(d.n / max) * 100}%`, height: "100%", background: d.c, boxShadow: `0 0 8px ${d.c}` }}/>
          </div>
        </div>
      ))}
    </div>
  );
};

window.BasinFloorLab = BasinFloorLab;
