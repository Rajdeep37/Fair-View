import React from 'react';
import { Icons } from './Icons';
import { formatTimestamp, normalizeInterview, readAverageScore, scoreTone } from './utils';

export function DashboardView({
  user, rooms, interviews, roomName, setRoomName, roomJobRole, setRoomJobRole,
  roomPosition, setRoomPosition, joinCode, setJoinCode, loading, errorMessage,
  statusMessage, onCreateRoom, onJoinRoom, onCloseRoom, onSelectInterview, onSignOut,
}) {
  return (
    <div className="dashboard-shell">
      <header className="dashboard-topbar">
        <div className="topbar-left">
          <div className="brand-mark small"><Icons.Spark /><span>Fair View</span></div>
        </div>
        <div className="topbar-right">
          <span className="role-badge">{user.role}</span>
          <span className="user-email">{user.email}</span>
          <button className="ghost-btn compact" onClick={onSignOut}>Sign out</button>
        </div>
      </header>

      <section className="overview-grid">
        <article className="hero-panel card">
          <div className="card-kicker">Overview</div>
          <h2>{user.role === 'interviewer' ? 'Manage interviews' : 'Your interviews'}</h2>
          <p className="muted-copy">
            {user.role === 'interviewer'
              ? 'Create rooms with a job role and position level, share the code, and review AI-generated scores.'
              : 'Join a room using the code from your interviewer, complete the interview, and track your results.'}
          </p>
          <div className="mini-stats">
            <div className="stat-card"><strong>{rooms.length}</strong><span>Rooms</span></div>
            <div className="stat-card"><strong>{interviews.length}</strong><span>Interviews</span></div>
          </div>
        </article>

        <article className="card action-card">
          <div className="card-kicker">Quick actions</div>
          {user.role === 'interviewer' && (
            <div className="action-form">
              <label>Room name<input value={roomName} onChange={(e) => setRoomName(e.target.value)} placeholder="Cloud Engineer Interview" /></label>
              <label>Job role<input value={roomJobRole} onChange={(e) => setRoomJobRole(e.target.value)} placeholder="e.g. Cloud Engineer" /></label>
              <label>
                Position level
                <div className="role-pills">
                  {['Junior', 'Mid', 'Senior'].map((lvl) => (
                    <button key={lvl} type="button" className={`pill ${roomPosition === lvl ? 'active' : ''}`} onClick={() => setRoomPosition(lvl)}>{lvl}</button>
                  ))}
                </div>
              </label>
              <button className="primary-btn" onClick={onCreateRoom}><Icons.Plus /> Create room</button>
            </div>
          )}
          {user.role === 'candidate' && (
            <div className="action-form">
              <label>Room code<input value={joinCode} onChange={(e) => setJoinCode(e.target.value.toUpperCase())} placeholder="AB12CD34" /></label>
              <button className="primary-btn" onClick={() => onJoinRoom()}><Icons.Door /> Join room</button>
            </div>
          )}
          {statusMessage && <div className="notice success">{statusMessage}</div>}
          {errorMessage && <div className="notice error">{errorMessage}</div>}
          {loading && <div className="inline-loading"><Icons.Loader /> Syncing…</div>}
        </article>
      </section>

      <section className="workspace-grid">
        <article className="card list-card">
          <div className="card-header"><h3>Rooms</h3><span className="count-badge">{rooms.length}</span></div>
          {rooms.length === 0 ? (
            <div className="empty-state">No rooms yet. {user.role === 'interviewer' ? 'Create one above.' : 'Ask your interviewer for a code.'}</div>
          ) : (
            <div className="row-list">
              {rooms.map((room) => (
                <div key={room.id} className="row-card room-row">
                  <div className="row-info">
                    <strong>{room.name}</strong>
                    <div className="row-sub">
                      <span className="code-tag">{room.code}</span>
                      {room.job_role && <span className="meta-tag">{room.job_role}</span>}
                      {room.position && <span className="meta-tag">{room.position}</span>}
                    </div>
                  </div>
                  <div className="row-meta">
                    <span className={`status-dot ${room.status}`}>{room.status}</span>
                    {room.status !== 'completed' && room.status !== 'closed' && (
                      <button className="row-action-btn" onClick={() => onJoinRoom(room.code)}>Open <Icons.Arrow /></button>
                    )}
                    {user.role === 'interviewer' && room.interviewer_id === user.id && room.status !== 'closed' && room.status !== 'completed' && (
                      <button className="row-action-btn danger" onClick={() => onCloseRoom(room)}>Close</button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </article>

        <article className="card list-card">
          <div className="card-header"><h3>Results</h3><span className="count-badge">{interviews.length}</span></div>
          {interviews.length === 0 ? (
            <div className="empty-state">No interviews scored yet.</div>
          ) : (
            <div className="row-list">
              {interviews.map((interview) => (
                <button key={interview.id} className="row-card clickable" onClick={() => onSelectInterview(normalizeInterview(interview))}>
                  <div className="row-info">
                    <strong>{interview.room_code || interview.room_id}</strong>
                    <span className="row-date">{formatTimestamp(interview.created_at)}</span>
                  </div>
                  <div className="row-meta">
                    <span className={`score-chip ${scoreTone(interview.evaluation_report?.total_score)}`}>
                      {Math.round(readAverageScore(interview.evaluation_report))}
                    </span>
                    <Icons.Arrow />
                  </div>
                </button>
              ))}
            </div>
          )}
        </article>
      </section>
    </div>
  );
}
