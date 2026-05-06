// ROOM 7 — Falsifier Ledger
const FalsifierLedger = () => {
  const m = window.MOCK;
  return (
    <RoomShell>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        <Section span={12} title="Falsifier timeline" eyebrow="chronological · color = severity">
          <Panel>
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {m.falsifiers.map(f => <FalsifierEvent key={f.id} f={f}/>)}
            </div>
          </Panel>
        </Section>

        <Section span={7} title="Negative-space map" eyebrow="five honest categories">
          <Panel padded={false}>
            <div style={{ padding: 14, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
              {[
                { k: "predicted_empty_basins",  n: 12, hint: "predicted absence confirmed" },
                { k: "simulation_only_attractors", n: 5, hint: "no biology homologue yet" },
                { k: "biology_only_motifs",     n: 3,  hint: "no simulation realization" },
                { k: "math_only_structures",    n: 7,  hint: "formal pattern, no instance" },
                { k: "unexplained_absences",    n: 2,  hint: "open · candidate falsifier" },
              ].map(c => (
                <div key={c.k} style={{
                  background: "var(--bg-base)",
                  border: "1px dashed var(--border-2)",
                  borderRadius: "var(--radius-md)",
                  padding: 12,
                }}>
                  <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: 6 }}>
                    <span style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-2)", letterSpacing: 0.4 }}>{c.k}</span>
                    <span style={{ font: "500 16px/1 var(--font-display)", color: "var(--fg-1)" }}>{c.n}</span>
                  </div>
                  <div style={{ font: "400 10.5px/1.4 var(--font-ui)", color: "var(--fg-3)" }}>{c.hint}</div>
                </div>
              ))}
            </div>
          </Panel>
        </Section>

        <Section span={5} title="Pre/post Truth Pass" eyebrow="downgrade comparison">
          <Panel>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 24px 1fr", gap: 8, alignItems: "stretch" }}>
              {[
                ["closure", "claim-bearing", "claim-bearing", "verified"],
                ["floor_connectivity", "claim-bearing", "falsified", "falsified"],
                ["memory", "claim-bearing", "exploratory", "warning"],
                ["repair", "exploratory", "exploratory", "verified"],
              ].map(([id, before, after, end]) => (
                <React.Fragment key={id}>
                  <div style={{
                    padding: 10, borderRadius: 4,
                    background: "var(--bg-base)", border: "1px solid var(--border-1)",
                  }}>
                    <div style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.5 }}>{id}</div>
                    <div style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-2)", marginTop: 6, letterSpacing: 0.3 }}>{before}</div>
                  </div>
                  <div style={{ alignSelf: "center", color: "var(--fg-3)", textAlign: "center", fontFamily: "var(--font-mono)" }}>→</div>
                  <div style={{
                    padding: 10, borderRadius: 4,
                    background: end === "falsified" ? "rgba(255,92,122,0.06)" : "var(--bg-base)",
                    border: `1px solid ${end === "falsified" ? "rgba(255,92,122,0.3)" : "var(--border-1)"}`,
                  }}>
                    <div style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.5 }}>after</div>
                    <Pill status={end} size="sm">{after}</Pill>
                  </div>
                </React.Fragment>
              ))}
            </div>
          </Panel>
        </Section>
      </div>
    </RoomShell>
  );
};
window.FalsifierLedger = FalsifierLedger;

// ROOM 8 — Doctrine and Integrity Console
const DoctrineConsole = () => {
  const m = window.MOCK;
  const ratified = m.doctrines.filter(d => d.mode === "binding");
  const candidates = m.doctrines.filter(d => d.mode === "candidate");
  const featured = ratified.find(d => d.id === "D22") || ratified[ratified.length - 1];
  const others = ratified.filter(d => d.id !== featured.id);
  return (
    <RoomShell>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        {/* Doctrine arc — chronological band of all D-rules */}
        <Section span={12} title="Doctrine arc" eyebrow="D7 → D22 · ratified rules across campaigns">
          <Panel padded>
            <div style={{ display: "flex", gap: 4, alignItems: "stretch", flexWrap: "wrap" }}>
              {ratified.map(d => (
                <div key={d.id} title={d.title} style={{
                  flex: "1 1 60px", minWidth: 60,
                  padding: "8px 6px",
                  border: "1px solid var(--border-2)",
                  borderTop: "2px solid var(--fg-3)",
                  borderRadius: 3,
                  background: "rgba(248,249,250,0.02)",
                  textAlign: "center",
                }}>
                  <div style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-1)", letterSpacing: 0.4 }}>{d.id}</div>
                  <div style={{ font: "500 9px/1.2 var(--font-mono)", color: "var(--fg-3)", marginTop: 4, letterSpacing: 0.3, textTransform: "uppercase" }}>{d.campaign}</div>
                </div>
              ))}
            </div>
          </Panel>
        </Section>

        {/* Featured rule — full ceremonial tablet */}
        <Section span={7} title="Featured rule · centerpiece" eyebrow="signed · binding">
          <DoctrineTablet d={featured}/>
        </Section>

        {/* Pending proposals — candidates, dashed treatment */}
        <Section span={5} title="Pending proposals" eyebrow="under review · class 12 lives here">
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {candidates.map(d => <DoctrineTablet key={d.id} d={d}/>)}
            {candidates.length === 0 && <div style={{
              padding: 14, border: "1px dashed var(--border-dashed-1)", borderRadius: "var(--radius-md)",
              font: "400 12px/1.5 var(--font-ui)", color: "var(--fg-3)",
            }}>No candidate proposals. The constitution is stable.</div>}
          </div>
        </Section>

        {/* Compact registry — every other ratified rule */}
        <Section span={12} title="Registry · every binding rule" eyebrow="signed · content-locked">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 10 }}>
            {others.map(d => <DoctrineTablet key={d.id} d={d} compact/>)}
          </div>
        </Section>

        <Section span={6} title="Active lints" eyebrow="enforcing doctrine">
          <Panel padded={false}>
            <div style={{ padding: 12, display: "flex", flexDirection: "column", gap: 6 }}>
              {[
                ["lint_no_hardcoded_science",     "D10", "verified"],
                ["lint_no_engineered_pass",        "D9",  "verified"],
                ["lint_no_softened_floors",        "D17.5","verified"],
                ["lint_substance_budget",          "D13", "verified"],
                ["lint_basis_content_lock",        "D18", "verified"],
                ["lint_quarantine_no_promote",     "D20", "verified"],
                ["lint_class_12_decorative",       "D22", "candidate"],
              ].map(([n, d, s]) => (
                <div key={n} style={{
                  display: "flex", alignItems: "center", gap: 10,
                  padding: "8px 10px", borderRadius: 4,
                  border: "1px solid var(--border-1)",
                }}>
                  <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-1)", flex: 1, letterSpacing: 0.3 }}>{n}</span>
                  <span style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-3)" }}>→ {d}</span>
                  <Pill status={s} size="sm">{s === "candidate" ? "draft" : "active"}</Pill>
                </div>
              ))}
            </div>
          </Panel>
        </Section>

        <Section span={6} title="Mistake catalog cross-link" eyebrow="class 1–12 ↔ ratifying doctrine">
          <Panel padded>
            <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
              {[
                ["1", "toy worlds",             "D7"],
                ["2", "number-generator corpora","D8"],
                ["3", "engineered pass criteria","D9"],
                ["4", "hardcoded science",       "D10"],
                ["5", "contaminated foundation", "D11"],
                ["6", "trivial gates",           "D12"],
                ["7", "unbounded substance",     "D13"],
                ["8", "scenario-internal hardcoding","D14"],
                ["9", "engineered floor",        "D15·D17"],
                ["10","scalar diversity",        "D16"],
                ["11","post-hoc basis",          "D18"],
                ["12","decorative completeness", "D22"],
              ].map(([n, t, d]) => (
                <div key={n} style={{ display: "grid", gridTemplateColumns: "32px 1fr 110px", alignItems: "center", gap: 8, padding: "4px 0", borderBottom: "1px solid var(--border-1)" }}>
                  <span style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)" }}>#{n}</span>
                  <span style={{ font: "400 12px/1.4 var(--font-ui)", color: "var(--fg-1)" }}>{t}</span>
                  <span style={{ font: "500 11px/1 var(--font-mono)", color: n === "12" ? "var(--status-exploratory)" : "var(--fg-2)", textAlign: "right", letterSpacing: 0.4 }}>→ {d}</span>
                </div>
              ))}
            </div>
          </Panel>
        </Section>
      </div>
    </RoomShell>
  );
};
window.DoctrineConsole = DoctrineConsole;
