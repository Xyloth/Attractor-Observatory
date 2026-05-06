// ROOM 9 — Factory Intake Dock (quarantined)
const FactoryIntakeDock = () => {
  return (
    <RoomShell>
      {/* Persistent quarantine banner */}
      <div style={{
        background: "repeating-linear-gradient(45deg, rgba(255,184,0,0.06) 0 12px, rgba(255,184,0,0.10) 12px 24px)",
        border: "1px solid rgba(255,184,0,0.5)",
        borderRadius: "var(--radius-md)",
        padding: "14px 18px", marginBottom: 18,
        display: "flex", alignItems: "center", gap: 14,
      }}>
        <div style={{
          width: 36, height: 36, borderRadius: 6,
          background: "rgba(255,184,0,0.15)", border: "1px solid rgba(255,184,0,0.5)",
          display: "flex", alignItems: "center", justifyContent: "center",
          color: "var(--status-exploratory)",
        }}><RoomGlyph id="factory" size={22}/></div>
        <div style={{ flex: 1 }}>
          <div style={{ font: "500 11px/1 var(--font-mono)", color: "var(--status-exploratory)", letterSpacing: 1.6, textTransform: "uppercase", marginBottom: 4 }}>NOT FOR PROMOTION</div>
          <div style={{ font: "400 12.5px/1.5 var(--font-ui)", color: "var(--fg-2)" }}>
            All registries below are <strong style={{ color: "var(--fg-1)" }}>candidate</strong>. Promotion to claim-bearing requires
            source-bound extraction (D19), quarantine compliance (D20), and signed audit chain (D21).
          </div>
        </div>
        <Pill status="warning" size="md">quarantined</Pill>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        {[
          { id: "ProcessRole",        n: 84, sample: ["catalyst","template","membrane-host","sensor","substrate"] },
          { id: "InteractionChannel", n: 47, sample: ["covalent","electrostatic","mechanical","diffusive","signaling"] },
          { id: "OverlapField",       n: 31, sample: ["chemistry∩biology","digital∩cognitive","field∩swarm"] },
          { id: "TraitDecomposition", n: 62, sample: ["closure-component","boundary-component","memory-component"] },
        ].map(r => (
          <Section span={6} key={r.id} title={r.id} eyebrow={`registry preview · ${r.n} candidates`}>
            <Panel variant="quarantine">
              <div style={{ font: "500 10px/1.4 var(--font-mono)", color: "var(--status-exploratory)", letterSpacing: 0.6, marginBottom: 8 }}>
                ⚠ all entries unaudited · do not import into claim-bearing artifacts
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                {r.sample.map(s => (
                  <div key={s} style={{
                    padding: "6px 10px", borderRadius: 3,
                    background: "rgba(255,184,0,0.04)",
                    border: "1px dashed rgba(255,184,0,0.25)",
                    font: "500 11px/1 var(--font-mono)", color: "var(--fg-2)", letterSpacing: 0.3,
                  }}>{s}</div>
                ))}
              </div>
            </Panel>
          </Section>
        ))}

        <Section span={12} title="Candidate evidence lifecycle" eyebrow="state machine">
          <Panel>
            <div style={{ display: "flex", alignItems: "center", gap: 0 }}>
              {["ingested","audited","promoted/rejected"].map((s, i, arr) => (
                <React.Fragment key={s}>
                  <div style={{
                    flex: 1, padding: "16px 14px", borderRadius: "var(--radius-md)",
                    background: i === 0 ? "rgba(255,184,0,0.08)" : "var(--bg-base)",
                    border: `1px ${i === 0 ? "solid" : "dashed"} ${i === 0 ? "rgba(255,184,0,0.4)" : "var(--border-2)"}`,
                    textAlign: "center",
                  }}>
                    <div style={{ font: "500 9px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 1.2, textTransform: "uppercase" }}>step {i+1}</div>
                    <div style={{ font: "500 14px/1 var(--font-display)", color: "var(--fg-1)", marginTop: 8 }}>{s}</div>
                    <div style={{ font: "500 10px/1 var(--font-mono)", color: i === 0 ? "var(--status-exploratory)" : "var(--fg-3)", marginTop: 8, letterSpacing: 0.4 }}>
                      {i === 0 ? "224 entries" : i === 1 ? "0 audited" : "0 promoted"}
                    </div>
                  </div>
                  {i < arr.length - 1 && <div style={{ width: 32, textAlign: "center", color: "var(--fg-3)", fontFamily: "var(--font-mono)" }}>→</div>}
                </React.Fragment>
              ))}
            </div>
          </Panel>
        </Section>

        <Section span={12} title="Source-bound extraction doctrine" eyebrow="D19 · D20 · D21">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10 }}>
            {window.MOCK.doctrines.filter(d => ["D19","D20","D21"].includes(d.id)).map(d => <DoctrineTablet key={d.id} d={d}/>)}
          </div>
        </Section>
      </div>
    </RoomShell>
  );
};
window.FactoryIntakeDock = FactoryIntakeDock;

// ROOM 10 — Portfolio / Demo Mode
const PortfolioDemo = () => {
  return (
    <RoomShell>
      <div style={{
        background: "radial-gradient(ellipse at 30% 20%, rgba(0,209,255,0.08), transparent 50%)," +
                    "radial-gradient(ellipse at 80% 80%, rgba(176,132,255,0.06), transparent 50%)," +
                    "var(--bg-base)",
        borderRadius: "var(--radius-lg)",
        border: "1px solid var(--border-1)",
        padding: "48px 40px", marginBottom: 24, textAlign: "center",
      }}>
        <div style={{ font: "500 10px/1 var(--font-mono)", letterSpacing: 1.6, color: "var(--fg-3)", textTransform: "uppercase", marginBottom: 16 }}>Attractor Observatory · v0.14</div>
        <div style={{ font: "500 38px/1.1 var(--font-display)", color: "var(--fg-1)", letterSpacing: -0.5, maxWidth: 720, margin: "0 auto 14px" }}>
          A research observatory for living patterns, artificial worlds, and AI-built science.
        </div>
        <div style={{ font: "400 16px/1.5 var(--font-display-serif)", color: "var(--fg-2)", maxWidth: 640, margin: "0 auto", fontStyle: "italic" }}>
          Single demonstration: an AI agent that detects, calibrates, and falsifies the same recurring attractor motifs across 13 simulated worlds — and remembers when it was wrong.
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        <Section span={6} title="Architecture overview" eyebrow="system">
          <Panel><ArchitectureDiagram/></Panel>
        </Section>
        <Section span={6} title="AI-agent workflow" eyebrow="cross-audit triangle">
          <Panel><AgentTriangle/></Panel>
        </Section>

        <Section span={12} title="Curated screenshot capture" eyebrow="6 highest-impact views">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
            {[
              { name: "Pulse Deck", glyph: "pulse", caption: "Project at a glance" },
              { name: "World Observatory", glyph: "world", caption: "13 worlds × density × motifs" },
              { name: "Motif Atlas", glyph: "motif", caption: "Constellation of recurring forms" },
              { name: "Basin-Floor Lab", glyph: "basin", caption: "Floor falsification arc" },
              { name: "Falsifier Ledger", glyph: "falsifier", caption: "Failed honestly" },
              { name: "Project Graph", glyph: "graph", caption: "Living intelligence map" },
            ].map(s => (
              <div key={s.name} style={{
                background: "var(--surface-1)", border: "1px solid var(--border-1)",
                borderRadius: "var(--radius-md)", padding: 14,
              }}>
                <div style={{
                  height: 100, borderRadius: 4,
                  background: "radial-gradient(circle at 30% 30%, rgba(0,209,255,0.10), transparent 60%), var(--bg-base)",
                  border: "1px solid var(--border-1)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  color: "var(--accent-trace)", marginBottom: 10,
                }}>
                  <RoomGlyph id={s.glyph} size={36}/>
                </div>
                <div style={{ font: "500 13px/1 var(--font-display)", color: "var(--fg-1)" }}>{s.name}</div>
                <div style={{ font: "400 11px/1.4 var(--font-ui)", color: "var(--fg-3)", marginTop: 4 }}>{s.caption}</div>
              </div>
            ))}
          </div>
        </Section>
      </div>
    </RoomShell>
  );
};

const ArchitectureDiagram = () => (
  <svg viewBox="0 0 460 220" style={{ width: "100%", height: 220 }}>
    {[
      { x: 60,  y: 50,  w: 130, h: 36, label: "Worlds W1–W13", c: "var(--accent-trace)" },
      { x: 60,  y: 110, w: 130, h: 36, label: "Calibration K", c: "var(--accent-trace)" },
      { x: 60,  y: 170, w: 130, h: 36, label: "Trace store",   c: "var(--accent-trace)" },
      { x: 270, y: 80,  w: 130, h: 36, label: "Detector lens", c: "var(--accent-motif)" },
      { x: 270, y: 140, w: 130, h: 36, label: "Falsifier",     c: "var(--status-falsified)" },
    ].map((b, i) => (
      <g key={i}>
        <rect x={b.x} y={b.y} width={b.w} height={b.h} rx="4" fill={b.c} fillOpacity="0.08" stroke={b.c} strokeWidth="1"/>
        <text x={b.x + b.w/2} y={b.y + 22} textAnchor="middle" style={{ font: "500 11px var(--font-mono)", fill: b.c, letterSpacing: 0.4 }}>{b.label}</text>
      </g>
    ))}
    <path d="M 190 68 L 270 96" stroke="var(--border-2)"/>
    <path d="M 190 128 L 270 100" stroke="var(--border-2)"/>
    <path d="M 190 188 L 270 156" stroke="var(--border-2)"/>
    <path d="M 270 110 L 270 145" stroke="var(--status-falsified)" strokeDasharray="3 3"/>
  </svg>
);

const AgentTriangle = () => (
  <svg viewBox="0 0 360 220" style={{ width: "100%", height: 220 }}>
    {[
      { x: 180, y: 40, label: "Architect",   role: "designs", c: "var(--accent-motif)" },
      { x: 60,  y: 170, label: "Builder",    role: "implements", c: "var(--accent-trace)" },
      { x: 300, y: 170, label: "Codex",      role: "audits",  c: "var(--status-verified)" },
    ].map((n, i) => (
      <g key={i}>
        <circle cx={n.x} cy={n.y} r="32" fill={n.c} fillOpacity="0.10" stroke={n.c} strokeWidth="1.5"
          style={{ filter: `drop-shadow(0 0 8px ${n.c})` }}/>
        <text x={n.x} y={n.y - 4} textAnchor="middle" style={{ font: "500 12px var(--font-display)", fill: n.c }}>{n.label}</text>
        <text x={n.x} y={n.y + 12} textAnchor="middle" style={{ font: "500 9px var(--font-mono)", fill: "var(--fg-3)", letterSpacing: 0.4 }}>{n.role}</text>
      </g>
    ))}
    <path d="M 152 60 L 88 150" stroke="var(--border-2)" strokeWidth="1.2"/>
    <path d="M 208 60 L 272 150" stroke="var(--border-2)" strokeWidth="1.2"/>
    <path d="M 92 170 L 268 170" stroke="var(--border-2)" strokeWidth="1.2" strokeDasharray="3 3"/>
    <text x={180} y={195} textAnchor="middle" style={{ font: "500 10px var(--font-mono)", fill: "var(--fg-3)", letterSpacing: 0.6 }}>cross-audit</text>
  </svg>
);

window.PortfolioDemo = PortfolioDemo;
