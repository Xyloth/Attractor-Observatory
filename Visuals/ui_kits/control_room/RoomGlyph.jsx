// Custom room glyphs — 24px, 1.5px stroke, currentColor. Per the brief:
// custom-ish, not generic icons.
const RoomGlyph = ({ id, size = 20, color = "currentColor" }) => {
  const s = { width: size, height: size, stroke: color, fill: "none", strokeWidth: 1.5, strokeLinecap: "round", strokeLinejoin: "round" };
  const glyphs = {
    pulse: <svg viewBox="0 0 24 24" {...s}><path d="M2 12h4l2-6 4 12 3-9 2 3h5"/></svg>,
    ai_ops: <svg viewBox="0 0 24 24" {...s}><circle cx="12" cy="6" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/><path d="M12 8v3M12 11l-6 5M12 11l6 5"/><path d="M3 22h18" opacity=".5"/></svg>,
    campaign: <svg viewBox="0 0 24 24" {...s}><path d="M5 21V4l8 3-8 3"/><path d="M5 7l14-3v9l-14 3" opacity=".5"/></svg>,
    world: <svg viewBox="0 0 24 24" {...s}><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="9" ry="3.5"/><path d="M12 3v18"/></svg>,
    motif: <svg viewBox="0 0 24 24" {...s}><circle cx="12" cy="12" r="2"/><circle cx="4" cy="6" r="1.5"/><circle cx="20" cy="6" r="1.5"/><circle cx="4" cy="18" r="1.5"/><circle cx="20" cy="18" r="1.5"/><path d="M12 12 4 6M12 12l8-6M12 12l-8 6M12 12l8 6"/></svg>,
    basin: <svg viewBox="0 0 24 24" {...s}><path d="M2 8c3 0 4 8 10 8s7-8 10-8"/><path d="M2 13c3 0 4 5 10 5s7-5 10-5" opacity=".5"/><path d="M2 18h20" opacity=".3"/></svg>,
    falsifier: <svg viewBox="0 0 24 24" {...s}><path d="M12 2 3 7v6c0 5 4 8 9 9 5-1 9-4 9-9V7l-9-5z"/><path d="m9 9 6 6M15 9l-6 6"/></svg>,
    doctrine: <svg viewBox="0 0 24 24" {...s}><rect x="5" y="3" width="14" height="18" rx="1"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>,
    factory: <svg viewBox="0 0 24 24" {...s}><path d="M4 21V10l5 3V10l5 3V10l5 3v8z"/><path d="M9 21v-4M14 21v-4M19 21v-4" opacity=".4"/></svg>,
    portfolio: <svg viewBox="0 0 24 24" {...s}><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M3 8h18M8 3v18" opacity=".5"/></svg>,
    graph: <svg viewBox="0 0 24 24" {...s}><circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="12" cy="14" r="2"/><circle cx="6" cy="20" r="1.5"/><circle cx="20" cy="18" r="1.5"/><path d="M7 7l4 6M17 7l-4 6M11 15 7 19M13 15l6 3"/></svg>,
    search: <svg viewBox="0 0 24 24" {...s}><circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/></svg>,
    snapshot: <svg viewBox="0 0 24 24" {...s}><rect x="3" y="6" width="18" height="14" rx="2"/><circle cx="12" cy="13" r="3.5"/><path d="M9 6V4h6v2"/></svg>,
  };
  return glyphs[id] || null;
};
window.RoomGlyph = RoomGlyph;
