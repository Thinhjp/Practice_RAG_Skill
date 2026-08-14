const $ = (selector) => document.querySelector(selector);

const state = {
  mode: 'ask',
  busy: false,
  stats: { total_chunks: 0, embedding_dim: 0, unique_files: 0, files: [] },
};

const elements = {
  messages: $('#messages'),
  welcome: $('#welcome'),
  form: $('#chatForm'),
  input: $('#questionInput'),
  send: $('#sendButton'),
  modeHint: $('#modeHint'),
  sourceContent: $('#sourceContent'),
  sourceCount: $('#sourceCount'),
  fileInput: $('#fileInput'),
  dropZone: $('#dropZone'),
  uploadProgress: $('#uploadProgress'),
  documentList: $('#documentList'),
  sidebar: $('#sidebar'),
  sidebarBackdrop: $('#sidebarBackdrop'),
  sourcesPanel: $('#sourcesPanel'),
};

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || `Yêu cầu thất bại (${response.status})`);
  }
  return payload;
}

function toast(message, type = 'success') {
  const item = document.createElement('div');
  item.className = `toast ${type === 'error' ? 'error' : ''}`;
  item.textContent = message;
  $('#toastRegion').append(item);
  setTimeout(() => item.remove(), 3500);
}

function setStatus(online) {
  $('#statusDot').className = online ? 'online' : 'offline';
  $('#statusText').textContent = online ? 'Đang hoạt động' : 'Mất kết nối';
}

function fileType(name) {
  return (name.split('.').pop() || 'file').slice(0, 4);
}

async function refreshStats() {
  try {
    const stats = await api('/api/v1/stats');
    state.stats = stats;
    $('#fileCount').textContent = stats.unique_files;
    $('#chunkCount').textContent = stats.total_chunks;
    $('#embeddingDim').textContent = stats.embedding_dim || '—';
    renderDocuments(stats.files || []);
  } catch (error) {
    toast(error.message, 'error');
  }
}

function renderDocuments(files) {
  elements.documentList.replaceChildren();
  if (!files.length) {
    const empty = document.createElement('div');
    empty.className = 'empty-docs';
    empty.innerHTML = '<span>⌁</span><p>Chưa có tài liệu</p><small>Upload tệp đầu tiên để bắt đầu</small>';
    elements.documentList.append(empty);
    return;
  }

  files.forEach((file) => {
    const row = document.createElement('div');
    row.className = 'document-item';

    const icon = document.createElement('span');
    icon.className = 'file-icon';
    icon.textContent = fileType(file.file_name);

    const info = document.createElement('div');
    const name = document.createElement('strong');
    name.textContent = file.file_name;
    name.title = file.file_name;
    const count = document.createElement('small');
    count.textContent = `${file.chunk_count} đoạn dữ liệu`;
    info.append(name, count);

    const view = document.createElement('button');
    view.type = 'button';
    view.textContent = '›';
    view.title = 'Xem các đoạn tài liệu';
    view.addEventListener('click', () => showDocumentChunks(file.file_name));
    row.append(icon, info, view);
    elements.documentList.append(row);
  });
}

async function showDocumentChunks(fileName) {
  try {
    const data = await api(`/api/v1/chunks?file_name=${encodeURIComponent(fileName)}&limit=100`);
    renderSources(data.chunks.map((chunk, index) => ({
      ...chunk,
      source_number: index + 1,
      similarity_score: null,
    })));
    openSources();
  } catch (error) {
    toast(error.message, 'error');
  }
}

async function uploadFile(file) {
  if (!file) return;
  const extension = `.${file.name.split('.').pop().toLowerCase()}`;
  if (!['.pdf', '.docx', '.txt'].includes(extension)) {
    toast('Chỉ hỗ trợ tệp PDF, DOCX hoặc TXT.', 'error');
    return;
  }
  if (file.size > 50 * 1024 * 1024) {
    toast('Tệp vượt quá giới hạn 50 MB.', 'error');
    return;
  }

  const form = new FormData();
  form.append('file', file);
  elements.dropZone.classList.add('hidden');
  elements.uploadProgress.classList.remove('hidden');
  try {
    const result = await api('/api/v1/upload', { method: 'POST', body: form });
    toast(`Đã thêm ${result.file_name} · ${result.chunks_count} đoạn`);
    await refreshStats();
    addMessage('assistant', `Mình đã đọc xong “${result.file_name}” và tạo ${result.chunks_count} đoạn dữ liệu. Bạn có thể bắt đầu đặt câu hỏi.`);
    elements.input.focus();
  } catch (error) {
    toast(error.message, 'error');
  } finally {
    elements.dropZone.classList.remove('hidden');
    elements.uploadProgress.classList.add('hidden');
    elements.fileInput.value = '';
  }
}

function addMessage(role, text, options = {}) {
  elements.welcome.classList.add('hidden');
  const row = document.createElement('article');
  row.className = `message-row ${role}`;

  const avatar = document.createElement('span');
  avatar.className = 'message-avatar';
  avatar.textContent = role === 'user' ? 'B' : 'R';

  const body = document.createElement('div');
  body.className = 'message-body';
  const meta = document.createElement('div');
  meta.className = 'message-meta';
  meta.textContent = role === 'user' ? 'Bạn' : 'RAGmate';
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  bubble.textContent = text;
  body.append(meta, bubble);

  if (role === 'assistant' && !options.loading) {
    const tools = document.createElement('div');
    tools.className = 'message-tools';
    const copy = document.createElement('button');
    copy.type = 'button';
    copy.textContent = 'Sao chép câu trả lời';
    copy.addEventListener('click', async () => {
      await navigator.clipboard.writeText(text);
      toast('Đã sao chép câu trả lời');
    });
    tools.append(copy);
    body.append(tools);
  }

  row.append(avatar, body);
  elements.messages.append(row);
  elements.messages.scrollTop = elements.messages.scrollHeight;
  return row;
}

function addTyping() {
  const row = addMessage('assistant', '', { loading: true });
  row.dataset.typing = 'true';
  const bubble = row.querySelector('.message-bubble');
  bubble.classList.add('typing-bubble');
  bubble.innerHTML = '<i></i><i></i><i></i>';
  return row;
}

async function enrichSources(sources) {
  return Promise.all(sources.map(async (source) => {
    if (source.text) return source;
    try {
      const chunk = await api(`/api/v1/chunks/${source.chunk_id}`);
      return { ...chunk, ...source };
    } catch {
      return source;
    }
  }));
}

function renderSources(sources) {
  elements.sourceContent.replaceChildren();
  elements.sourceCount.textContent = sources.length;
  if (!sources.length) {
    const empty = document.createElement('div');
    empty.className = 'source-empty';
    empty.innerHTML = '<span>⌕</span><h3>Không tìm thấy nguồn</h3><p>Thử diễn đạt câu hỏi bằng các từ khóa xuất hiện trong tài liệu.</p>';
    elements.sourceContent.append(empty);
    return;
  }

  sources.forEach((source, index) => {
    const card = document.createElement('article');
    card.className = 'source-card';
    const head = document.createElement('div');
    head.className = 'source-card-head';
    const number = document.createElement('div');
    number.className = 'source-number';
    const badge = document.createElement('span');
    badge.textContent = source.source_number || index + 1;
    const name = document.createElement('strong');
    name.textContent = source.file_name || 'Tài liệu';
    number.append(badge, name);
    head.append(number);
    if (typeof source.similarity_score === 'number') {
      const score = document.createElement('span');
      score.className = 'score';
      score.textContent = `${Math.max(0, source.similarity_score * 100).toFixed(0)}%`;
      score.title = 'Độ tương đồng';
      head.append(score);
    }
    const excerpt = document.createElement('p');
    excerpt.textContent = source.text || 'Không tải được nội dung đoạn.';
    const footer = document.createElement('small');
    footer.textContent = `Đoạn ${Number(source.chunk_index ?? index) + 1}`;
    card.append(head, excerpt, footer);
    card.addEventListener('click', () => {
      excerpt.style.webkitLineClamp = excerpt.style.webkitLineClamp === 'unset' ? '5' : 'unset';
    });
    elements.sourceContent.append(card);
  });
}

async function submitQuestion(question) {
  const text = question.trim();
  if (!text || state.busy) return;
  state.busy = true;
  elements.send.disabled = true;
  addMessage('user', text);
  elements.input.value = '';
  resizeInput();
  const typing = addTyping();

  try {
    if (state.mode === 'ask') {
      const data = await api('/api/v1/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text, top_k: 5, threshold: -1 }),
      });
      typing.remove();
      addMessage('assistant', data.answer);
      const sources = await enrichSources(data.sources || []);
      renderSources(sources);
    } else {
      const results = await api('/api/v1/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text, top_k: 8, threshold: -1 }),
      });
      typing.remove();
      const response = results.length
        ? `Mình tìm thấy ${results.length} đoạn liên quan. Mở bảng “Nguồn tham chiếu” để xem và đối chiếu nội dung.`
        : 'Mình chưa tìm thấy đoạn tài liệu phù hợp với câu hỏi này.';
      addMessage('assistant', response);
      renderSources(results.map((item, index) => ({ ...item, source_number: index + 1 })));
    }
    if (window.innerWidth <= 1120) openSources();
  } catch (error) {
    typing.remove();
    addMessage('assistant', `Mình chưa thể xử lý câu hỏi: ${error.message}`);
    toast(error.message, 'error');
  } finally {
    state.busy = false;
    elements.send.disabled = !elements.input.value.trim();
    elements.input.focus();
  }
}

function resizeInput() {
  elements.input.style.height = 'auto';
  elements.input.style.height = `${Math.min(elements.input.scrollHeight, 145)}px`;
  elements.send.disabled = state.busy || !elements.input.value.trim();
}

function openSources() { elements.sourcesPanel.classList.add('open'); }
function closeSources() { elements.sourcesPanel.classList.remove('open'); }
function closeSidebar() {
  elements.sidebar.classList.remove('open');
  elements.sidebarBackdrop.classList.remove('open');
}

function resetChat() {
  elements.messages.querySelectorAll('.message-row').forEach((item) => item.remove());
  elements.welcome.classList.remove('hidden');
  renderSources([]);
  closeSources();
  elements.input.focus();
}

elements.form.addEventListener('submit', (event) => {
  event.preventDefault();
  submitQuestion(elements.input.value);
});
elements.input.addEventListener('input', resizeInput);
elements.input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    elements.form.requestSubmit();
  }
});

$('#suggestions').addEventListener('click', (event) => {
  const button = event.target.closest('[data-question]');
  if (button) submitQuestion(button.dataset.question);
});

document.querySelectorAll('[data-mode]').forEach((button) => {
  button.addEventListener('click', () => {
    state.mode = button.dataset.mode;
    document.querySelectorAll('[data-mode]').forEach((item) => item.classList.toggle('active', item === button));
    elements.modeHint.innerHTML = state.mode === 'ask'
      ? '<i>✦</i> Trả lời có dẫn nguồn'
      : '<i>⌕</i> Hiển thị các đoạn gần nhất';
    elements.input.placeholder = state.mode === 'ask'
      ? 'Hỏi về tài liệu của bạn…'
      : 'Nhập từ khóa cần tìm…';
  });
});

elements.fileInput.addEventListener('change', () => uploadFile(elements.fileInput.files[0]));
['dragenter', 'dragover'].forEach((name) => elements.dropZone.addEventListener(name, (event) => {
  event.preventDefault();
  elements.dropZone.classList.add('dragover');
}));
['dragleave', 'drop'].forEach((name) => elements.dropZone.addEventListener(name, (event) => {
  event.preventDefault();
  elements.dropZone.classList.remove('dragover');
}));
elements.dropZone.addEventListener('drop', (event) => uploadFile(event.dataTransfer.files[0]));

$('#clearDatabase').addEventListener('click', async () => {
  if (!confirm('Xóa toàn bộ vector và dữ liệu đã lập chỉ mục? Tệp upload gốc vẫn được giữ lại.')) return;
  try {
    await api('/api/v1/database', { method: 'DELETE' });
    await refreshStats();
    resetChat();
    toast('Đã xóa kho dữ liệu');
  } catch (error) {
    toast(error.message, 'error');
  }
});

$('#newChat').addEventListener('click', resetChat);
$('#toggleSources').addEventListener('click', () => elements.sourcesPanel.classList.toggle('open'));
$('#closeSources').addEventListener('click', closeSources);
$('#openSidebar').addEventListener('click', () => {
  elements.sidebar.classList.add('open');
  elements.sidebarBackdrop.classList.add('open');
});
$('#closeSidebar').addEventListener('click', closeSidebar);
elements.sidebarBackdrop.addEventListener('click', closeSidebar);
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeSidebar();
    closeSources();
  }
});

async function initialize() {
  try {
    await api('/api/v1/health');
    setStatus(true);
  } catch {
    setStatus(false);
  }
  await refreshStats();
}

initialize();
