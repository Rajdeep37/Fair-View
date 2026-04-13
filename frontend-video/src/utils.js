import { API_BASE, STORAGE_KEY } from './config';

export function readStoredSession() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function persistSession(session) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
}

export function clearStoredSession() {
  localStorage.removeItem(STORAGE_KEY);
}

export async function apiRequest(path, { method = 'GET', body, token, isForm = false } = {}) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body && !isForm) headers['Content-Type'] = 'application/json';

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? (isForm ? body : JSON.stringify(body)) : undefined,
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || payload.error || 'Request failed');
  }
  return payload;
}

export function formatTimestamp(value) {
  if (!value) return 'Just now';
  const date = new Date(value);
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date);
}

export function scoreTone(score) {
  const numericScore = Number(score || 0);
  if (numericScore >= 80) return 'success';
  if (numericScore >= 50) return 'warning';
  return 'danger';
}

export function readAverageScore(report) {
  const rawScore = report?.total_score ?? report?.totalScore ?? 0;
  const numeric = Number(rawScore);
  return Number.isFinite(numeric) ? numeric : 0;
}

export function normalizeInterview(item) {
  const report = item.evaluation_report || {};
  return {
    ...item,
    evaluation_report: report,
    score: readAverageScore(report),
    qa_pairs: item.qa_pairs || [],
  };
}
