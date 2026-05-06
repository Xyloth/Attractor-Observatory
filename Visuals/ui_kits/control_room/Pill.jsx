// Status pill — the canonical status chip. Single source of truth.
const Pill = ({ status = "verified", children, mono = false, dot = true, size = "md" }) => {
  const tones = {
    verified:    { bg: "rgba(82, 224, 162, 0.10)", fg: "var(--status-verified)",    bd: "rgba(82,224,162,0.30)" },
    active:      { bg: "rgba(0, 209, 255, 0.10)",  fg: "var(--status-active)",      bd: "rgba(0,209,255,0.30)" },
    exploratory: { bg: "rgba(255, 184, 0, 0.10)",  fg: "var(--status-exploratory)", bd: "rgba(255,184,0,0.30)" },
    candidate:   { bg: "rgba(255, 184, 0, 0.10)",  fg: "var(--status-exploratory)", bd: "rgba(255,184,0,0.30)" },
    warning:     { bg: "rgba(255, 184, 0, 0.10)",  fg: "var(--status-exploratory)", bd: "rgba(255,184,0,0.30)" },
    missing:     { bg: "rgba(120, 138, 168, 0.10)",fg: "var(--status-missing)",     bd: "rgba(120,138,168,0.25)" },
    falsified:   { bg: "rgba(255, 92, 122, 0.10)", fg: "var(--status-falsified)",   bd: "rgba(255,92,122,0.30)" },
    failed:      { bg: "rgba(255, 92, 122, 0.10)", fg: "var(--status-falsified)",   bd: "rgba(255,92,122,0.30)" },
  };
  const t = tones[status] || tones.missing;
  const sizes = {
    sm: { pad: "1px 7px", fs: 10, gap: 5, dot: 5 },
    md: { pad: "3px 10px", fs: 11, gap: 6, dot: 6 },
    lg: { pad: "5px 14px", fs: 13, gap: 8, dot: 7 },
  }[size];
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: sizes.gap,
      padding: sizes.pad, borderRadius: 999,
      background: t.bg, border: `1px solid ${t.bd}`, color: t.fg,
      fontFamily: mono ? "var(--font-mono)" : "var(--font-ui)",
      fontSize: sizes.fs, fontWeight: 500, letterSpacing: 0.4,
      textTransform: "uppercase", whiteSpace: "nowrap",
    }}>
      {dot && <span style={{
        width: sizes.dot, height: sizes.dot, borderRadius: "50%", background: t.fg,
        boxShadow: `0 0 6px ${t.fg}`,
      }} />}
      {children}
    </span>
  );
};

window.Pill = Pill;
