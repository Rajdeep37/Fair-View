# Fair View - Interview Platform

Fair View is a role-based interview platform built with React, WebRTC, FastAPI, and SQLite. Interviewers can create rooms, candidates can join with a shared room code, and interview evaluations are stored in the database for both participants to review later.

## Features

- Sign up and sign in with interviewer or candidate roles
- Create and join interview rooms with shared room codes
- Record interview audio and send it through the evaluation pipeline
- Persist users, rooms, and interview results in SQLite
- Review scores, feedback, and transcripts after the session

## Prerequisites

- Node.js (v14 or higher)
- Python 3.10+ with the dependencies in `python/requirements.txt`
- Modern web browser with WebRTC support (Chrome, Firefox, Edge)
- Camera and microphone access

## Quick Start

1. Install the frontend dependencies:
   ```bash
   cd frontend-video
   npm install
   ```

2. Install the Python dependencies:
   ```bash
   cd python
   pip install -r requirements.txt
   ```

3. Seed the question bank and create the database schema:
   ```bash
   python init_db.py
   ```

4. Start the Python API:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

5. Start the Node audio bridge:
   ```bash
   cd ../frontend-video/server
   npm start
   ```

6. Start the React frontend:
   ```bash
   cd ..
   npm start
   ```

## Usage

1. Create an account as an interviewer or candidate.
2. Interviewers create rooms and share the room code.
3. Candidates join the room with the shared code.
4. End the call to save the recording, generate scores, and persist the interview result.
5. Open the results page from the dashboard to review scoring history.

## Security

- Authentication uses JWT tokens issued by the FastAPI backend
- Passwords are hashed before being stored in the database
- Interview results persist in SQLite so history survives refreshes
- Local development still depends on the ScaleDrone signaling service for WebRTC

## Development

- Built with React 19.1.0
- Uses WebRTC for peer-to-peer communication
- ScaleDrone for signaling
- FastAPI handles authentication, room management, and result persistence

## Troubleshooting

If you encounter issues:
1. Ensure both devices are on the same network
2. Check browser console for any errors
3. Verify camera and microphone permissions
4. Make sure your firewall allows connections on port 3000

## License

MIT License
