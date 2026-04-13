import React, { useCallback, useEffect, useState } from 'react';
import './App.css';
import { Icons } from './Icons';
import { API_BASE } from './config';
import { readStoredSession, persistSession, clearStoredSession, apiRequest, normalizeInterview } from './utils';
import { AuthView } from './AuthView';
import { DashboardView } from './DashboardView';
import { InterviewRoom } from './InterviewRoom';
import { ResultsView } from './ResultsView';
import { HomePage } from './HomePage';

function App() {
  const [bootstrapping, setBootstrapping] = useState(true);
  const [session, setSession] = useState(() => readStoredSession());
  const [view, setView] = useState(session?.token ? 'dashboard' : 'home');
  const [authMode, setAuthMode] = useState('signin');
  const [authForm, setAuthForm] = useState({ email: '', password: '', role: 'interviewer' });
  const [roomName, setRoomName] = useState('Fair View Interview');
  const [roomJobRole, setRoomJobRole] = useState('');
  const [roomPosition, setRoomPosition] = useState('Mid');
  const [joinCode, setJoinCode] = useState('');
  const [rooms, setRooms] = useState([]);
  const [interviews, setInterviews] = useState([]);
  const [selectedInterview, setSelectedInterview] = useState(null);
  const [activeRoom, setActiveRoom] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [statusMessage, setStatusMessage] = useState('');
  const [loadingWorkspace, setLoadingWorkspace] = useState(false);

  const signOut = useCallback(() => {
    clearStoredSession();
    setSession(null);
    setRooms([]);
    setInterviews([]);
    setSelectedInterview(null);
    setActiveRoom(null);
    setErrorMessage('');
    setStatusMessage('');
    setView('home');
  }, []);

  const refreshWorkspace = useCallback(async (tokenOverride = session?.token) => {
    if (!tokenOverride) return;
    setLoadingWorkspace(true);
    try {
      const [me, roomList, interviewList] = await Promise.all([
        apiRequest('/auth/me', { token: tokenOverride }),
        apiRequest('/rooms/mine', { token: tokenOverride }),
        apiRequest('/interviews', { token: tokenOverride }),
      ]);

      const nextSession = { token: tokenOverride, user: me };
      setSession(nextSession);
      persistSession(nextSession);
      setRooms(roomList);
      setInterviews(interviewList.map(normalizeInterview));
    } catch (error) {
      signOut();
      setErrorMessage(error.message);
    } finally {
      setLoadingWorkspace(false);
      setBootstrapping(false);
    }
  }, [session?.token, signOut]);

  useEffect(() => {
    if (session?.token) {
      refreshWorkspace(session.token);
    } else {
      setBootstrapping(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleAuthSubmit = async (event) => {
    event.preventDefault();
    setErrorMessage('');
    setStatusMessage('');

    try {
      const path = authMode === 'signin' ? '/auth/signin' : '/auth/signup';
      const response = await apiRequest(path, {
        method: 'POST',
        body: authForm,
      });

      const nextSession = { token: response.access_token, user: response.user };
      setSession(nextSession);
      persistSession(nextSession);
      setView('dashboard');
      await refreshWorkspace(response.access_token);
    } catch (error) {
      setErrorMessage(error.message);
    }
  };

  const createRoom = async () => {
    setErrorMessage('');
    setStatusMessage('');

    if (!roomJobRole.trim()) {
      setErrorMessage('Please enter a job role for the interview.');
      return;
    }

    try {
      const room = await apiRequest('/rooms/create', {
        method: 'POST',
        body: { name: roomName, job_role: roomJobRole.trim(), position: roomPosition },
        token: session.token,
      });
      setActiveRoom(room);
      setStatusMessage(`Room ${room.code} created. Share the code with your candidate.`);
      setView('room');
      await refreshWorkspace(session.token);
    } catch (error) {
      setErrorMessage(error.message);
    }
  };

  const joinRoom = async (roomCode) => {
    const normalizedCode = String(roomCode || joinCode).trim().toUpperCase();
    if (!normalizedCode) {
      setErrorMessage('Enter a room code to continue.');
      return;
    }

    setErrorMessage('');
    setStatusMessage('');

    try {
      const room = await apiRequest('/rooms/join', {
        method: 'POST',
        body: { room_code: normalizedCode },
        token: session.token,
      });
      setActiveRoom(room);
      setJoinCode(normalizedCode);
      setView('room');
      await refreshWorkspace(session.token);
    } catch (error) {
      setErrorMessage(error.message);
    }
  };

  const closeRoom = async (room) => {
    setErrorMessage('');
    setStatusMessage('');

    try {
      await apiRequest(`/rooms/${room.id}/close`, {
        method: 'POST',
        token: session.token,
      });
      setStatusMessage(`Room ${room.code} closed.`);
      await refreshWorkspace(session.token);
    } catch (error) {
      setErrorMessage(error.message);
    }
  };

  if (bootstrapping) {
    return (
      <div className="bootstrap-screen">
        <div className="loading-panel">
          <Icons.Loader />
          <h2>Loading workspace</h2>
          <p>Checking your session and fetching interview history.</p>
        </div>
      </div>
    );
  }

  if (!session?.token) {
    if (view === 'auth') {
      return (
        <AuthView
          mode={authMode}
          authForm={authForm}
          setAuthForm={setAuthForm}
          errorMessage={errorMessage}
          onSubmit={handleAuthSubmit}
          onToggleMode={(nextMode) => {
            setAuthMode(nextMode);
            setErrorMessage('');
          }}
          onBack={() => setView('home')}
        />
      );
    }
    return <HomePage onGetStarted={() => setView('auth')} />;
  }

  if (view === 'room' && activeRoom) {
    return <InterviewRoom user={session.user} token={session.token} room={activeRoom} onExit={() => { setActiveRoom(null); setView('dashboard'); refreshWorkspace(session.token); }} />;
  }

  if (view === 'results') {
    return (
      <ResultsView
        user={session.user}
        token={session.token}
        interview={selectedInterview || interviews[0] || null}
        interviews={interviews}
        onBack={() => setView('dashboard')}
        onSelectInterview={(interview) => setSelectedInterview(interview)}
        onInterviewUpdate={(updated) => {
          setSelectedInterview(updated);
          setInterviews((current) => current.map((i) => i.id === updated.id ? updated : i));
        }}
      />
    );
  }

  return (
    <DashboardView
      user={session.user}
      rooms={rooms}
      interviews={interviews}
      roomName={roomName}
      setRoomName={setRoomName}
      roomJobRole={roomJobRole}
      setRoomJobRole={setRoomJobRole}
      roomPosition={roomPosition}
      setRoomPosition={setRoomPosition}
      joinCode={joinCode}
      setJoinCode={setJoinCode}
      loading={loadingWorkspace}
      errorMessage={errorMessage}
      statusMessage={statusMessage}
      onCreateRoom={createRoom}
      onJoinRoom={joinRoom}
      onCloseRoom={closeRoom}
      onSelectInterview={(interview) => {
        setSelectedInterview(interview);
        setView('results');
      }}
      onSignOut={signOut}
    />
  );
}

export default App;