import React, { useEffect, useRef, useState } from 'react';
import './App.css';

function App() {
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);
  const droneRef = useRef(null);
  const roomRef = useRef(null);
  const pcRef = useRef(null);
  const localStreamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const [cameraOn, setCameraOn] = useState(true);
  const [micOn, setMicOn] = useState(true);
  const [callActive, setCallActive] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [recordings, setRecordings] = useState([]);

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

  // Add recording handlers
  const startRecording = async () => {
    if (!localStreamRef.current) {
      alert('No audio stream available. Please make sure your microphone is connected and permissions are granted.');
      return;
    }

    try {
      audioChunksRef.current = [];
      
      // Get only the audio tracks from the stream
      const audioTracks = localStreamRef.current.getAudioTracks();
      if (audioTracks.length === 0) {
        alert('No audio tracks found. Please make sure your microphone is working.');
        return;
      }

      // Create a new stream with only audio tracks
      const audioStream = new MediaStream(audioTracks);
      
      // Check for supported MIME types
      const mimeTypes = [
        'audio/webm',
        'audio/webm;codecs=opus',
        'audio/ogg;codecs=opus',
        'audio/mp4',
        'audio/mpeg'
      ];

      let selectedMimeType = '';
      for (const mimeType of mimeTypes) {
        if (MediaRecorder.isTypeSupported(mimeType)) {
          selectedMimeType = mimeType;
          break;
        }
      }

      if (!selectedMimeType) {
        alert('Your browser does not support audio recording. Please try a different browser.');
        return;
      }

      console.log('Using MIME type:', selectedMimeType);

      const mediaRecorder = new MediaRecorder(audioStream, {
        mimeType: selectedMimeType,
        audioBitsPerSecond: 128000
      });

      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        try {
          if (audioChunksRef.current.length === 0) {
            alert('No audio data was recorded. Please try again.');
            return;
          }

          const audioBlob = new Blob(audioChunksRef.current, { type: selectedMimeType });
          const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
          const fileExtension = selectedMimeType.split('/')[1].split(';')[0];
          const fileName = `recording-${timestamp}.${fileExtension}`;

          // Create FormData to send to server
          const formData = new FormData();
          formData.append('audio', audioBlob, fileName);

          // Send to server
          const response = await fetch('http://localhost:3001/save-audio', {
            method: 'POST',
            body: formData
          });

          if (!response.ok) {
            throw new Error('Failed to save audio file');
          }

          const result = await response.json();
          console.log('Audio saved:', result);

          // Create URL for playback
          const audioUrl = URL.createObjectURL(audioBlob);
          
          // Save the recording in state
          setRecordings(prev => [...prev, { 
            url: audioUrl, 
            name: fileName, 
            blob: audioBlob,
            serverPath: result.path 
          }]);

          alert('Recording saved successfully!');
        } catch (error) {
          console.error('Error saving recording:', error);
          alert('Error saving recording. Please try again.');
        }
      };

      mediaRecorder.onerror = (event) => {
        console.error('MediaRecorder error:', event);
        alert('Error during recording. Please try again.');
        setIsRecording(false);
      };

      // Start recording with a 1-second timeslice
      mediaRecorder.start(1000);
      setIsRecording(true);
      console.log('Recording started successfully');
    } catch (error) {
      console.error('Error starting MediaRecorder:', error);
      alert('Error starting recording. Please make sure your microphone is working and try again.');
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      try {
        mediaRecorderRef.current.stop();
        setIsRecording(false);
        console.log('Recording stopped successfully');
      } catch (error) {
        console.error('Error stopping recording:', error);
        alert('Error stopping recording. Please try again.');
        setIsRecording(false);
      }
    }
  };

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
  const handleEndCall = async () => {
    if (isRecording) {
      stopRecording();
    }
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

    // Convert all audio files to text
    try {
      const response = await fetch('http://localhost:3001/convert-all-to-text', {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error('Failed to convert audio files');
      }

      const result = await response.json();
      console.log('Audio to text conversion completed:', result);
      alert('All audio recordings have been converted to text files!');
    } catch (error) {
      console.error('Error converting audio to text:', error);
      alert('Error converting audio to text. Please try again.');
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
        <button 
          onClick={isRecording ? stopRecording : startRecording} 
          disabled={!callActive}
          style={{ backgroundColor: isRecording ? '#ff4444' : '#4CAF50' }}
        >
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </button>
        <button onClick={handleEndCall} disabled={!callActive} style={{ color: 'red' }}>
          End Call
        </button>
      </div>
      <video ref={localVideoRef} autoPlay muted playsInline id="localVideo" style={{ display: callActive ? 'block' : 'none' }} />
      <video ref={remoteVideoRef} autoPlay playsInline id="remoteVideo" style={{ display: callActive ? 'block' : 'none' }} />
      
      {recordings.length > 0 && (
        <div className="recordings">
          <h3>Recordings</h3>
          <ul>
            {recordings.map((recording, index) => (
              <li key={index}>
                <audio controls src={recording.url} />
                <a href={recording.url} download={recording.name}>
                  Download {recording.name}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App; 