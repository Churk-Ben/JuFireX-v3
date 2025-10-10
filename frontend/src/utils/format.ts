export function formatDate(ts: number): string {
  const d = new Date(ts)
  return d.toISOString()
}