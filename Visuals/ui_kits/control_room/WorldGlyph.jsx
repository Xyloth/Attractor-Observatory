// World family emblems — W1–W13. Each is a small SVG glyph following the
// brief's visual concepts (molecular constellation, membrane vesicle, wave
// field, branching embryo, circuit organism, food-web terrain, swarm trail,
// neural loop, crystal pore network, hyperedge node, sequence cloud,
// nested cells, recursive nested rings).
const WorldGlyph = ({ id, size = 36, color = "currentColor" }) => {
  const s = { width: size, height: size, fill: "none", stroke: color, strokeWidth: 1.25, strokeLinecap: "round", strokeLinejoin: "round" };
  const fillS = { ...s, fill: color, fillOpacity: 0.15 };
  const glyphs = {
    W1: ( // chemistry — molecule web
      <svg viewBox="0 0 36 36" {...s}>
        <circle cx="10" cy="12" r="2.5"/><circle cx="22" cy="9" r="2"/><circle cx="26" cy="20" r="2.5"/>
        <circle cx="14" cy="24" r="2"/><circle cx="20" cy="28" r="1.5"/>
        <path d="M12 13l8-3M23 11l3 7M24 22l-9 2M16 25l3 2M11 14l3 8"/>
      </svg>
    ),
    W2: ( // protocell — membrane vesicle
      <svg viewBox="0 0 36 36" {...s}>
        <circle cx="18" cy="18" r="11"/>
        <circle cx="18" cy="18" r="7" strokeDasharray="2 2" opacity=".7"/>
        <circle cx="18" cy="18" r="2" fill={color} fillOpacity="0.4" stroke="none"/>
      </svg>
    ),
    W3: ( // field — wave field
      <svg viewBox="0 0 36 36" {...s}>
        <path d="M3 10c4-3 8-3 12 0s8 3 12 0 6-3 6-3"/>
        <path d="M3 18c4-3 8-3 12 0s8 3 12 0 6-3 6-3" opacity=".7"/>
        <path d="M3 26c4-3 8-3 12 0s8 3 12 0 6-3 6-3" opacity=".4"/>
      </svg>
    ),
    W4: ( // morphogenesis — branching
      <svg viewBox="0 0 36 36" {...s}>
        <path d="M18 32V18"/>
        <path d="M18 18 8 8M18 18l10-10"/>
        <path d="M8 8 4 4M8 8 4 12M28 8l4-4M28 8l4 4"/>
        <circle cx="4" cy="4" r="1.2" fill={color} stroke="none"/>
        <circle cx="4" cy="12" r="1.2" fill={color} stroke="none"/>
        <circle cx="32" cy="4" r="1.2" fill={color} stroke="none"/>
        <circle cx="32" cy="12" r="1.2" fill={color} stroke="none"/>
      </svg>
    ),
    W5: ( // digital — circuit organism
      <svg viewBox="0 0 36 36" {...s}>
        <rect x="14" y="14" width="8" height="8" rx="1"/>
        <path d="M18 14V6M18 22v8M14 18H6M22 18h8"/>
        <circle cx="6" cy="18" r="1.5"/><circle cx="30" cy="18" r="1.5"/>
        <circle cx="18" cy="6" r="1.5"/><circle cx="18" cy="30" r="1.5"/>
      </svg>
    ),
    W6: ( // ecosystem — food-web layers
      <svg viewBox="0 0 36 36" {...s}>
        <path d="M2 10h32M2 18h32M2 26h32" opacity=".4"/>
        <circle cx="8" cy="10" r="1.5" fill={color} stroke="none"/>
        <circle cx="20" cy="10" r="1.5" fill={color} stroke="none"/>
        <circle cx="14" cy="18" r="1.5" fill={color} stroke="none"/>
        <circle cx="26" cy="18" r="1.5" fill={color} stroke="none"/>
        <circle cx="10" cy="26" r="1.5" fill={color} stroke="none"/>
        <circle cx="22" cy="26" r="1.5" fill={color} stroke="none"/>
        <path d="M8 10l6 8M20 10l-6 8M20 10l6 8M14 18l-4 8M26 18l-4 8"/>
      </svg>
    ),
    W7: ( // swarm — agent trails
      <svg viewBox="0 0 36 36" {...s}>
        <path d="M4 22c4-2 7 2 11 0s7-6 12-4 5 4 5 4" opacity=".5"/>
        <circle cx="6" cy="22" r="1" fill={color} stroke="none"/>
        <circle cx="12" cy="20" r="1" fill={color} stroke="none"/>
        <circle cx="18" cy="22" r="1" fill={color} stroke="none"/>
        <circle cx="24" cy="18" r="1" fill={color} stroke="none"/>
        <circle cx="28" cy="20" r="1" fill={color} stroke="none"/>
        <circle cx="32" cy="22" r="1" fill={color} stroke="none"/>
        <circle cx="14" cy="14" r="1" fill={color} stroke="none"/>
        <circle cx="22" cy="12" r="1" fill={color} stroke="none"/>
      </svg>
    ),
    W8: ( // cognitive — neural loop
      <svg viewBox="0 0 36 36" {...s}>
        <circle cx="10" cy="14" r="2"/><circle cx="26" cy="14" r="2"/>
        <circle cx="18" cy="24" r="2"/>
        <path d="M12 14h12M11 16l6 7M25 16l-6 7"/>
        <path d="M10 11C6 11 4 8 6 5M26 11c4 0 6-3 4-6" opacity=".5"/>
      </svg>
    ),
    W9: ( // origins-mineral — pore network
      <svg viewBox="0 0 36 36" {...s}>
        <path d="M4 4h28v28H4z" opacity=".3"/>
        <circle cx="10" cy="10" r="2.5"/><circle cx="20" cy="8" r="1.8"/>
        <circle cx="26" cy="14" r="2"/><circle cx="14" cy="18" r="2"/>
        <circle cx="22" cy="22" r="2.5"/><circle cx="10" cy="26" r="1.8"/>
        <circle cx="28" cy="26" r="1.5"/>
      </svg>
    ),
    W10: ( // hypergraph — high-order node
      <svg viewBox="0 0 36 36" {...s}>
        <path d="M18 6 6 14l4 14h16l4-14z" opacity=".5"/>
        <circle cx="18" cy="6" r="1.5" fill={color} stroke="none"/>
        <circle cx="6" cy="14" r="1.5" fill={color} stroke="none"/>
        <circle cx="10" cy="28" r="1.5" fill={color} stroke="none"/>
        <circle cx="26" cy="28" r="1.5" fill={color} stroke="none"/>
        <circle cx="30" cy="14" r="1.5" fill={color} stroke="none"/>
        <circle cx="18" cy="18" r="2" fill={color} stroke="none"/>
        <path d="M18 6v12M6 14l12 4M30 14l-12 4M10 28l8-10M26 28l-8-10"/>
      </svg>
    ),
    W11: ( // quasispecies — sequence cloud
      <svg viewBox="0 0 36 36" {...s}>
        <circle cx="18" cy="18" r="3" fill={color} fillOpacity=".3" stroke="none"/>
        <circle cx="10" cy="14" r="1.2" fill={color} stroke="none"/>
        <circle cx="14" cy="8" r="1" fill={color} stroke="none"/>
        <circle cx="22" cy="9" r="1.2" fill={color} stroke="none"/>
        <circle cx="28" cy="14" r="1" fill={color} stroke="none"/>
        <circle cx="26" cy="22" r="1.2" fill={color} stroke="none"/>
        <circle cx="22" cy="28" r="1" fill={color} stroke="none"/>
        <circle cx="13" cy="26" r="1.2" fill={color} stroke="none"/>
        <circle cx="8" cy="22" r="1" fill={color} stroke="none"/>
      </svg>
    ),
    W12: ( // symbiogenesis — nested cells
      <svg viewBox="0 0 36 36" {...s}>
        <ellipse cx="18" cy="18" rx="13" ry="10"/>
        <ellipse cx="13" cy="18" rx="4" ry="3"/>
        <ellipse cx="22" cy="17" rx="3" ry="2.5"/>
        <circle cx="22" cy="22" r="1.5"/>
      </svg>
    ),
    W13: ( // multiscale — recursive nested rings
      <svg viewBox="0 0 36 36" {...s}>
        <circle cx="18" cy="18" r="14"/>
        <circle cx="18" cy="18" r="9" opacity=".7"/>
        <circle cx="18" cy="18" r="5" opacity=".5"/>
        <circle cx="18" cy="18" r="2" fill={color} stroke="none"/>
      </svg>
    ),
  };
  return glyphs[id] || null;
};
window.WorldGlyph = WorldGlyph;
