import React, { useEffect, useRef, useState } from 'react';
import { Icons } from './Icons';
import { SCALEDRONE_ID, UPLOAD_BASE } from './config';

export function InterviewRoom({ user, token, room, onExit }) {
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const droneRef = useRef(null);
  const pcRef = useRef(null);
  const localStreamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const shouldEvaluateRef = useRef(false);

  const isInterviewer = user.role === 'interviewer';

  const [cameraOn, setCameraOn] = useState(true);
  const [micOn, setMicOn] = useState(true);
  const [callActive, setCallActive] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showEndPrompt, setShowEndPrompt] = useState(false);
  const [callEndedByInterviewer, setCallEndedByInterviewer] = useState(false);
  const [roomError, setRoomError] = useState('');
  const [copied, setCopied] = useState(false);
  const onExitRef = useRef(onExit);

  useEffect(() => { onExitRef.current = onExit; }, [onExit]);

  useEffect(() => {
    let mounted = true;
    const roomName = `observable-${room.code}`;
    const config = { iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] };
    const drone = new window.ScaleDrone(SCALEDRONE_ID);
    droneRef.current = drone;
    let roomChannel = null;
    let peerConnection = null;

    const stopRecording = () => {
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
    };

    const cleanup = () => {
      stopRecording();
      if (peerConnection) peerConnection.close();
      if (droneRef.current) droneRef.current.close();
      if (localStreamRef.current) localStreamRef.current.getTracks().forEach((t) => t.stop());
    };

    const uploadAndPersist = async (audioBlob, mimeType, evaluate) => {
      setIsProcessing(true);
      try {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const extension = mimeType.split('/')[1].split(';')[0];
        const fileName = `interview-${timestamp}.${extension}`;
        const formData = new FormData();
        formData.append('audio', audioBlob, fileName);
        formData.append('room_id', room.code);
        formData.append('evaluate', evaluate ? 'true' : 'false');

        const response = await fetch(UPLOAD_BASE, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
          body: formData,
        });

        const payload = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(payload.error || payload.message || 'Failed to upload interview audio');

        if (payload.status === 'pending_merge') {
          // First to upload — go back to dashboard; ResultsView will poll
          onExitRef.current();
        } else {
          // Second to upload — merge already happened, go back to dashboard
          onExitRef.current();
        }
      } catch (error) {
        setRoomError(error.message);
        setIsProcessing(false);
      }
    };

    const startRecording = async (stream) => {
      if (!stream || !mounted) return;
      audioChunksRef.current = [];
      const audioTracks = stream.getAudioTracks();
      if (audioTracks.length === 0) return;

      const audioStream = new MediaStream(audioTracks);
      const mimeTypes = ['audio/webm', 'audio/webm;codecs=opus', 'audio/mp4'];
      const selectedMimeType = mimeTypes.find((t) => window.MediaRecorder.isTypeSupported(t));
      if (!selectedMimeType) return;

      const mediaRecorder = new MediaRecorder(audioStream, { mimeType: selectedMimeType, audioBitsPerSecond: 128000 });
      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.ondataavailable = (e) => { if (e.data.size > 0) audioChunksRef.current.push(e.data); };
      mediaRecorder.onstop = async () => {
        if (!audioChunksRef.current.length) return;
        const audioBlob = new Blob(audioChunksRef.current, { type: selectedMimeType });
        if (shouldEvaluateRef.current) {
          await uploadAndPersist(audioBlob, selectedMimeType, true);
        } else {
          // No evaluation — just exit cleanly
          onExitRef.current();
        }
      };
      mediaRecorder.start(1000);
    };

    let pendingCandidates = [];

    const drainCandidates = () => {
      if (!peerConnection || !peerConnection.remoteDescription) return;
      pendingCandidates.forEach((c) => peerConnection.addIceCandidate(new window.RTCIceCandidate(c)));
      pendingCandidates = [];
    };

    const startPeerConnection = (isOfferer) => {
      peerConnection = new window.RTCPeerConnection(config);
      pcRef.current = peerConnection;

      peerConnection.onicecandidate = (e) => {
        if (e.candidate) drone.publish({ room: roomName, message: { candidate: e.candidate } });
      };

      if (isOfferer) {
        peerConnection.onnegotiationneeded = () => {
          peerConnection.createOffer().then((desc) => {
            peerConnection.setLocalDescription(desc, () => {
              drone.publish({ room: roomName, message: { sdp: peerConnection.localDescription } });
            });
          });
        };
      }

      peerConnection.ontrack = (e) => {
        if (remoteVideoRef.current) remoteVideoRef.current.srcObject = e.streams[0];
      };

      navigator.mediaDevices
        .getUserMedia({ audio: true, video: true })
        .then((stream) => {
          if (!mounted) return;
          localStreamRef.current = stream;
          if (localVideoRef.current) localVideoRef.current.srcObject = stream;
          stream.getTracks().forEach((t) => peerConnection.addTrack(t, stream));
          startRecording(stream);
        })
        .catch(() => setRoomError('Camera and microphone access is required.'));
    };

    drone.on('open', (error) => {
      if (error) { setRoomError('Could not connect to the signaling service.'); return; }

      roomChannel = drone.subscribe(roomName);
      roomChannel.on('members', (members) => {
        if (!mounted) return;
        startPeerConnection(members.length === 2);
      });

      roomChannel.on('data', (message, client) => {
        if (client.id === drone.clientId) return;

        // Handle end-call signal from the interviewer
        if (message.type === 'end-call') {
          if (!mounted) return;
          shouldEvaluateRef.current = !!message.evaluate;
          setCallEndedByInterviewer(true);
          setCallActive(false);
          // Stop recording — onstop will check shouldEvaluateRef
          if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
            mediaRecorderRef.current.stop();
          }
          if (localStreamRef.current) {
            localStreamRef.current.getTracks().forEach((t) => t.stop());
          }
          return;
        }

        if (!peerConnection) return;
        if (message.sdp) {
          peerConnection.setRemoteDescription(new window.RTCSessionDescription(message.sdp), () => {
            drainCandidates();
            if (peerConnection.remoteDescription.type === 'offer') {
              peerConnection.createAnswer().then((desc) => {
                peerConnection.setLocalDescription(desc, () => {
                  drone.publish({ room: roomName, message: { sdp: peerConnection.localDescription } });
                });
              });
            }
          });
        } else if (message.candidate) {
          if (peerConnection.remoteDescription) {
            peerConnection.addIceCandidate(new window.RTCIceCandidate(message.candidate));
          } else {
            pendingCandidates.push(message.candidate);
          }
        }
      });
    });

    return () => {
      mounted = false;
      cleanup();
    };
  }, [room.code, room.id, room.name, token]);

  // Interviewer clicks "End call" → show the evaluate prompt
  const handleEndClick = () => {
    setShowEndPrompt(true);
  };

  // Interviewer picks Yes or No on the prompt
  const handleEndDecision = (evaluate) => {
    setShowEndPrompt(false);
    shouldEvaluateRef.current = evaluate;
    setCallActive(false);

    // Signal the candidate via ScaleDrone
    const roomName = `observable-${room.code}`;
    if (droneRef.current) {
      droneRef.current.publish({ room: roomName, message: { type: 'end-call', evaluate } });
    }

    // Stop own recording — onstop handler will upload or exit
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    if (localStreamRef.current) {
      localStreamRef.current.getTracks().forEach((t) => t.stop());
    }
  };

  const toggleTrack = (type) => {
    if (!localStreamRef.current) return;
    const tracks = type === 'video' ? localStreamRef.current.getVideoTracks() : localStreamRef.current.getAudioTracks();
    tracks.forEach((t) => { t.enabled = !t.enabled; });
    if (type === 'video') setCameraOn((v) => !v); else setMicOn((v) => !v);
  };

  const copyRoomCode = async () => {
    await navigator.clipboard.writeText(room.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="room-shell">
      <header className="room-topbar">
        {isInterviewer && <button className="ghost-btn compact back-btn" onClick={onExit}><Icons.Arrow /> Exit</button>}
        <div className="room-identity">
          <div className="eyebrow">Live session</div>
          <h1>{room.name}</h1>
        </div>
        <button className={`room-code ${copied ? 'copied' : ''}`} onClick={copyRoomCode}>
          <span>{room.code}</span>
          {copied ? <Icons.Check /> : <Icons.Copy />}
        </button>
      </header>

      {roomError && <div className="notice error room-notice">{roomError}</div>}

      <main className="room-stage">
        <div className="video-grid">
          <div className="video-card remote">
            <video ref={remoteVideoRef} autoPlay playsInline />
            <div className="video-label">Remote</div>
          </div>
          <div className="video-card local">
            <video ref={localVideoRef} autoPlay muted playsInline />
            <div className="video-label">You</div>
          </div>
        </div>
      </main>

      <footer className="room-controls">
        <button className={`control-btn ${!micOn ? 'off' : ''}`} onClick={() => toggleTrack('audio')} title={micOn ? 'Mute' : 'Unmute'}>
          {micOn ? <Icons.Mic /> : <Icons.MicOff />}
        </button>
        <button className={`control-btn ${!cameraOn ? 'off' : ''}`} onClick={() => toggleTrack('video')} title={cameraOn ? 'Camera off' : 'Camera on'}>
          {cameraOn ? <Icons.Cam /> : <Icons.CamOff />}
        </button>
        {isInterviewer && (
          <button className="control-btn end-call" onClick={handleEndClick} title="End interview">
            <Icons.Door />
          </button>
        )}
      </footer>

      {showEndPrompt && (
        <div className="loading-overlay">
          <div className="loading-panel end-prompt">
            <h2>End interview</h2>
            <p>Would you like to evaluate this interview?</p>
            <div className="prompt-actions">
              <button className="btn primary" onClick={() => handleEndDecision(true)}>Yes, evaluate</button>
              <button className="btn ghost" onClick={() => handleEndDecision(false)}>No, just end</button>
            </div>
          </div>
        </div>
      )}

      {!showEndPrompt && (isProcessing || callEndedByInterviewer || !callActive) && (
        <div className="loading-overlay">
          <div className="loading-panel">
            <Icons.Loader />
            <h2>
              {callEndedByInterviewer && !isProcessing ? 'Interview ended'
                : isProcessing ? 'Uploading recording…'
                : 'Session ended'}
            </h2>
            <p>
              {callEndedByInterviewer && !isProcessing ? 'The interviewer has ended the session.'
                : isProcessing ? 'Your recording is being uploaded.'
                : 'Wrapping up…'}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
