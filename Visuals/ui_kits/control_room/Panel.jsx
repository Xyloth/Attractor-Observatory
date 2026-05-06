// Panel — surface card primitive. Variants: surface (default), raised, sunken, quarantine.
const Panel = ({ variant = "surface", title, eyebrow, action, children, style = {}, padded = true, glow = null }) => {
  const variants = {
    surface:    { bg: "var(--surface-1)", bd: "var(--border-1)" },
    raised:     { bg: "var(--surface-2)", bd: "var(--border-2)" },
    sunken:     { bg: "var(--bg-base)",   bd: "var(--border-1)" },
    quarantine: { bg: "rgba(255, 184, 0, 0.04)", bd: "rgba(255, 184, 0, 0.40)", dashed: true },
    danger:     { bg: "rgba(255, 92, 122, 0.04)", bd: "rgba(255, 92, 122, 0.35)" },
  }[variant] || { bg: "var(--surface-1)", bd: "var(--border-1)" };
  const glows = {
    verified: "0 0 0 1px rgba(82,224,162,0.18), 0 0 32px -8px rgba(82,224,162,0.25)",
    active:   "0 0 0 1px rgba(0,209,255,0.18),  0 0 32px -8px rgba(0,209,255,0.25)",
    falsified:"0 0 0 1px rgba(255,92,122,0.18), 0 0 32px -8px rgba(255,92,122,0.25)",
  };
  return (
    <div style={{
      background: variants.bg,
      border: `1px ${variants.dashed ? "dashed" : "solid"} ${variants.bd}`,
      borderRadius: "var(--radius-lg)",
      boxShadow: glow ? glows[glow] : "var(--shadow-card)",
      ...style,
    }}>
      {(title || eyebrow || action) && (
        <div style={{
          display: "flex", alignItems: "center", justifyContent: "space-between",
          padding: "12px 16px", borderBottom: `1px solid ${variants.bd}`,
        }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
            {eyebrow && <div style={{
              font: "500 10px/1 var(--font-mono)", letterSpacing: 1.2,
              color: "var(--fg-3)", textTransform: "uppercase",
            }}>{eyebrow}</div>}
            {title && <div style={{
              font: "500 13px/1.2 var(--font-ui)", color: "var(--fg-1)", letterSpacing: 0.2,
            }}>{title}</div>}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      <div style={{ padding: padded ? 16 : 0 }}>{children}</div>
    </div>
  );
};

window.Panel = Panel;
