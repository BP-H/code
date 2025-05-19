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

export async function* chatStream(baseUrl, character, message) {
  const r = await fetch(`${baseUrl.replace(/\/$/, '')}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ character, message })
  });
  if (!r.ok) {
    throw new Error(`HTTP ${r.status}`);
  }
  const reader = r.body.getReader();
  const dec = new TextDecoder();
  let buf = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    let idx;
    while ((idx = buf.indexOf('\n\n')) >= 0) {
      const line = buf.slice(0, idx);
      buf = buf.slice(idx + 2);
      if (line.startsWith('data: ')) {
        yield line.slice(6);
      }
    }
  }
  if (buf.startsWith('data: ')) {
    yield buf.slice(6);
  }
}

export async function manifest(baseUrl) {
  const r = await fetch(`${baseUrl.replace(/\/$/, '')}/manifest`);
  if (!r.ok) {
    throw new Error(`HTTP ${r.status}`);
  }
  return await r.json();
}
