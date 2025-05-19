/** Minimal ESM wrapper (works in browser or Node 18+). */
export async function chat(baseUrl, character, message) {
  const r = await fetch(`${baseUrl.replace(/\/$/, '')}/chat`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ character, message })
  });
  if (!r.ok) {
    throw new Error(`HTTP ${r.status}`);
  }
  const json = await r.json();
  return json.reply;
}

export async function manifest(baseUrl) {
  const r = await fetch(`${baseUrl.replace(/\/$/, '')}/manifest`);
  if (!r.ok) {
    throw new Error(`HTTP ${r.status}`);
  }
  return await r.json();
}
