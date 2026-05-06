// Agent identity system. Glyphs + colors + treatment for the five
// recognized agents on the project. Status colors stay separate.
//
//   Builder    — amber/gold      — execution / forge        (wrench-arc)
//   Codex      — electric cyan   — senior code audit        (scalpel-checksum)
//   Architect  — violet          — systems blueprint        (compass-lattice)
//   GPT        — silver-blue     — synthesis / theory       (prism-orbit)
//   Human PI   — white-gold      — arbitration / command    (decision seal)

const AGENTS = {
  builder:   { id: "builder",   label: "Claude Builder",   short: "CB",  color: "var(--agent-builder)",   soft: "var(--agent-builder-soft)",   glow: "var(--agent-builder-glow)",   role: "execution" },
  codex:     { id: "codex",     label: "Codex",            short: "CX",  color: "var(--agent-codex)",     soft: "var(--agent-codex-soft)",     glow: "var(--agent-codex-glow)",     role: "audit" },
  architect: { id: "architect", label: "Claude Architect", short: "CA",  color: "var(--agent-architect)", soft: "var(--agent-architect-soft)", glow: "var(--agent-architect-glow)", role: "blueprint" },
  gpt:       { id: "gpt",       label: "GPT Reviewer",     short: "GR",  color: "var(--agent-gpt)",       soft: "var(--agent-gpt-soft)",       glow: "var(--agent-gpt-glow)",       role: "synthesis" },
  human:     { id: "human",     label: "Human PI · Xy",    short: "Xy",  color: "var(--agent-human)",     soft: "var(--agent-human-soft)",     glow: "var(--agent-human-glow)",     role: "arbitration" },
};
window.AGENTS = AGENTS;

// Each glyph is a 24×24 viewBox, stroked in currentColor. Style the wrapper.
const AgentGlyph = ({ agent, size = 18, style = {} }) => {
  const a = AGENTS[agent];
  if (!a) return null;
  const sw = 1.6;
  const glyphs = {
    // Builder — wrench-arc with forge spark. Construction-line motif.
    builder: (
      <g fill="none" stroke="currentColor" strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round">
        <path d="M5 19 L11 13"/>
        <path d="M14 4 a4.5 4.5 0 0 0 -4 6 L4 16 l4 4 6 -6 a4.5 4.5 0 0 0 6 -4 l-3 3 -3 -3 z"/>
        <circle cx="5.5" cy="18.5" r="0.9" fill="currentColor"/>
      </g>
    ),
    // Codex — scalpel + checksum tick. Sharp, precise.
    codex: (
      <g fill="none" stroke="currentColor" strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 20 L14 10 L17 13 L7 23"/>
        <path d="M14 10 L18 6 L20 8 L17 13"/>
        <path d="M14 18 l2 2 l4 -5" opacity="0.85"/>
      </g>
    ),
    // Architect — compass + lattice frame. Blueprint geometry.
    architect: (
      <g fill="none" stroke="currentColor" strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="9" r="2"/>
        <path d="M12 11 L6 21"/>
        <path d="M12 11 L18 21"/>
        <path d="M8 17 L16 17" opacity="0.7"/>
        <path d="M12 3 L12 7" opacity="0.7"/>
      </g>
    ),
    // GPT — prism + orbit. Synthesis / refraction.
    gpt: (
      <g fill="none" stroke="currentColor" strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 4 L20 18 L4 18 Z"/>
        <ellipse cx="12" cy="14" rx="9" ry="3" opacity="0.55"/>
        <circle cx="12" cy="11" r="0.9" fill="currentColor"/>
      </g>
    ),
    // Human PI — decision seal / arbitration star.
    human: (
      <g fill="none" stroke="currentColor" strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="7"/>
        <path d="M12 5 L12 19 M5 12 L19 12 M7 7 L17 17 M17 7 L7 17" opacity="0.55"/>
        <circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/>
      </g>
    ),
  };
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" style={{ color: a.color, flexShrink: 0, ...style }}>
      {glyphs[agent]}
    </svg>
  );
};

// Identity chip — small inline tag used in feeds, audits, task cards.
// Variants: "chip" (default, soft fill), "outline", "solid".
const AgentChip = ({ agent, variant = "chip", showLabel = true, size = 11, style = {} }) => {
  const a = AGENTS[agent];
  if (!a) return null;
  const bg     = variant === "solid"   ? a.color
              : variant === "outline" ? "transparent"
              : a.soft;
  const fg     = variant === "solid"   ? "#0a0e16"
              : a.color;
  const border = variant === "outline" ? `1px solid ${a.color}`
              : variant === "solid"    ? "none"
              : `1px solid ${a.color}`;
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 6,
      padding: "3px 8px 3px 6px",
      background: bg, border,
      borderRadius: 999,
      font: `500 ${size}px/1 var(--font-mono)`,
      letterSpacing: 0.4,
      color: fg,
      whiteSpace: "nowrap",
      ...style,
    }}>
      <AgentGlyph agent={agent} size={size + 3}/>
      {showLabel && <span>{a.short}</span>}
    </span>
  );
};

// Avatar — circular identity badge. Used in agent cards, AI Ops Tower.
const AgentAvatar = ({ agent, size = 36, glow = false, style = {} }) => {
  const a = AGENTS[agent];
  if (!a) return null;
  return (
    <div style={{
      width: size, height: size, borderRadius: "50%",
      background: a.soft,
      border: `1px solid ${a.color}`,
      display: "flex", alignItems: "center", justifyContent: "center",
      boxShadow: glow ? a.glow : "none",
      flexShrink: 0,
      ...style,
    }}>
      <AgentGlyph agent={agent} size={Math.round(size * 0.55)}/>
    </div>
  );
};

window.AgentGlyph = AgentGlyph;
window.AgentChip = AgentChip;
window.AgentAvatar = AgentAvatar;
