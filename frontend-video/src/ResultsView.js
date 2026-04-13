import React, { useEffect, useState, useRef } from 'react';
import { Icons } from './Icons';
import { API_BASE } from './config';
import { formatTimestamp, scoreTone, readAverageScore, normalizeInterview } from './utils';

export function ResultsView({ user, token, interview, interviews, onBack, onSelectInterview, onInterviewUpdate }) {
  const [liveInterview, setLiveInterview] = useState(interview);
  const [pollFailed, setPollFailed] = useState(false);
  const pollRef = useRef(null);
  const failTimerRef = useRef(null);

  const isLoading = liveInterview && liveInterview.status === 'pending_merge' && !pollFailed;

  useEffect(() => {
    setLiveInterview(interview);
    setPollFailed(false);
  }, [interview]);

  useEffect(() => {
    if (!liveInterview?.id || liveInterview.status !== 'pending_merge') return;

    const poll = async () => {
      try {
        const res = await fetch(`${API_BASE}/interviews/${liveInterview.id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) return;
        const data = await res.json();
        if (data.status === 'completed' || data.status === 'skipped') {
          clearInterval(pollRef.current);
          clearTimeout(failTimerRef.current);
          const updated = normalizeInterview(data);
          setLiveInterview(updated);
          if (onInterviewUpdate) onInterviewUpdate(updated);
        }
      } catch (_) { /* retry next tick */ }
    };

    pollRef.current = setInterval(poll, 5000);
    failTimerRef.current = setTimeout(() => {
      clearInterval(pollRef.current);
      setPollFailed(true);
    }, 120000); // 2 minutes timeout

    return () => {
      clearInterval(pollRef.current);
      clearTimeout(failTimerRef.current);
    };
  }, [liveInterview?.id, liveInterview?.status, token, onInterviewUpdate]);

  const report = liveInterview?.evaluation_report || {};
  const results = report.results || [];
  const score = readAverageScore(report);

  if (isLoading) {
    return (
      <div className="results-shell">
        <header className="results-topbar">
          <button className="ghost-btn compact back-btn" onClick={onBack}>
            <Icons.Arrow /> Dashboard
          </button>
          <div className="room-identity">
            <div className="eyebrow">Result review</div>
            <h1>{liveInterview?.room_name || liveInterview?.room_code || 'Interview results'}</h1>
          </div>
        </header>
        <div className="bootstrap-screen">
          <div className="loading-panel">
            <Icons.Loader />
            <h2>Evaluating interview…</h2>
            <p>The AI is analyzing the recordings. This may take a minute or two.</p>
          </div>
        </div>
      </div>
    );
  }

  if (pollFailed) {
    return (
      <div className="results-shell">
        <header className="results-topbar">
          <button className="ghost-btn compact back-btn" onClick={onBack}>
            <Icons.Arrow /> Dashboard
          </button>
          <div className="room-identity">
            <div className="eyebrow">Result review</div>
            <h1>{liveInterview?.room_name || liveInterview?.room_code || 'Interview results'}</h1>
          </div>
        </header>
        <div className="bootstrap-screen">
          <div className="loading-panel">
            <h2>Unable to evaluate</h2>
            <p>Results could not be retrieved. Please contact an administrator.</p>
            <button className="ghost-btn compact" onClick={onBack}><Icons.Arrow /> Back to dashboard</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="results-shell">
      <header className="results-topbar">
        <button className="ghost-btn compact back-btn" onClick={onBack}>
          <Icons.Arrow /> Dashboard
        </button>
        <div className="room-identity">
          <div className="eyebrow">Result review</div>
          <h1>{liveInterview?.room_name || liveInterview?.room_code || 'Interview results'}</h1>
        </div>
        <div className={`score-badge ${scoreTone(score)}`}>
          <span>{Math.round(score)}</span>
          <small>Overall</small>
        </div>
      </header>

      <section className="results-grid">
        <article className="card result-summary">
          <h2>Summary</h2>
          <p className="muted-copy">
            {user.role} view for {user.email}. Scores are stored in the database and visible to both participants.
          </p>
          <div className="summary-row">
            <div><span>Room</span><strong>{liveInterview?.room_code || liveInterview?.room_id}</strong></div>
            <div><span>Recorded</span><strong>{formatTimestamp(liveInterview?.created_at)}</strong></div>
          </div>
          {liveInterview?.full_transcript && (
            <div className="transcript-block">
              <h3>Transcript</h3>
              <p>{liveInterview.full_transcript}</p>
            </div>
          )}
        </article>

        <aside className="card history-panel">
          <div className="card-header">
            <h3>History</h3>
            <span className="count-badge">{interviews.length}</span>
          </div>
          <div className="history-list">
            {interviews.map((item) => (
              <button key={item.id} className="history-item" onClick={() => onSelectInterview(normalizeInterview(item))}>
                <div>
                  <strong>{item.room_code || item.room_id}</strong>
                  <span>{formatTimestamp(item.created_at)}</span>
                </div>
                <span className={`score-chip ${scoreTone(item.evaluation_report?.total_score)}`}>
                  {Math.round(readAverageScore(item.evaluation_report))}
                </span>
              </button>
            ))}
          </div>
        </aside>
      </section>

      <section className="card questions-panel">
        <div className="card-header">
          <h3>Interview breakdown</h3>
          <span className="count-badge">{results.length} scored</span>
        </div>

        <div className="result-cards">
          {results.length === 0 ? (
            <div className="empty-state">No scored questions available for this session.</div>
          ) : (
            results.map((item, index) => (
              <article key={`${item.question}-${index}`} className="question-card">
                <div className="question-head">
                  <div>
                    <div className="card-kicker">
                      {item.topic || 'General'}
                      {item.question_relevance ? ` · ${item.question_relevance}` : ''}
                      {item.difficulty_assessment ? ` · ${item.difficulty_assessment}` : ''}
                    </div>
                    <h4>{item.question}</h4>
                  </div>
                  <span className={`score-chip ${scoreTone(item.score)}`}>{item.score}/100</span>
                </div>
                <p className="answer-text"><strong>Answer:</strong> {item.candidate_answer || item.answer}</p>
                {item.feedback && <div className="feedback-box">{item.feedback}</div>}
              </article>
            ))
          )}
        </div>
      </section>
    </div>
  );
}
