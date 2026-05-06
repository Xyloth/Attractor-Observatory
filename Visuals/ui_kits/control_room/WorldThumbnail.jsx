// WorldThumbnail — richer atmospheric art for World Observatory cards,
// chamber detail pages, and portfolio screenshots. The canonical glyph
// (see WorldGlyph.jsx) stays the system identity; this layer is for
// visual impact in larger surfaces. Consumers pass `size` (square px).
//
// All thumbnails:
//   - draw on a dark obsidian background with the world's hue accent
//   - use only the world's hue + soft cyan/purple highlights
//   - include faint grid/noise treatment so they read as observatory art
//   - degrade legibly to small sizes (the artwork scales by viewBox)

const WorldThumbnail = ({ id, size = 120, style = {} }) => {
  const w = (window.MOCK?.worlds || []).find(x => x.id === id);
  const hue = w ? `var(${w.hue})` : "var(--accent-trace)";
  const art = ART[id];
  return (
    <div style={{
      width: size, height: size, position: "relative", overflow: "hidden",
      borderRadius: "var(--radius-md)",
      background: `radial-gradient(circle at 30% 25%, ${hue}22, transparent 60%), var(--bg-deepest)`,
      border: `1px solid ${hue}33`,
      ...style,
    }}>
      {/* faint observatory grid */}
      <svg viewBox="0 0 120 120" width="100%" height="100%" style={{ position: "absolute", inset: 0, opacity: 0.18 }}>
        <defs>
          <pattern id={`gr-${id}`} width="12" height="12" patternUnits="userSpaceOnUse">
            <path d="M12 0 L0 0 L0 12" fill="none" stroke="var(--border-2)" strokeWidth="0.4"/>
          </pattern>
        </defs>
        <rect width="120" height="120" fill={`url(#gr-${id})`}/>
      </svg>
      {/* world art */}
      <svg viewBox="0 0 120 120" width="100%" height="100%" style={{ position: "absolute", inset: 0 }}>
        {art && art(hue)}
      </svg>
      {/* subtle starfield */}
      <svg viewBox="0 0 120 120" width="100%" height="100%" style={{ position: "absolute", inset: 0, mixBlendMode: "screen" }}>
        {[[12,18,0.4],[88,22,0.35],[103,82,0.45],[28,98,0.3],[64,12,0.25],[96,55,0.3]].map(([x,y,o],i) => (
          <circle key={i} cx={x} cy={y} r="0.7" fill="white" opacity={o}/>
        ))}
      </svg>
    </div>
  );
};

// Each entry returns SVG children for a 120×120 viewBox. Hue is the
// world's accent color string. Keep stroke widths > 0.6 so they survive
// at thumb size (~80px).
const ART = {
  // W1 CRN — molecular constellation / reaction web
  W1: (h) => (<>
    <g fill="none" stroke={h} strokeWidth="0.8" opacity="0.7">
      <line x1="32" y1="48" x2="60" y2="36"/>
      <line x1="60" y1="36" x2="84" y2="52"/>
      <line x1="32" y1="48" x2="48" y2="78"/>
      <line x1="84" y1="52" x2="78" y2="86"/>
      <line x1="48" y1="78" x2="78" y2="86"/>
      <line x1="60" y1="36" x2="60" y2="64"/>
      <line x1="60" y1="64" x2="48" y2="78"/>
      <line x1="60" y1="64" x2="78" y2="86"/>
    </g>
    {[[32,48,3],[60,36,3.5],[84,52,3],[48,78,3],[78,86,3],[60,64,4]].map(([x,y,r],i) => (
      <g key={i}>
        <circle cx={x} cy={y} r={r+1.5} fill={h} opacity="0.18"/>
        <circle cx={x} cy={y} r={r} fill={h}/>
      </g>
    ))}
  </>),

  // W2 Protocell — luminous membrane vesicles
  W2: (h) => (<>
    <defs>
      <radialGradient id="v2-1"><stop offset="0%" stopColor={h} stopOpacity="0.35"/><stop offset="70%" stopColor={h} stopOpacity="0.04"/><stop offset="100%" stopOpacity="0"/></radialGradient>
    </defs>
    <ellipse cx="48" cy="58" rx="28" ry="22" fill="url(#v2-1)"/>
    <ellipse cx="48" cy="58" rx="28" ry="22" fill="none" stroke={h} strokeWidth="1.0"/>
    <ellipse cx="46" cy="56" rx="22" ry="17" fill="none" stroke={h} strokeWidth="0.5" opacity="0.5"/>
    <ellipse cx="84" cy="80" rx="14" ry="11" fill="url(#v2-1)"/>
    <ellipse cx="84" cy="80" rx="14" ry="11" fill="none" stroke={h} strokeWidth="0.8"/>
    <circle cx="50" cy="56" r="2" fill={h} opacity="0.6"/>
    <circle cx="42" cy="64" r="1.4" fill={h} opacity="0.4"/>
    <circle cx="82" cy="80" r="1.4" fill={h} opacity="0.6"/>
  </>),

  // W3 Field — wave / interference field
  W3: (h) => (<>
    <g fill="none" stroke={h} strokeWidth="0.6" opacity="0.55">
      {Array.from({length: 8}, (_, i) => 14 + i * 12).map((r, i) => (
        <circle key={i} cx="40" cy="60" r={r} opacity={0.7 - i*0.07}/>
      ))}
      {Array.from({length: 8}, (_, i) => 14 + i * 12).map((r, i) => (
        <circle key={`b${i}`} cx="86" cy="62" r={r} opacity={0.7 - i*0.07}/>
      ))}
    </g>
    <circle cx="40" cy="60" r="2.5" fill={h}/>
    <circle cx="86" cy="62" r="2.5" fill={h}/>
  </>),

  // W4 Morphogenesis — branching embryo / dendrite
  W4: (h) => (<>
    <g fill="none" stroke={h} strokeWidth="1" strokeLinecap="round">
      <path d="M60 100 L60 70"/>
      <path d="M60 70 Q50 55 38 48"/>
      <path d="M60 70 Q70 55 82 48"/>
      <path d="M38 48 Q30 42 24 32"/>
      <path d="M38 48 Q42 38 36 26"/>
      <path d="M82 48 Q90 42 96 32"/>
      <path d="M82 48 Q78 38 84 26"/>
      <path d="M60 70 Q60 55 60 36"/>
    </g>
    {[[24,32],[36,26],[60,36],[84,26],[96,32]].map(([x,y],i) => (
      <circle key={i} cx={x} cy={y} r="2.2" fill={h}/>
    ))}
    <circle cx="60" cy="100" r="3" fill={h} opacity="0.4"/>
  </>),

  // W5 Digital — circuit organism
  W5: (h) => (<>
    <g fill="none" stroke={h} strokeWidth="0.8">
      <path d="M20 30 L40 30 L40 50 L60 50 L60 30 L80 30 L80 70 L60 70 L60 90 L40 90 L40 70 L20 70 Z" opacity="0.6"/>
      <path d="M80 30 L100 30 L100 90 L80 90" opacity="0.6"/>
      <line x1="40" y1="50" x2="20" y2="50" opacity="0.5"/>
      <line x1="80" y1="50" x2="100" y2="50" opacity="0.5"/>
    </g>
    {[[20,30],[40,30],[60,30],[80,30],[100,30],[20,50],[40,50],[60,50],[80,50],[100,50],[20,70],[40,70],[60,70],[80,70],[100,70],[40,90],[60,90],[80,90],[100,90]].map(([x,y],i) => (
      <circle key={i} cx={x} cy={y} r="1.4" fill={h} opacity="0.85"/>
    ))}
  </>),

  // W6 Ecosystem — layered terrain / food web
  W6: (h) => (<>
    <g fill="none" stroke={h} strokeWidth="0.7">
      <path d="M0 90 Q30 78 60 84 T120 80" opacity="0.7"/>
      <path d="M0 72 Q25 64 60 68 T120 64" opacity="0.5"/>
      <path d="M0 54 Q35 48 60 52 T120 50" opacity="0.4"/>
      <path d="M0 36 Q40 30 60 34 T120 32" opacity="0.3"/>
    </g>
    <g stroke={h} strokeWidth="0.5" opacity="0.55">
      <line x1="22" y1="52" x2="32" y2="68"/><line x1="32" y1="68" x2="50" y2="82"/>
      <line x1="60" y1="50" x2="70" y2="68"/><line x1="70" y1="68" x2="84" y2="82"/>
      <line x1="92" y1="50" x2="100" y2="64"/>
    </g>
    {[[22,52],[32,68],[50,82],[60,50],[70,68],[84,82],[92,50],[100,64]].map(([x,y],i) => (
      <circle key={i} cx={x} cy={y} r="1.6" fill={h}/>
    ))}
  </>),

  // W7 Swarm — luminous swarm trail over terrain
  W7: (h) => (<>
    <path d="M0 92 Q30 84 60 90 T120 86" fill="none" stroke="var(--border-2)" strokeWidth="0.6" opacity="0.6"/>
    <g fill={h}>
      {[[10,84,0.4],[18,76,0.5],[28,68,0.55],[36,58,0.6],[44,46,0.7],[52,40,0.85],[58,32,1.0],[68,30,0.9],[76,36,0.8],[82,46,0.7],[88,58,0.6],[92,72,0.5],[98,82,0.4]].map(([x,y,o],i) => (
        <circle key={i} cx={x} cy={y} r="1.4" opacity={o}/>
      ))}
      {[[14,92],[28,90],[44,90],[58,92],[74,90],[90,92]].map(([x,y],i) => (
        <circle key={`s${i}`} cx={x} cy={y} r="0.9" opacity="0.5"/>
      ))}
    </g>
    <path d="M10 84 Q30 60 58 32 Q86 50 98 82" fill="none" stroke={h} strokeWidth="0.5" opacity="0.45" strokeDasharray="1 2"/>
  </>),

  // W8 Cognitive — neural loop / control field
  W8: (h) => (<>
    <ellipse cx="60" cy="60" rx="40" ry="18" fill="none" stroke={h} strokeWidth="0.8" opacity="0.55"/>
    <ellipse cx="60" cy="60" rx="40" ry="18" fill="none" stroke={h} strokeWidth="0.5" opacity="0.4" transform="rotate(60 60 60)"/>
    <ellipse cx="60" cy="60" rx="40" ry="18" fill="none" stroke={h} strokeWidth="0.5" opacity="0.4" transform="rotate(-60 60 60)"/>
    {[[24,60],[60,42],[96,60],[60,78],[42,46],[78,46],[42,74],[78,74]].map(([x,y],i) => (
      <g key={i}>
        <circle cx={x} cy={y} r="3" fill={h} opacity="0.18"/>
        <circle cx={x} cy={y} r="1.6" fill={h}/>
      </g>
    ))}
    <circle cx="60" cy="60" r="3" fill={h}/>
    <g stroke={h} strokeWidth="0.5" opacity="0.5">
      <line x1="24" y1="60" x2="60" y2="60"/><line x1="60" y1="60" x2="96" y2="60"/>
      <line x1="60" y1="42" x2="60" y2="78"/>
    </g>
  </>),

  // W9 Origins-mineral — crystal surface / pore network
  W9: (h) => (<>
    <g fill="none" stroke={h} strokeWidth="0.7" opacity="0.7">
      <path d="M30 90 L30 50 L60 30 L90 50 L90 90 Z"/>
      <path d="M30 50 L60 70 L90 50"/>
      <path d="M60 30 L60 70 L60 90"/>
      <path d="M30 90 L60 70 L90 90"/>
      <path d="M44 60 L44 80 L60 90"/>
      <path d="M76 60 L76 80 L60 90"/>
    </g>
    {[[44,60],[76,60],[60,30],[30,50],[90,50],[60,70]].map(([x,y],i) => (
      <circle key={i} cx={x} cy={y} r="1.8" fill={h} opacity="0.7"/>
    ))}
  </>),

  // W10 Hypergraph — high-order reaction nodes
  W10: (h) => (<>
    <g fill="none" stroke={h} strokeWidth="0.6" opacity="0.55">
      <path d="M30 30 Q60 20 90 32 Q92 60 88 88 Q60 96 32 88 Q24 60 30 30 Z"/>
      <path d="M40 40 Q60 36 80 44 Q82 60 78 76 Q60 80 42 76 Q38 60 40 40 Z"/>
    </g>
    {[[30,30],[60,24],[90,32],[88,60],[88,88],[60,92],[32,88],[28,60]].map(([x,y],i) => (
      <circle key={i} cx={x} cy={y} r="2" fill={h}/>
    ))}
    <circle cx="60" cy="58" r="2.5" fill={h}/>
    <g stroke={h} strokeWidth="0.4" opacity="0.5">
      <line x1="60" y1="58" x2="30" y2="30"/><line x1="60" y1="58" x2="90" y2="32"/>
      <line x1="60" y1="58" x2="88" y2="88"/><line x1="60" y1="58" x2="32" y2="88"/>
    </g>
  </>),

  // W11 Quasispecies — sequence cloud
  W11: (h) => (<>
    {Array.from({length: 60}, (_, i) => {
      const a = (i * 137.5) * Math.PI / 180;
      const r = 6 + Math.sqrt(i) * 5;
      const x = 60 + Math.cos(a) * r;
      const y = 60 + Math.sin(a) * r;
      return <circle key={i} cx={x} cy={y} r={1.2} fill={h} opacity={0.85 - i*0.012}/>;
    })}
    <circle cx="60" cy="60" r="3" fill={h}/>
  </>),

  // W12 Symbiogenesis — nested cells (cell within cell)
  W12: (h) => (<>
    <ellipse cx="60" cy="60" rx="42" ry="34" fill="none" stroke={h} strokeWidth="0.9" opacity="0.7"/>
    <ellipse cx="56" cy="58" rx="22" ry="18" fill="none" stroke={h} strokeWidth="0.7" opacity="0.7"/>
    <ellipse cx="76" cy="68" rx="10" ry="8" fill="none" stroke={h} strokeWidth="0.6" opacity="0.6"/>
    <circle cx="56" cy="58" r="2.5" fill={h} opacity="0.7"/>
    <circle cx="76" cy="68" r="1.8" fill={h} opacity="0.7"/>
    <circle cx="50" cy="62" r="1.2" fill={h} opacity="0.5"/>
    <circle cx="62" cy="54" r="1.0" fill={h} opacity="0.5"/>
  </>),

  // W13 Multiscale — recursive nested rings
  W13: (h) => (<>
    {[6, 14, 24, 36, 48].map((r, i) => (
      <circle key={i} cx="60" cy="60" r={r} fill="none" stroke={h} strokeWidth="0.8" opacity={0.85 - i*0.13}/>
    ))}
    <circle cx="60" cy="60" r="2.5" fill={h}/>
    {/* tick marks suggesting scale */}
    {[0,72,144,216,288].map(deg => {
      const rad = deg * Math.PI/180;
      const x1 = 60 + Math.cos(rad)*52, y1 = 60 + Math.sin(rad)*52;
      const x2 = 60 + Math.cos(rad)*58, y2 = 60 + Math.sin(rad)*58;
      return <line key={deg} x1={x1} y1={y1} x2={x2} y2={y2} stroke={h} strokeWidth="0.7" opacity="0.6"/>;
    })}
  </>),
};

window.WorldThumbnail = WorldThumbnail;
