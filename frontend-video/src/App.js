import React, { useEffect, useRef, useState } from 'react';
import './App.css';

// --- ICONS ---
const Icons = {
  Mic: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>,
  MicOff: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="1" y1="1" x2="23" y2="23"/><path d="M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6"/><path d="M17 16.95A7 7 0 0 1 5 12v-2m14 0v2a7 7 0 0 1-.11 1.23"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>,
  Cam: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>,
  CamOff: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M16 16v1a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h2m5.66 0H14a2 2 0 0 1 2 2v3.34l1 1L23 7v10"/><line x1="1" y1="1" x2="23" y2="23"/></svg>,
  Phone: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10.68 13.31a16 16 0 0 0 6.93 6.93l2.28-2.28a2 2 0 0 1 2.57-.42 12.33 12.33 0 0 1 5.92 9.07 2 2 0 0 1-2 2A17 17 0 0 1 3 3a2 2 0 0 1 2-2 12.33 12.33 0 0 1 9.07 5.92 2 2 0 0 1-.42 2.57l-2.28 2.28z"/></svg>,
  Copy: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>,
  Back: () => <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>,
  Loader: () => <svg className="spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/></svg>
};

// Helper for dynamic score coloring
const getScoreColor = (score) => {
  if (score === undefined || score === null) return '#888';
  if (score >= 80) return '#238636'; // Success Green
  if (score >= 50) return '#9e6a03'; // Warning Orange
  return '#da3633'; // Danger Red
};

function App() {
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const droneRef = useRef(null);
  const pcRef = useRef(null);
  const localStreamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const [cameraOn, setCameraOn] = useState(true);
  const [micOn, setMicOn] = useState(true);
  const [callActive, setCallActive] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  
  // Data State
  const [recordings, setRecordings] = useState([]);
  const [activeReport, setActiveReport] = useState(null); 
  const [roomHash, setRoomHash] = useState('');

  // --- RECORDING LOGIC ---
  const startRecording = async (stream) => {
    if (!stream) return;
    try {
      audioChunksRef.current = [];
      const audioTracks = stream.getAudioTracks();
      if (audioTracks.length === 0) return;

      const audioStream = new MediaStream(audioTracks);
      const mimeTypes = ['audio/webm', 'audio/webm;codecs=opus', 'audio/mp4'];
      let selectedMimeType = mimeTypes.find(type => MediaRecorder.isTypeSupported(type));

      if (!selectedMimeType) return; 

      const mediaRecorder = new MediaRecorder(audioStream, {
        mimeType: selectedMimeType,
        audioBitsPerSecond: 128000
      });

      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        setIsProcessing(true);
        try {
          if (audioChunksRef.current.length === 0) throw new Error("No audio recorded");

          const audioBlob = new Blob(audioChunksRef.current, { type: selectedMimeType });
          const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
          const ext = selectedMimeType.split('/')[1].split(';')[0];
          const fileName = `interview-${timestamp}.${ext}`;

          const formData = new FormData();
          formData.append('audio', audioBlob, fileName);

          console.log('📤 Uploading audio for analysis...');
          const response = await fetch('http://localhost:3001/save-audio', {
            method: 'POST',
            body: formData
          });


          if (!response.ok) throw new Error('Server upload failed');

          const result = await response.json();
          console.log("SERVER RESPONSE:", result); // Debugging

          const audioUrl = URL.createObjectURL(audioBlob);

          // Create new recording object
          const newSession = {
            id: Date.now(),
            date: new Date(),
            url: audioUrl,
            name: fileName,
            serverPath: result.path,
            // Capture BOTH the raw pairs and the evaluation report
            evaluation: result.evaluation_report, 
            qa_pairs: result.qa_pairs || [],
            full_text: result.transcription
          };

          setRecordings(prev => [newSession, ...prev]); 
          setActiveReport(newSession); 

        } catch (error) {
          console.error('Processing failed:', error);
          alert('Could not process interview. Check console.');
        } finally {
          setIsProcessing(false);
        }
      };

      mediaRecorder.start(1000);
      setIsRecording(true);
    } catch (error) {
      console.error('MediaRecorder Error:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  // --- WEBRTC LOGIC ---
  useEffect(() => {
    if (!window.location.hash) {
      window.location.hash = Math.floor(Math.random() * 0xFFFFFF).toString(16);
    }
    const hash = window.location.hash.substring(1);
    setRoomHash(hash);

    const drone = new window.ScaleDrone('yiS12Ts5RdNhebyM');
    droneRef.current = drone;
    const roomName = 'observable-' + hash;
    const config = { iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] };
    let room, pc;

    drone.on('open', error => {
      if (error) return console.error(error);
      room = drone.subscribe(roomName);
      room.on('members', members => {
        const isOfferer = members.length === 2;
        startWebRTC(isOfferer);
      });
    });

    function sendMessage(message) { drone.publish({ room: roomName, message }); }

    function startWebRTC(isOfferer) {
      pc = new window.RTCPeerConnection(config);
      pcRef.current = pc;
      
      pc.onicecandidate = event => {
        if (event.candidate) sendMessage({ candidate: event.candidate });
      };

      if (isOfferer) {
        pc.onnegotiationneeded = () => {
          pc.createOffer().then(desc => {
            pc.setLocalDescription(desc, () => sendMessage({ sdp: pc.localDescription }), console.error);
          });
        };
      }

      pc.ontrack = event => {
        const stream = event.streams[0];
        if (remoteVideoRef.current) remoteVideoRef.current.srcObject = stream;
      };

      navigator.mediaDevices.getUserMedia({ audio: true, video: true })
        .then(stream => {
          localStreamRef.current = stream;
          if (localVideoRef.current) localVideoRef.current.srcObject = stream;
          stream.getTracks().forEach(track => pc.addTrack(track, stream));
          startRecording(stream); 
        }, console.error);

      room.on('data', (message, client) => {
        if (client.id === drone.clientId) return;
        if (message.sdp) {
          pc.setRemoteDescription(new window.RTCSessionDescription(message.sdp), () => {
            if (pc.remoteDescription.type === 'offer') {
              pc.createAnswer().then(desc => {
                pc.setLocalDescription(desc, () => sendMessage({ sdp: pc.localDescription }), console.error);
              });
            }
          }, console.error);
        } else if (message.candidate) {
          pc.addIceCandidate(new window.RTCIceCandidate(message.candidate));
        }
      });
    }

    return () => {
      stopRecording();
      if (pcRef.current) pcRef.current.close();
      if (droneRef.current) droneRef.current.close();
      if (localStreamRef.current) localStreamRef.current.getTracks().forEach(t => t.stop());
    };
  }, []);

  // --- HANDLERS ---
  const handleToggle = (type) => {
    if (!localStreamRef.current) return;
    const tracks = type === 'video' 
      ? localStreamRef.current.getVideoTracks() 
      : localStreamRef.current.getAudioTracks();
    
    tracks.forEach(t => t.enabled = !t.enabled);
    if (type === 'video') setCameraOn(!cameraOn);
    else setMicOn(!micOn);
  };

  const handleEndCall = () => {
    stopRecording();
    setCallActive(false);
    if (localStreamRef.current) localStreamRef.current.getTracks().forEach(t => t.stop());
  };

  const copyRoomID = () => {
    navigator.clipboard.writeText(window.location.href);
    alert("Link copied!");
  };

  // --- RENDER HELPERS ---
  
  if (isProcessing) return (
    <div className="loading-overlay">
      <div className="spinner"><Icons.Loader/></div>
      <h2>Analyzing Interview...</h2>
      <p>Generating technical scores and feedback.</p>
    </div>
  );

  // --- FULL SCREEN REPORT VIEW ---
  if (activeReport) {
    // 1. SELECT DATA SOURCE: 
    // If 'evaluation' exists (scores), use evaluation.results
    // If NOT, use 'qa_pairs' (just transcript)
    const hasEval = !!(activeReport.evaluation && activeReport.evaluation.results);
    const reportData = hasEval ? activeReport.evaluation.results : activeReport.qa_pairs;
    const totalScore = hasEval ? activeReport.evaluation.total_score : 0;

    return (
      <div className="app-container">
        <header className="top-bar">
          <button className="back-nav" onClick={() => setActiveReport(null)}>
            <Icons.Back /> Back to Dashboard
          </button>
          <div className="logo">Interview Analysis</div>
          <div style={{width: 40}}></div> 
        </header>

        <div className="report-view">
          <div className="report-content">
            
            {/* Report Header */}
            <div className="report-header">
              <div className="header-left">
                <h2>Session Report</h2>
                <p>Recorded on {activeReport.date.toLocaleDateString()} at {activeReport.date.toLocaleTimeString()}</p>
                <div style={{marginTop: '1rem'}}>
                    <a href={activeReport.url} download={activeReport.name} className="dl-btn">
                       Download Original Audio
                    </a>
                </div>
              </div>
              
              {hasEval && (
                <div className="score-badge" style={{borderColor: getScoreColor(totalScore)}}>
                  <div className="score-value" style={{color: getScoreColor(totalScore)}}>
                    {totalScore}
                  </div>
                  <div className="score-label">Technical Match</div>
                </div>
              )}
            </div>

            {/* Audio Player */}
            <div className="audio-section">
              <span>Playback:</span>
              <audio controls src={activeReport.url} />
            </div>

            {/* Q&A Grid */}
            <div className="qa-grid">
              {reportData.map((item, idx) => {
                
                // IMPORTANT: Handle data structure differences
                // The Evaluation API returns "candidate_answer"
                // The Raw Transcription API returns "answer"
                const answerText = item.candidate_answer || item.answer;
                const isGraded = !!item.difficulty; 

                return (
                  <div key={idx} className="qa-card" style={{borderTop: isGraded ? `4px solid ${getScoreColor(item.score)}` : 'none'}}>
                    
                    {/* Metadata Tags (Only shows if we have evaluation data) */}
                    {isGraded && (
                      <div className="qa-meta">
                        <div className="tags">
                          <span className="tag topic">{item.topic || 'General'}</span>
                          <span className="tag diff">{item.difficulty}</span>
                        </div>
                        <span className="item-score" style={{color: getScoreColor(item.score)}}>
                          {item.score}/100
                        </span>
                      </div>
                    )}

                    <div className="qa-body">
                      <div className="q-block">
                        <div className="icon-label icon-q">Q</div>
                        <div className="text-content"><strong>{item.question}</strong></div>
                      </div>
                      <div className="a-block">
                        <div className="icon-label icon-a">A</div>
                        <div className="text-content">{answerText}</div>
                      </div>
                      
                      {/* Feedback Block */}
                      {isGraded && item.feedback && (
                        <div className="feedback-box">
                          {item.feedback}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

          </div>
        </div>
      </div>
    );
  }

  // --- DASHBOARD VIEW ---
  return (
    <div className="app-container">
      <header className="top-bar">
        <div className="logo">Interview<span className="logo-bold">AI</span></div>
        <div className="room-id" onClick={copyRoomID}>
          <span>ID: {roomHash}</span>
          <Icons.Copy />
        </div>
        {isRecording && (
          <div className="recording-badge">
            <span className="pulse-dot"></span> LIVE
          </div>
        )}
      </header>

      {callActive ? (
        <>
          <main className="video-stage">
            <div className="video-grid">
              <div className="video-wrapper remote">
                <video ref={remoteVideoRef} autoPlay playsInline />
                <div className="video-label">Candidate</div>
              </div>
              <div className="video-wrapper local">
                <video ref={localVideoRef} autoPlay muted playsInline />
              </div>
            </div>
          </main>

          <footer className="controls-bar">
            <button className={`control-btn ${!micOn ? 'off' : ''}`} onClick={() => handleToggle('audio')}>
              {micOn ? <Icons.Mic /> : <Icons.MicOff />}
            </button>
            <button className={`control-btn ${!cameraOn ? 'off' : ''}`} onClick={() => handleToggle('video')}>
              {cameraOn ? <Icons.Cam /> : <Icons.CamOff />}
            </button>
            <button className="control-btn end-call" onClick={handleEndCall}>
              <Icons.Phone />
            </button>
          </footer>
        </>
      ) : (
        <div className="sessions-list-container">
          <h2>Interview History</h2>
          {recordings.length === 0 ? (
            <p style={{color: '#8b949e'}}>No interviews recorded yet.</p>
          ) : (
            recordings.map((rec) => (
              <div key={rec.id} className="session-item">
                <div>
                  <div style={{fontWeight: 'bold', fontSize: '1.1rem'}}>Interview Session</div>
                  <div style={{color: '#8b949e', fontSize: '0.9rem'}}>
                    {rec.date.toLocaleDateString()} at {rec.date.toLocaleTimeString()}
                  </div>
                </div>
                <button className="session-btn" onClick={() => setActiveReport(rec)}>
                  View Analysis
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default App;