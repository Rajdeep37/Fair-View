import React, { useEffect, useRef, useState } from 'react';
import './App.css';

function App() {
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const droneRef = useRef(null);
  const roomRef = useRef(null);
  const pcRef = useRef(null);
  const localStreamRef = useRef(null);

  const [cameraOn, setCameraOn] = useState(true);
  const [micOn, setMicOn] = useState(true);
  const [callActive, setCallActive] = useState(true);

  useEffect(() => {
    // Generate random room name if needed
    if (!window.location.hash) {
      window.location.hash = Math.floor(Math.random() * 0xFFFFFF).toString(16);
    }
    const roomHash = window.location.hash.substring(1);
    // TODO: Replace with your own channel ID
    const drone = new window.ScaleDrone('yiS12Ts5RdNhebyM');
    droneRef.current = drone;
    const roomName = 'observable-' + roomHash;
    const configuration = {
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    };
    let room, pc;

    function onSuccess() {}
    function onError(error) { console.error(error); }

    drone.on('open', error => {
      if (error) {
        return console.error(error);
      }
      room = drone.subscribe(roomName);
      roomRef.current = room;
      room.on('open', error => {
        if (error) onError(error);
      });
      room.on('members', members => {
        const isOfferer = members.length === 2;
        startWebRTC(isOfferer);
      });
    });

    function sendMessage(message) {
      drone.publish({ room: roomName, message });
    }

    function startWebRTC(isOfferer) {
      pc = new window.RTCPeerConnection(configuration);
      pcRef.current = pc;
      pc.onicecandidate = event => {
        if (event.candidate) {
          sendMessage({ candidate: event.candidate });
        }
      };
      if (isOfferer) {
        pc.onnegotiationneeded = () => {
          pc.createOffer().then(localDescCreated).catch(onError);
        };
      }
      pc.ontrack = event => {
        const stream = event.streams[0];
        if (!remoteVideoRef.current.srcObject || remoteVideoRef.current.srcObject.id !== stream.id) {
          remoteVideoRef.current.srcObject = stream;
        }
      };
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Your browser does not support WebRTC. Please use a modern browser like Chrome or Firefox.');
        return;
      }
      navigator.mediaDevices.getUserMedia({ audio: true, video: true })
        .then(stream => {
          localStreamRef.current = stream;
          localVideoRef.current.srcObject = stream;
          stream.getTracks().forEach(track => pc.addTrack(track, stream));
        }, onError);
      room.on('data', (message, client) => {
        if (client.id === drone.clientId) return;
        if (message.sdp) {
          pc.setRemoteDescription(new window.RTCSessionDescription(message.sdp), () => {
            if (pc.remoteDescription.type === 'offer') {
              pc.createAnswer().then(localDescCreated).catch(onError);
            }
          }, onError);
        } else if (message.candidate) {
          pc.addIceCandidate(new window.RTCIceCandidate(message.candidate), onSuccess, onError);
        }
      });
    }

    function localDescCreated(desc) {
      pc.setLocalDescription(desc, () => sendMessage({ sdp: pc.localDescription }), onError);
    }

    // Cleanup on unmount
    return () => {
      if (pcRef.current) {
        pcRef.current.close();
      }
      if (droneRef.current) {
        droneRef.current.close();
      }
      if (localStreamRef.current) {
        localStreamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  // Camera toggle handler
  const handleCameraToggle = () => {
    if (localStreamRef.current) {
      localStreamRef.current.getVideoTracks().forEach(track => {
        track.enabled = !cameraOn;
      });
      setCameraOn(v => !v);
    }
  };

  // Mic toggle handler
  const handleMicToggle = () => {
    if (localStreamRef.current) {
      localStreamRef.current.getAudioTracks().forEach(track => {
        track.enabled = !micOn;
      });
      setMicOn(m => !m);
    }
  };

  // End call handler
  const handleEndCall = () => {
    setCallActive(false);
    if (pcRef.current) {
      pcRef.current.close();
      pcRef.current = null;
    }
    if (droneRef.current) {
      droneRef.current.close();
      droneRef.current = null;
    }
    if (localStreamRef.current) {
      localStreamRef.current.getTracks().forEach(track => track.stop());
      localStreamRef.current = null;
    }
    if (localVideoRef.current) {
      localVideoRef.current.srcObject = null;
    }
    if (remoteVideoRef.current) {
      remoteVideoRef.current.srcObject = null;
    }
  };

  return (
    <div className="App">
      <div className="copy">Send your URL to a friend to start a video call</div>
      <div className="controls">
        <button onClick={handleCameraToggle} disabled={!callActive}>
          {cameraOn ? 'Turn Camera Off' : 'Turn Camera On'}
        </button>
        <button onClick={handleMicToggle} disabled={!callActive}>
          {micOn ? 'Mute Mic' : 'Unmute Mic'}
        </button>
        <button onClick={handleEndCall} disabled={!callActive} style={{ color: 'red' }}>
          End Call
        </button>
      </div>
      <video ref={localVideoRef} autoPlay muted playsInline id="localVideo" style={{ display: callActive ? 'block' : 'none' }} />
      <video ref={remoteVideoRef} autoPlay playsInline id="remoteVideo" style={{ display: callActive ? 'block' : 'none' }} />
    </div>
  );
}

export default App;
