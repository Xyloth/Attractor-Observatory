// Living Project Graph — the iconic centerpiece. Force-positioned nodes:
// worlds · campaigns · motifs · agents · doctrines · falsifiers · reports.
// Edges typed: produced / audited / falsified / depends-on / detected-in /
// modifies / supports / conflicts-with.
const ProjectGraph = () => {
  const [filter, setFilter] = React.useState({ world: true, campaign: true, motif: true, agent: true, doctrine: true, falsifier: true, report: true });
  const [edgeFilter, setEdgeFilter] = React.useState({ produced: true, audited: true, falsified: true, "depends-on": true, "detected-in": true });
  const [hover, setHover] = React.useState(null);
  const [t, setT] = React.useState(1); // 0..1 transition

  // Hand-placed for legibility; real impl would be force-directed.
  const nodes = [
    // worlds (cyan ring)
    { id: "W1",  type: "world", x: 140, y: 200, label: "W1 CRN",        status: "verified" },
    { id: "W2",  type: "world", x: 100, y: 320, label: "W2 Protocell",  status: "verified" },
    { id: "W3",  type: "world", x: 220, y: 130, label: "W3 Field",      status: "exploratory" },
    { id: "W5",  type: "world", x: 90,  y: 460, label: "W5 Digital",    status: "exploratory" },
    { id: "W13", type: "world", x: 200, y: 540, label: "W13 Multiscale",status: "exploratory" },
    // motifs (violet)
    { id: "closure",      type: "motif", x: 360, y: 220, status: "verified" },
    { id: "boundary",     type: "motif", x: 380, y: 320, status: "verified" },
    { id: "memory",       type: "motif", x: 340, y: 430, status: "warning" },
    { id: "floor_conn",   type: "motif", x: 320, y: 540, status: "failed" },
    // campaigns
    { id: "C006", type: "campaign", x: 540, y: 130, status: "verified" },
    { id: "C009", type: "campaign", x: 540, y: 240, status: "active"   },
    { id: "C013", type: "campaign", x: 540, y: 340, status: "verified" },
    { id: "C014", type: "campaign", x: 540, y: 460, status: "failed"   },
    // agents
    { id: "Codex",     type: "agent", x: 740, y: 100, status: "verified" },
    { id: "Builder",   type: "agent", x: 760, y: 220, status: "active"   },
    { id: "Architect", type: "agent", x: 760, y: 360, status: "verified" },
    // doctrines
    { id: "D17", type: "doctrine", x: 700, y: 480, status: "verified" },
    { id: "D18", type: "doctrine", x: 760, y: 540, status: "verified" },
    { id: "D22", type: "doctrine", x: 620, y: 560, status: "warning" },
    // falsifiers
    { id: "F-014-1", type: "falsifier", x: 440, y: 600, status: "failed" },
    // reports
    { id: "rep-C014", type: "report", x: 660, y: 600, status: "warning" },
  ];
  const edges = [
    ["W1","closure","detected-in"],["W2","closure","detected-in"],["W3","closure","detected-in"],
    ["W2","boundary","detected-in"],["W5","memory","detected-in"],["W13","floor_conn","detected-in"],
    ["closure","C006","produced"],["boundary","C009","produced"],["floor_conn","C014","produced"],
    ["memory","C013","produced"],
    ["C014","F-014-1","falsified"],["floor_conn","F-014-1","falsified"],
    ["Codex","C013","audited"],["Codex","C009","audited"],["Builder","C014","audited"],
    ["C014","D17","depends-on"],["C009","D18","depends-on"],
    ["C014","rep-C014","produced"],["F-014-1","rep-C014","supports"],
  ];

  // Compute alternate layouts. Each returns {id: {x, y}}.
  const layouts = React.useMemo(() => {
    const W = 900, H = 680, cx = W / 2, cy = H / 2;
    const curated = Object.fromEntries(nodes.map(n => [n.id, { x: n.x, y: n.y }]));

    // Constellation: deterministic pseudo-force scatter by type cluster.
    const typeAnchor = {
      world:     { x: 200, y: 250 },
      motif:     { x: 380, y: 350 },
      campaign:  { x: 540, y: 280 },
      agent:     { x: 730, y: 220 },
      doctrine:  { x: 700, y: 500 },
      falsifier: { x: 460, y: 580 },
      report:    { x: 640, y: 580 },
    };
    const hash = (s) => { let h = 0; for (let i = 0; i < s.length; i++) h = ((h<<5)-h + s.charCodeAt(i)) | 0; return h; };
    const constellation = Object.fromEntries(nodes.map(n => {
      const a = typeAnchor[n.type] || { x: cx, y: cy };
      const h1 = hash(n.id), h2 = hash(n.id + "y");
      return [n.id, {
        x: a.x + ((h1 % 200) - 100) * 0.9,
        y: a.y + ((h2 % 200) - 100) * 0.9,
      }];
    }));

    // Radial: rings by type. worlds inner, motifs, campaigns, agents/doctrines outer.
    const ringRadius = { world: 90, motif: 170, campaign: 240, agent: 320, doctrine: 320, falsifier: 290, report: 290 };
    const byType = {};
    nodes.forEach(n => { (byType[n.type] = byType[n.type] || []).push(n.id); });
    const radial = {};
    Object.entries(byType).forEach(([type, ids]) => {
      const r = ringRadius[type] || 250;
      ids.forEach((id, i) => {
        const ang = (i / ids.length) * Math.PI * 2 - Math.PI / 2;
        radial[id] = { x: cx + Math.cos(ang) * r, y: cy + Math.sin(ang) * r };
      });
    });

    return { curated, constellation, radial };
  }, []);

  const [fromLayout, setFromLayout] = React.useState("curated");
  const [toLayout, setToLayout] = React.useState("curated");

  const switchLayout = (next) => {
    if (next === toLayout) return;
    setFromLayout(toLayout);
    setToLayout(next);
    setT(0);
  };

  React.useEffect(() => {
    if (t >= 1) return;
    let raf, start;
    const tick = (ts) => {
      if (!start) start = ts;
      const p = Math.min(1, (ts - start) / 600);
      const eased = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      setT(eased);
      if (p < 1) raf = requestAnimationFrame(tick);
      else setT(1);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [toLayout]);

  // Resolve current node positions via lerp.
  const pos = (id) => {
    const a = layouts[fromLayout][id], b = layouts[toLayout][id];
    return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
  };
  const positionedNodes = nodes.map(n => ({ ...n, ...pos(n.id) }));

  const typeStyle = {
    world:     { fill: "var(--accent-trace)",     ring: "var(--accent-trace)",     glyphFn: (n) => <WorldGlyph id={n.id} size={20} color="var(--accent-trace)"/> },
    motif:     { fill: "var(--accent-motif)",     ring: "var(--accent-motif)" },
    campaign:  { fill: "var(--status-exploratory)", ring: "var(--status-exploratory)" },
    agent:     { fill: "var(--fg-1)",             ring: "var(--fg-2)" },
    doctrine:  { fill: "var(--status-verified)",  ring: "var(--status-verified)" },
    falsifier: { fill: "var(--status-falsified)", ring: "var(--status-falsified)" },
    report:    { fill: "var(--fg-3)",             ring: "var(--fg-3)" },
  };
  const edgeColor = {
    "produced":     "var(--accent-trace)",
    "audited":      "var(--status-verified)",
    "falsified":    "var(--status-falsified)",
    "depends-on":   "var(--status-exploratory)",
    "detected-in":  "var(--accent-motif)",
  };
  const statusGlow = (status) => {
    const map = {
      verified: "rgba(82,224,162,0.5)", active: "rgba(0,209,255,0.6)",
      warning: "rgba(255,184,0,0.5)", exploratory: "rgba(255,184,0,0.5)",
      failed: "rgba(255,92,122,0.6)",
    };
    return map[status] || "rgba(120,138,168,0.3)";
  };

  return (
    <div style={{ position: "relative", flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", background: "var(--bg-base)" }}>
      {/* starfield bg */}
      <div style={{ position: "absolute", inset: 0,
        background: "radial-gradient(ellipse at 30% 20%, rgba(0,209,255,0.04), transparent 50%)," +
                    "radial-gradient(ellipse at 80% 70%, rgba(176,132,255,0.04), transparent 50%)," +
                    "radial-gradient(ellipse at 50% 100%, rgba(255,92,122,0.03), transparent 40%)",
        pointerEvents: "none",
      }}/>

      {/* Layout mode toggle — top center */}
      <div style={{
        position: "absolute", top: 16, left: "50%", transform: "translateX(-50%)", zIndex: 3,
        display: "flex", alignItems: "center", gap: 4,
        background: "var(--surface-2)", border: "1px solid var(--border-2)",
        borderRadius: 999, padding: 3,
        boxShadow: "var(--shadow-card-md)",
      }}>
        {[
          { id: "curated",       label: "Curated"       },
          { id: "constellation", label: "Constellation" },
          { id: "radial",        label: "Radial"        },
        ].map(opt => (
          <button key={opt.id} onClick={() => switchLayout(opt.id)} style={{
            padding: "6px 12px", borderRadius: 999, border: "none", cursor: "pointer",
            background: toLayout === opt.id ? "var(--accent-trace)" : "transparent",
            color: toLayout === opt.id ? "var(--bg-base)" : "var(--fg-2)",
            font: "500 10px/1 var(--font-mono)", letterSpacing: 0.6, textTransform: "uppercase",
            transition: "background 160ms, color 160ms",
          }}>{opt.label}</button>
        ))}
      </div>

      {/* Filter rails */}
      <div style={{ position: "absolute", top: 16, left: 16, right: 16, display: "flex", justifyContent: "space-between", gap: 12, zIndex: 2 }}>
        <FilterPanel title="node types" items={[
          { id: "world",     label: "Worlds",     color: "var(--accent-trace)"     },
          { id: "campaign",  label: "Campaigns",  color: "var(--status-exploratory)" },
          { id: "motif",     label: "Motifs",     color: "var(--accent-motif)"     },
          { id: "agent",     label: "Agents",     color: "var(--fg-1)"             },
          { id: "doctrine",  label: "Doctrine",   color: "var(--status-verified)"  },
          { id: "falsifier", label: "Falsifiers", color: "var(--status-falsified)" },
          { id: "report",    label: "Reports",    color: "var(--fg-3)"             },
        ]} state={filter} setState={setFilter}/>
        <FilterPanel title="edges" items={[
          { id: "produced",     label: "produced",     color: edgeColor.produced     },
          { id: "audited",      label: "audited",      color: edgeColor.audited      },
          { id: "falsified",    label: "falsified",    color: edgeColor.falsified    },
          { id: "depends-on",   label: "depends-on",   color: edgeColor["depends-on"]},
          { id: "detected-in",  label: "detected-in",  color: edgeColor["detected-in"]},
        ]} state={edgeFilter} setState={setEdgeFilter}/>
      </div>

      {/* Graph */}
      <svg viewBox="0 0 900 680" style={{ width: "100%", height: "100%", position: "relative", zIndex: 1 }}>
        <defs>
          <radialGradient id="bg-glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="rgba(0,209,255,0.04)"/>
            <stop offset="100%" stopColor="transparent"/>
          </radialGradient>
        </defs>

        {edges.filter(([a, b, et]) => edgeFilter[et]
            && filter[positionedNodes.find(n => n.id === a).type]
            && filter[positionedNodes.find(n => n.id === b).type]).map(([a, b, et], i) => {
          const A = positionedNodes.find(n => n.id === a), B = positionedNodes.find(n => n.id === b);
          return (
            <g key={i}>
              <path d={`M${A.x} ${A.y} Q ${(A.x+B.x)/2} ${(A.y+B.y)/2 - 20} ${B.x} ${B.y}`}
                fill="none" stroke={edgeColor[et]} strokeWidth={et === "falsified" ? 1.4 : 0.9}
                opacity={et === "falsified" ? 0.85 : 0.5}
                strokeDasharray={et === "depends-on" ? "3 3" : "0"}
                style={{ filter: et === "falsified" ? `drop-shadow(0 0 4px ${edgeColor[et]})` : "none" }}/>
            </g>
          );
        })}

        {positionedNodes.filter(n => filter[n.type]).map(n => {
          const ts = typeStyle[n.type];
          const r = n.type === "agent" ? 22 : n.type === "campaign" ? 16 : n.type === "world" ? 18 : 13;
          return (
            <g key={n.id} style={{ cursor: "pointer" }} onMouseEnter={() => setHover(n)} onMouseLeave={() => setHover(null)}>
              <circle cx={n.x} cy={n.y} r={r * 1.6} fill={statusGlow(n.status)} opacity="0.4" filter="blur(6px)"/>
              <circle cx={n.x} cy={n.y} r={r} fill={ts.fill} fillOpacity="0.12" stroke={ts.ring} strokeWidth="1.4"/>
              <circle cx={n.x} cy={n.y} r={r * 0.35} fill={ts.ring} opacity="0.8"/>
              {n.status === "failed" && (
                <g stroke={ts.ring} strokeWidth="1.5" strokeLinecap="round" opacity="0.9">
                  <line x1={n.x - r * 0.55} y1={n.y - r * 0.55} x2={n.x + r * 0.55} y2={n.y + r * 0.55}/>
                  <line x1={n.x + r * 0.55} y1={n.y - r * 0.55} x2={n.x - r * 0.55} y2={n.y + r * 0.55}/>
                </g>
              )}
              {n.status === "active" && (
                <circle cx={n.x} cy={n.y} r={r * 1.2} fill="none" stroke={ts.ring} strokeWidth="1" opacity="0.6">
                  <animate attributeName="r" from={r} to={r * 1.6} dur="2s" repeatCount="indefinite"/>
                  <animate attributeName="opacity" from="0.7" to="0" dur="2s" repeatCount="indefinite"/>
                </circle>
              )}
              <text x={n.x} y={n.y + r + 14} textAnchor="middle"
                style={{ font: "500 9.5px var(--font-mono)", fill: "var(--fg-2)", letterSpacing: 0.3 }}>
                {n.label || n.id}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Minimap */}
      <div style={{
        position: "absolute", bottom: 16, right: 16, zIndex: 2,
        width: 160, height: 110,
        background: "var(--surface-1)", border: "1px solid var(--border-1)",
        borderRadius: "var(--radius-sm)", padding: 6, opacity: 0.85,
      }}>
        <svg viewBox="0 0 900 680" style={{ width: "100%", height: "100%" }}>
          {positionedNodes.map(n => <circle key={n.id} cx={n.x} cy={n.y} r="14" fill={typeStyle[n.type].ring} opacity="0.6"/>)}
          <rect x="0" y="0" width="900" height="680" fill="none" stroke="var(--accent-trace)" strokeWidth="6"/>
        </svg>
      </div>

      {/* Hover detail */}
      {hover && (
        <div style={{
          position: "absolute", bottom: 16, left: 16, zIndex: 2,
          background: "var(--surface-2)", border: "1px solid var(--border-2)",
          borderRadius: "var(--radius-md)", padding: 14,
          minWidth: 240, boxShadow: "var(--shadow-card-lg)",
        }}>
          <div style={{ font: "500 9px/1 var(--font-mono)", letterSpacing: 1.4, color: "var(--fg-3)", textTransform: "uppercase", marginBottom: 6 }}>{hover.type}</div>
          <div style={{ font: "500 14px/1 var(--font-display)", color: "var(--fg-1)", marginBottom: 8 }}>{hover.label || hover.id}</div>
          <Pill status={hover.status} size="sm">{hover.status}</Pill>
        </div>
      )}
    </div>
  );
};

const FilterPanel = ({ title, items, state, setState }) => (
  <div style={{
    background: "var(--surface-1)", border: "1px solid var(--border-1)",
    borderRadius: "var(--radius-md)", padding: 10, display: "flex", flexDirection: "column", gap: 6,
  }}>
    <div style={{ font: "500 9px/1 var(--font-mono)", color: "var(--fg-3)", letterSpacing: 1.2, textTransform: "uppercase", marginBottom: 4 }}>{title}</div>
    <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
      {items.map(it => (
        <button key={it.id} onClick={() => setState({ ...state, [it.id]: !state[it.id] })} style={{
          display: "flex", alignItems: "center", gap: 6,
          padding: "4px 8px", borderRadius: 999,
          background: state[it.id] ? "rgba(255,255,255,0.04)" : "transparent",
          border: `1px solid ${state[it.id] ? "var(--border-2)" : "var(--border-1)"}`,
          opacity: state[it.id] ? 1 : 0.4, cursor: "pointer",
          font: "500 10px/1 var(--font-mono)", color: "var(--fg-2)", letterSpacing: 0.4,
        }}>
          <span style={{ width: 6, height: 6, borderRadius: "50%", background: it.color }}/>
          {it.label}
        </button>
      ))}
    </div>
  </div>
);

window.ProjectGraph = ProjectGraph;
