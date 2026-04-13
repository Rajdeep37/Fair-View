import React from 'react';
import { Icons } from './Icons';

export function AuthView({ mode, authForm, setAuthForm, errorMessage, onSubmit, onToggleMode, onBack }) {
  return (
    <div className="auth-shell">
      <section className="auth-hero">
        {onBack && <button className="ghost-btn compact back-btn auth-back" onClick={onBack}><Icons.Arrow /> Home</button>}
        <div className="brand-mark">
          <Icons.Spark />
          <span>Fair View</span>
        </div>
        <h1>AI-powered interview evaluation platform.</h1>
        <p>
          Create rooms, conduct interviews over video, and get instant AI-driven scoring and feedback for every session.
        </p>
        <div className="hero-points">
          <div><Icons.Shield /><span>Secure authentication</span></div>
          <div><Icons.Door /><span>Sharable room codes</span></div>
          <div><Icons.Spark /><span>AI-powered scoring</span></div>
        </div>
      </section>

      <section className="auth-card">
        <div className="tab-row">
          <button className={`tab ${mode === 'signin' ? 'active' : ''}`} onClick={() => onToggleMode('signin')}>Sign in</button>
          <button className={`tab ${mode === 'signup' ? 'active' : ''}`} onClick={() => onToggleMode('signup')}>Sign up</button>
        </div>

        <h2>{mode === 'signin' ? 'Welcome back' : 'Create your account'}</h2>
        <p className="muted-copy">{mode === 'signin' ? 'Sign in to access your rooms and scores.' : 'Choose your role to get started.'}</p>

        <form className="auth-form" onSubmit={onSubmit}>
          <label>
            Email
            <input type="email" value={authForm.email} onChange={(e) => setAuthForm({ ...authForm, email: e.target.value })} placeholder="you@example.com" required />
          </label>

          <label>
            Password
            <input type="password" value={authForm.password} onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })} placeholder="••••••••" minLength={6} required />
          </label>

          {mode === 'signup' && (
            <label>
              Role
              <div className="role-pills">
                {['interviewer', 'candidate'].map((role) => (
                  <button key={role} type="button" className={`pill ${authForm.role === role ? 'active' : ''}`} onClick={() => setAuthForm({ ...authForm, role })}>
                    {role}
                  </button>
                ))}
              </div>
            </label>
          )}

          {errorMessage && <div className="notice error">{errorMessage}</div>}
          <button type="submit" className="primary-btn full-width">{mode === 'signin' ? 'Sign in' : 'Create account'}</button>
        </form>
      </section>
    </div>
  );
}
