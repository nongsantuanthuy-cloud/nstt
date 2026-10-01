// Hàm hỗ trợ thao tác Google Flow — dán vào javascript_tool của Claude in Chrome (trang dự án Flow).
// Thay window.__P bằng các cảnh cần tạo: { "S06": { "p": "<prompt_flow>", "nv": ["Thang Lanh", "Bay Loi"] } }
// Mỗi lệnh javascript_tool tối đa 45 s → gọi __prep cho TỪNG cảnh, kiểm tra, rồi __submit().
window.__sleep = ms => new Promise(r => setTimeout(r, ms));

// Gắn 1 nhân vật Flow vào ô nhập (mở bảng "Thêm thành phần", tìm tên, bấm đúng mục "Nhân vật").
window.__addChar = async (name) => {
  if (!document.querySelector('input[placeholder="Tìm kiếm thành phần"]')) {
    const b = [...document.querySelectorAll('button')].find(e => (e.getAttribute('aria-label') || '').includes('Thêm thành phần vào ô nhập'));
    if (!b) return 'no plus';
    b.click(); await __sleep(1500);
  }
  const i = document.querySelector('input[placeholder="Tìm kiếm thành phần"]');
  if (!i) return 'no search';
  i.focus(); i.select(); document.execCommand('insertText', false, name);
  for (let k = 0; k < 8; k++) {
    await __sleep(600);
    const o = [...document.querySelectorAll('[role=option]')].find(e => e.innerText.trim().split('\n')[0].trim() === name);
    if (o) { o.click(); await __sleep(1500); return 'added ' + name; }
  }
  return 'no option ' + name;
};

window.__editor = () => document.querySelector('.ProseMirror[contenteditable=true]');

// Dán prompt (thay toàn bộ nội dung ô nhập) và xác nhận khớp nguyên văn.
window.__setPrompt = async (t) => {
  const e = __editor(); if (!e) return 'no editor';
  e.focus(); document.execCommand('selectAll'); document.execCommand('insertText', false, t);
  await __sleep(800);
  return e.innerText.trim() === t.trim() ? 'prompt ok' : 'prompt MISMATCH';
};

window.__prep = async (so) => {
  const s = __P[so]; const r = [];
  for (const n of s.nv) r.push(await __addChar(n));
  r.push(await __setPrompt(s.p));
  return so + ': ' + r.join(', ');
};

window.__submit = () => {
  const b = [...document.querySelectorAll('button')].find(b => (b.getAttribute('aria-label') || b.innerText).includes('Bắt đầu tạo'));
  if (!b) return 'no submit';
  b.click(); return 'submitted';
};

// Đọc cài đặt hiện tại (model + tín dụng) — phải là "Veo 3.1 - Lite" và "10 tín dụng".
window.__checkModel = async () => {
  [...document.querySelectorAll('button')].find(b => b.innerText.includes('720p')).click();
  await __sleep(1000);
  const t = document.body.innerText, i = t.indexOf('tín dụng');
  return t.slice(Math.max(0, i - 90), i + 10).replace(/\n/g, ' | ');  // đóng menu bằng phím Escape sau đó
};

window.__P = window.__P || {};
'helpers ready';
