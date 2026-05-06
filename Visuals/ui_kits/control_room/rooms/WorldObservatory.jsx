// ROOM 4 — World Observatory
const WorldObservatory = () => {
  const m = window.MOCK;
  const [focusId, setFocusId] = React.useState("W2");
  const focus = m.worlds.find(w => w.id === focusId) || m.worlds[0];
  const families = ["chemistry","biology","cognitive","digital","multiscale"];
  return (
    <RoomShell>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        {/* World Chamber detail — thumbnail centerpiece */}
        <Section span={12} title={`Chamber · ${focus.id} ${focus.name}`} eyebrow="active drilldown · click any world card below to switch">
          <Panel padded={false}>
            <div style={{ display: "grid", gridTemplateColumns: "260px 1fr", gap: 0 }}>
              <div style={{ padding: 18, borderRight: "1px solid var(--border-1)", display: "flex", flexDirection: "column", alignItems: "center", gap: 12, background: `radial-gradient(ellipse at 50% 0%, var(${focus.hue})12, transparent 70%)` }}>
                <WorldThumbnail id={focus.id} size={220}/>
                <div style={{ textAlign: "center" }}>
                  <div style={{ font: "500 11px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 0.6 }}>{focus.id} · {focus.family}</div>
                  <div style={{ font: "500 22px/1.1 var(--font-display)", color: "var(--fg-1)", marginTop: 6 }}>{focus.name}</div>
                </div>
                <Pill status={focus.density.includes("claim") ? "verified" : focus.density === "skeleton" ? "missing" : "exploratory"} size="sm">{focus.density.replace(/_/g, " ")}</Pill>
              </div>
              <div style={{ padding: 18, display: "flex", flexDirection: "column", gap: 14 }}>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10 }}>
                  {[
                    ["traces", focus.traces],
                    ["motifs", focus.motifs],
                    ["κ (calib)", focus.kappa == null ? "—" : focus.kappa.toFixed(2)],
                    ["falsifiers", focus.falsifiers],
                  ].map(([k, v], i) => (
                    <div key={i} style={{ background: "var(--surface-2)", border: "1px solid var(--border-1)", borderRadius: "var(--radius-md)", padding: 10 }}>
                      <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.2, color: "var(--fg-3)", textTransform: "uppercase" }}>{k}</div>
                      <div style={{ font: `500 18px/1 var(--font-mono)`, color: i === 3 && v > 0 ? "var(--status-falsified)" : "var(--fg-1)", marginTop: 6 }}>{v}</div>
                    </div>
                  ))}
                </div>
                <div>
                  <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", textTransform: "uppercase", marginBottom: 8 }}>Recent activity</div>
                  <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                    {[
                      `K-corpus locked · ${focus.id.toLowerCase()}_k${(parseInt(focus.id.slice(1))*7) % 31}`,
                      `${focus.motifs} motif${focus.motifs===1?"":"s"} present · ${focus.falsifiers > 0 ? "1 falsified" : "all calibrated"}`,
                      focus.density === "skeleton"
                        ? "skeleton · awaiting densification campaign"
                        : "trace validation passed (D17.5)",
                    ].map((s, i) => (
                      <div key={i} style={{ font: "400 12px/1.4 var(--font-ui)", color: "var(--fg-2)", display: "flex", gap: 8 }}>
                        <span style={{ width: 4, height: 4, borderRadius: "50%", background: `var(${focus.hue})`, marginTop: 7, flexShrink: 0 }}/>
                        {s}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </Panel>
        </Section>

        <Section span={12} title="Worlds W1–W13" eyebrow="density × family">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }}>
            {m.worlds.map(w => <WorldCard key={w.id} world={w} onClick={() => setFocusId(w.id)}/>)}
          </div>
        </Section>

        <Section span={7} title="World × metrics heatmap" eyebrow="density · trace · κ · falsifier · motif">
          <Panel><WorldHeatmap/></Panel>
        </Section>

        <Section span={5} title="Density legend" eyebrow="five honest states">
          <Panel>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {[
                { k: "skeleton", count: 5, status: "missing", label: "60–80 lines · stub only" },
                { k: "trace-valid sparse", count: 3, status: "exploratory", label: "validated traces · low N" },
                { k: "exploratory densified", count: 3, status: "exploratory", label: "high N · pre-calibration" },
                { k: "calibration-backed", count: 0, status: "verified", label: "K-corpus locked" },
                { k: "claim-ready densified", count: 2, status: "verified", label: "K-locked + audit-passed" },
              ].map(d => (
                <div key={d.k} style={{ display: "grid", gridTemplateColumns: "180px 1fr 32px", gap: 10, alignItems: "center", padding: "6px 0", borderBottom: "1px solid var(--border-1)" }}>
                  <Pill status={d.status} size="sm">{d.k}</Pill>
                  <span style={{ font: "400 11.5px/1.4 var(--font-ui)", color: "var(--fg-2)" }}>{d.label}</span>
                  <span style={{ font: "500 13px/1 var(--font-mono)", color: "var(--fg-1)", textAlign: "right" }}>{d.count}</span>
                </div>
              ))}
            </div>
          </Panel>
        </Section>

        <Section span={12} title="Substance audit cards" eyebrow="W6–W13 · D17.5 audit">
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }}>
            {m.worlds.filter(w => parseInt(w.id.slice(1)) >= 6).map(w => (
              <div key={w.id} style={{
                background: "var(--surface-1)", border: "1px solid var(--border-1)",
                borderRadius: "var(--radius-md)", padding: 14,
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                  <WorldGlyph id={w.id} size={22} color={`var(${w.hue})`}/>
                  <span style={{ font: "500 12px/1 var(--font-mono)", color: "var(--fg-3)" }}>{w.id}</span>
                  <span style={{ font: "500 13px/1 var(--font-display)", color: "var(--fg-1)" }}>{w.name}</span>
                </div>
                <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.2, color: "var(--fg-3)", textTransform: "uppercase", marginBottom: 6 }}>verdict</div>
                <Pill status={w.density === "skeleton" ? "missing" : w.density.includes("claim") ? "verified" : "exploratory"} size="sm">
                  {w.density === "skeleton" ? "audit pending" : w.density.includes("claim") ? "passed strict" : "softened-floor"}
                </Pill>
                <div style={{ font: "500 10px/1.4 var(--font-mono)", color: "var(--fg-3)", marginTop: 10, letterSpacing: 0.4 }}>
                  signed-by · codex+builder<br/>
                  hash · {w.id.toLowerCase()}_a{Math.floor(Math.random() * 9000) + 1000}
                </div>
              </div>
            ))}
          </div>
        </Section>
      </div>
    </RoomShell>
  );
};

const WorldHeatmap = () => {
  const m = window.MOCK;
  const cols = ["density","trace","κ","falsif.","motifs"];
  const cellColor = (v) => {
    if (v == null) return "rgba(120,138,168,0.06)";
    const t = Math.max(0, Math.min(1, v));
    return `rgba(0, 209, 255, ${0.06 + t * 0.6})`;
  };
  const densityScore = { skeleton: 0.05, trace_valid_sparse: 0.3, exploratory_densified: 0.55, calibration_backed: 0.85, claim_ready_densified: 1 };
  return (
    <div style={{ display: "grid", gridTemplateColumns: `60px repeat(${cols.length}, 1fr)`, gap: 4 }}>
      <div/>
      {cols.map(c => <div key={c} style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.2, color: "var(--fg-3)", textTransform: "uppercase", textAlign: "center", padding: 4 }}>{c}</div>)}
      {m.worlds.map(w => {
        const traceN = Math.min(1, w.traces / 150);
        const kappa = w.kappa;
        const falsScore = w.falsifiers > 0 ? 1 : 0;
        const motifScore = w.motifs / 6;
        const vals = [densityScore[w.density], traceN, kappa, falsScore, motifScore];
        return (
          <React.Fragment key={w.id}>
            <div style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-2)", padding: "6px 4px", letterSpacing: 0.4 }}>{w.id}</div>
            {vals.map((v, i) => (
              <div key={i} style={{
                height: 22, borderRadius: 3, background: i === 3 && v ? "rgba(255,92,122,0.4)" : cellColor(v),
                border: "1px solid var(--border-1)",
                display: "flex", alignItems: "center", justifyContent: "center",
                font: "500 10px/1 var(--font-mono)", color: "var(--fg-2)",
              }}>{v == null ? "—" : v.toFixed(2).replace(/^0/, "")}</div>
            ))}
          </React.Fragment>
        );
      })}
    </div>
  );
};

window.WorldObservatory = WorldObservatory;
