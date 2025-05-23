# Fair View - WebRTC Video Chat Application

A secure, peer-to-peer video chat application built with React and WebRTC. This application allows users to establish direct video calls through their web browsers without the need for any plugins or additional software.

## Features

- Real-time peer-to-peer video and audio communication
- Secure HTTPS connections
- No server-side video/audio processing
- Works across different devices and networks
- Simple and intuitive user interface

## Prerequisites

- Node.js (v14 or higher)
- Modern web browser with WebRTC support (Chrome, Firefox, Edge)
- Camera and microphone access

## Quick Start

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Access the application:
   - Local: https://localhost:3000
   - Network: https://YOUR_IP_ADDRESS:3000

## Usage

1. Open the application in your browser
2. Allow camera and microphone access when prompted
3. Share the URL with another person to start a video call
4. The connection will be established automatically when both parties are present

## Security

- All video/audio data is transmitted directly between peers
- HTTPS encryption for secure signaling
- No video/audio data is stored on any server
- Local development uses self-signed certificates (accept the security warning in your browser)

## Development

- Built with React 19.1.0
- Uses WebRTC for peer-to-peer communication
- ScaleDrone for signaling server
- Development server runs on HTTPS for better WebRTC support

## Troubleshooting

If you encounter issues:
1. Ensure both devices are on the same network
2. Check browser console for any errors
3. Verify camera and microphone permissions
4. Make sure your firewall allows connections on port 3000

## License

MIT License
