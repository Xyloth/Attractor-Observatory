// ROOM 5 — Motif Atlas
const MotifAtlas = () => {
  const m = window.MOCK;
  // Place motifs on a 2D embedding.
  const positions = {
    closure:       { x: 200, y: 140 },
    boundary:      { x: 320, y: 100 },
    repair:        { x: 380, y: 220 },
    memory:        { x: 480, y: 130 },
    coordination:  { x: 280, y: 260 },
    gradient:      { x: 140, y: 240 },
    floor_connectivity: { x: 540, y: 280 },
  };
  const edges = [
    ["closure","boundary"], ["closure","gradient"],
    ["boundary","repair"], ["repair","coordination"],
    ["memory","coordination"], ["closure","coordination"],
    ["gradient","boundary"], ["repair","floor_connectivity"],
  ];
  return (
    <RoomShell>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(12, 1fr)", gap: 16 }}>
        <Section span={8} title="Motif spatial embedding" eyebrow="shared-feature similarity · constellation map">
          <Panel padded={false}>
            <div style={{
              background: "radial-gradient(ellipse at 30% 30%, rgba(176,132,255,0.06), transparent 60%)," +
                          "radial-gradient(ellipse at 70% 70%, rgba(0,209,255,0.05), transparent 60%)," +
                          "var(--bg-base)",
              borderRadius: "var(--radius-lg)",
              minHeight: 400,
              position: "relative",
              overflow: "hidden",
            }}>
              <svg viewBox="0 0 700 400" style={{ width: "100%", height: 400, display: "block" }}>
                {/* faint grid */}
                <defs>
                  <pattern id="motif-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="var(--border-2)" strokeWidth="0.5" opacity="0.25"/>
                  </pattern>
                </defs>
                <rect width="700" height="400" fill="url(#motif-grid)"/>
                {/* edges = process-role / interaction-channel filaments */}
                {edges.map(([a, b], i) => {
                  const A = positions[a], B = positions[b];
                  return <line key={i} x1={A.x} y1={A.y} x2={B.x} y2={B.y}
                    stroke="var(--accent-motif)" strokeWidth="0.8" opacity="0.4"
                    style={{ filter: "drop-shadow(0 0 2px var(--accent-motif))" }}/>;
                })}
                {/* nodes */}
                {m.motifs.map(motif => (
                  <MotifNode key={motif.id} motif={motif} x={positions[motif.id].x} y={positions[motif.id].y} r={16}/>
                ))}
              </svg>
            </div>
          </Panel>
        </Section>

        <Section span={4} title="Motif registry" eyebrow="status · floor">
          <Panel padded={false}>
            <div style={{ padding: 10, display: "flex", flexDirection: "column", gap: 4 }}>
              {m.motifs.map(motif => (
                <div key={motif.id} style={{
                  display: "flex", alignItems: "center", gap: 10,
                  padding: 10, borderRadius: 4,
                  background: motif.status === "failed" ? "rgba(255,92,122,0.04)" : "transparent",
                  border: "1px solid var(--border-1)",
                }}>
                  <div style={{
                    width: 24, height: 24, borderRadius: "50%",
                    background: motif.status === "failed" ? "rgba(255,92,122,0.10)" : "rgba(176,132,255,0.10)",
                    border: `1px solid ${motif.status === "failed" ? "rgba(255,92,122,0.4)" : "rgba(176,132,255,0.4)"}`,
                  }}/>
                  <div style={{ flex: 1 }}>
                    <div style={{ font: "500 12px/1 var(--font-ui)", color: "var(--fg-1)" }}>{motif.id}</div>
                    <div style={{ font: "500 9px/1 var(--font-mono)", color: "var(--fg-3)", marginTop: 4, letterSpacing: 0.5 }}>floor · {motif.floor}</div>
                  </div>
                  <Pill status={motif.status} size="sm" dot={false}>{motif.status}</Pill>
                </div>
              ))}
            </div>
          </Panel>
        </Section>

        <Section span={6} title="Motif × world matrix" eyebrow="presence strength">
          <Panel padded={false}>
            <div style={{ padding: 12 }}>
              <div style={{ display: "grid", gridTemplateColumns: `120px repeat(7, 1fr)`, gap: 3 }}>
                <div/>
                {["W1","W2","W3","W4","W5","W6","W13"].map(w => (
                  <div key={w} style={{ font: "500 9px/1 var(--font-mono)", color: "var(--fg-3)", textAlign: "center", padding: 4, letterSpacing: 0.4 }}>{w}</div>
                ))}
                {m.motifs.map(motif => (
                  <React.Fragment key={motif.id}>
                    <div style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-2)", padding: "4px 6px", letterSpacing: 0.4, overflow: "hidden", textOverflow: "ellipsis" }}>{motif.id}</div>
                    {["W1","W2","W3","W4","W5","W6","W13"].map(w => {
                      const present = motif.worlds.includes(w);
                      const intensity = present ? Math.random() * 0.6 + 0.4 : 0;
                      return (
                        <div key={w} style={{
                          height: 18, borderRadius: 2,
                          background: present
                            ? motif.status === "failed"
                              ? `rgba(255,92,122,${intensity})`
                              : `rgba(176,132,255,${intensity})`
                            : "var(--bg-base)",
                          border: "1px solid var(--border-1)",
                        }}/>
                      );
                    })}
                  </React.Fragment>
                ))}
              </div>
            </div>
          </Panel>
        </Section>

        <Section span={6} title="Formal coverage" eyebrow="8 lenses × motif">
          <Panel padded={false}>
            <div style={{ padding: 12 }}>
              <div style={{ display: "grid", gridTemplateColumns: `120px repeat(8, 1fr)`, gap: 3 }}>
                <div/>
                {["dyn","topo","info","alg","cat","stat","geo","comp"].map(l => (
                  <div key={l} style={{ font: "500 9px/1 var(--font-mono)", color: "var(--fg-3)", textAlign: "center", padding: 4, letterSpacing: 0.4 }}>{l}</div>
                ))}
                {m.motifs.map(motif => (
                  <React.Fragment key={motif.id}>
                    <div style={{ font: "500 10px/1 var(--font-mono)", color: "var(--fg-2)", padding: "4px 6px", overflow: "hidden", textOverflow: "ellipsis" }}>{motif.id}</div>
                    {Array.from({length: 8}).map((_, i) => {
                      const v = Math.random();
                      const noData = v < 0.2;
                      return (
                        <div key={i} style={{
                          height: 18, borderRadius: 2,
                          background: noData ? "var(--bg-base)" : `rgba(82,224,162,${v * 0.7})`,
                          border: `1px ${noData ? "dashed" : "solid"} var(--border-1)`,
                        }}/>
                      );
                    })}
                  </React.Fragment>
                ))}
              </div>
            </div>
          </Panel>
        </Section>
      </div>
    </RoomShell>
  );
};

window.MotifAtlas = MotifAtlas;
