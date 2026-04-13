import React from 'react';
import { Icons } from './Icons';

export function HomePage({ onGetStarted }) {
  return (
    <div className="home-shell">
      {/* ── HERO ── */}
      <header className="home-hero">
        <div className="brand-mark">
          <Icons.Spark />
          <span>Fair View</span>
        </div>
        <h1>Unbiased interviews,<br />powered by AI.</h1>
        <p className="hero-sub">
          Traditional interviews are inconsistent — some interviewers ask easy questions while
          others go tough for the exact same role. Fair View levels the playing field by evaluating
          <strong> both </strong> the quality of questions <em>and</em> the candidate's answers with AI,
          ensuring every interview is scored fairly.
        </p>
        <button className="primary-btn hero-cta" onClick={onGetStarted}>
          Get started <Icons.Arrow />
        </button>
      </header>

      {/* ── PROBLEM STATEMENT ── */}
      <section className="home-section">
        <div className="section-tag">The problem</div>
        <h2>Why traditional interviews aren't fair</h2>
        <div className="problem-grid">
          <article className="card problem-card">
            <div className="problem-icon inconsistent" />
            <h3>Inconsistent difficulty</h3>
            <p>
              Two candidates apply for the same Cloud Engineer role. One interviewer asks
              "What is a virtual machine?" while another asks "Design a multi-region active-active
              failover architecture." Both candidates are scored on the same scale — but the bar
              was never the same.
            </p>
          </article>
          <article className="card problem-card">
            <div className="problem-icon irrelevant" />
            <h3>Irrelevant questions</h3>
            <p>
              A frontend developer candidate is asked low-level kernel questions because the
              interviewer is a systems engineer. The questions don't reflect the actual job,
              yet the score decides the hire.
            </p>
          </article>
          <article className="card problem-card">
            <div className="problem-icon subjective" />
            <h3>Subjective scoring</h3>
            <p>
              Without a structured rubric, two interviewers can hear the same answer and give
              wildly different scores. Mood, bias, and personal preference creep in, and there's
              no audit trail.
            </p>
          </article>
        </div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section className="home-section">
        <div className="section-tag">The solution</div>
        <h2>How Fair View removes bias</h2>
        <p className="section-sub">
          Fair View doesn't just score the candidate — it evaluates the interviewer's questions too.
          Every question is checked for <strong>relevance</strong> to the job role and
          <strong> difficulty appropriateness</strong> for the seniority level, so the entire
          session is transparent and auditable.
        </p>

        <div className="dual-eval-grid">
          <article className="card eval-card interviewer-eval">
            <div className="eval-header">
              <span className="eval-badge interviewer">Interviewer</span>
              <h3>Question evaluation</h3>
            </div>
            <ul>
              <li><strong>Relevance</strong> — Is the question related to the target job role?</li>
              <li><strong>Difficulty</strong> — Is it appropriate for the position level (Junior / Mid / Senior)?</li>
              <li>Flagged as <em>Too Easy</em>, <em>Appropriate</em>, or <em>Too Hard</em></li>
            </ul>
          </article>
          <article className="card eval-card candidate-eval">
            <div className="eval-header">
              <span className="eval-badge candidate">Candidate</span>
              <h3>Answer evaluation</h3>
            </div>
            <ul>
              <li><strong>Score 0–100</strong> — accuracy, depth, and technical correctness</li>
              <li><strong>Feedback</strong> — specific, actionable commentary on the answer</li>
              <li>Scored against the actual job role and seniority context</li>
            </ul>
          </article>
        </div>
      </section>

      {/* ── FLOWCHART ── */}
      <section className="home-section">
        <div className="section-tag">Platform flow</div>
        <h2>End-to-end interview pipeline</h2>
        <div className="flowchart">
          <div className="flow-row">
            <div className="flow-node">
              <div className="flow-icon">👤</div>
              <strong>Sign up</strong>
              <span>Choose interviewer or candidate role</span>
            </div>
            <div className="flow-arrow" />
            <div className="flow-node">
              <div className="flow-icon">🏠</div>
              <strong>Create / join room</strong>
              <span>Interviewer sets job role &amp; level, shares room code</span>
            </div>
            <div className="flow-arrow" />
            <div className="flow-node">
              <div className="flow-icon">🎥</div>
              <strong>Video interview</strong>
              <span>Peer-to-peer WebRTC call, audio recorded on both sides</span>
            </div>
          </div>

          <div className="flow-connector-down" />

          <div className="flow-row reversed">
            <div className="flow-node">
              <div className="flow-icon">📊</div>
              <strong>Review results</strong>
              <span>Both participants see scores, feedback, and bias flags</span>
            </div>
            <div className="flow-arrow reversed" />
            <div className="flow-node highlight">
              <div className="flow-icon">🤖</div>
              <strong>AI evaluation</strong>
              <span>Gemini scores answers AND rates question quality</span>
            </div>
            <div className="flow-arrow reversed" />
            <div className="flow-node">
              <div className="flow-icon">🔀</div>
              <strong>Transcript merge</strong>
              <span>Two audio streams merged into Q&amp;A pairs by AI</span>
            </div>
          </div>

          <div className="flow-connector-down" />

          <div className="flow-row single">
            <div className="flow-node final">
              <div className="flow-icon">✅</div>
              <strong>Fair outcome</strong>
              <span>Transparent, auditable, and bias-aware evaluation for every session</span>
            </div>
          </div>
        </div>
      </section>

      {/* ── KEY METRICS ── */}
      <section className="home-section">
        <div className="section-tag">What gets evaluated</div>
        <h2>Every session produces a full report</h2>
        <div className="metrics-grid">
          <div className="card metric-card">
            <div className="metric-value accent">0–100</div>
            <div className="metric-label">Answer score per question</div>
          </div>
          <div className="card metric-card">
            <div className="metric-value warm">Relevance</div>
            <div className="metric-label">Is the question related to the job?</div>
          </div>
          <div className="card metric-card">
            <div className="metric-value success">Difficulty</div>
            <div className="metric-label">Appropriate for the seniority level?</div>
          </div>
          <div className="card metric-card">
            <div className="metric-value">Feedback</div>
            <div className="metric-label">Specific AI commentary on each answer</div>
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="home-cta-section">
        <h2>Ready for fairer interviews?</h2>
        <p>Create your account and run your first evaluated session in minutes.</p>
        <button className="primary-btn hero-cta" onClick={onGetStarted}>
          Get started <Icons.Arrow />
        </button>
      </section>

      <footer className="home-footer">
        <div className="brand-mark small">
          <Icons.Spark />
          <span>Fair View</span>
        </div>
        <span className="muted-copy">AI-powered interview evaluation platform</span>
      </footer>
    </div>
  );
}
