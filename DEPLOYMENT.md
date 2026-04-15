# Fair-View Deployment Plan (Free / Minimal Cost)

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│  React Frontend  │────▶│  Node Audio Bridge   │────▶│  Python FastAPI       │
│  (Vercel - Free) │     │  (Render - Free)     │     │  (Render - Free)     │
│  Static Build    │     │  Express + Multer    │     │  SQLite + Gemini     │
└─────────────────┘     └──────────────────────┘     └──────────────────────┘
        │                                                      │
        ▼                                                      ▼
  ScaleDrone (Free)                                   Gemini API (Free Tier)
  WebRTC Signaling                                    AI Evaluation
```

**Total Monthly Cost: $0**

---

## Services & Free Tiers Used

| Component            | Platform       | Free Tier Limits                          |
|----------------------|----------------|-------------------------------------------|
| React Frontend       | **Vercel**     | Unlimited static deploys, 100GB bandwidth |
| Node Audio Bridge    | **Render**     | 750 hrs/month, spins down after 15min idle|
| Python FastAPI       | **Render**     | 750 hrs/month, spins down after 15min idle|
| WebRTC Signaling     | **ScaleDrone** | Already configured, free tier sufficient  |
| AI/LLM              | **Gemini API** | Free tier: 15 RPM, 1M tokens/day         |
| Database             | **SQLite**     | Bundled with Python service (ephemeral)   |

> **Note:** Render free services spin down after 15 minutes of inactivity. First request after idle takes ~30-60 seconds (cold start). This is acceptable for a portfolio project.

---

## Step-by-Step Deployment

### Prerequisites

- GitHub account (push Fair-View repo to GitHub)
- Vercel account (sign up free with GitHub)
- Render account (sign up free with GitHub)
- Your existing Gemini API key and ScaleDrone channel ID

---

### Step 1: Push Code to GitHub

```bash
cd c:\projects\Fair-View
git init   # if not already
git add .
git commit -m "Prepare for deployment"
git remote add origin https://github.com/<your-username>/Fair-View.git
git push -u origin main
```

---

### Step 2: Deploy Python FastAPI Backend on Render

1. Go to [render.com](https://render.com) → **New** → **Web Service**
2. Connect your GitHub repo
3. Configure:

| Setting           | Value                                         |
|-------------------|-----------------------------------------------|
| **Name**          | `fair-view-api`                               |
| **Root Directory**| `python`                                      |
| **Runtime**       | `Python 3`                                    |
| **Build Command** | `pip install -r requirements.txt`             |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free`                                        |

4. Add **Environment Variables**:

| Key                        | Value                             |
|----------------------------|-----------------------------------|
| `GEMINI_API_KEY`           | `your-actual-gemini-key`          |
| `JWT_SECRET_KEY`           | `generate-a-random-64-char-string`|
| `ALLOWED_ORIGINS`          | `https://fair-view.vercel.app,https://fair-view-audio.onrender.com` |
| `DATABASE_URL`             | `sqlite:///./fair_view.db`        |
| `AUDIO_DIR`                | `./audio`                         |

5. Click **Create Web Service** → note the URL (e.g. `https://fair-view-api.onrender.com`)

---

### Step 3: Deploy Node Audio Bridge on Render

1. Go to Render → **New** → **Web Service**
2. Connect **same** GitHub repo
3. Configure:

| Setting           | Value                                              |
|-------------------|----------------------------------------------------|
| **Name**          | `fair-view-audio`                                  |
| **Root Directory**| `frontend-video/server`                            |
| **Runtime**       | `Node`                                             |
| **Build Command** | `npm install`                                      |
| **Start Command** | `node server.js`                                   |
| **Instance Type** | `Free`                                             |

4. Add **Environment Variables**:

| Key               | Value                                                              |
|-------------------|--------------------------------------------------------------------|
| `PORT`            | `3001`                                                             |
| `PYTHON_API_URL`  | `https://fair-view-api.onrender.com/process-interview`             |
| `ALLOWED_ORIGINS` | `https://fair-view.vercel.app`                                     |

5. Click **Create Web Service** → note the URL (e.g. `https://fair-view-audio.onrender.com`)

---

### Step 4: Deploy React Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project** → Import your GitHub repo
2. Configure:

| Setting              | Value                    |
|----------------------|--------------------------|
| **Framework Preset** | `Create React App`       |
| **Root Directory**   | `frontend-video`         |
| **Build Command**    | `npm run build`          |
| **Output Directory** | `build`                  |

3. Add **Environment Variables**:

| Key                         | Value                                              |
|-----------------------------|----------------------------------------------------|
| `REACT_APP_API_URL`         | `https://fair-view-api.onrender.com`               |
| `REACT_APP_UPLOAD_URL`      | `https://fair-view-audio.onrender.com/save-audio`  |
| `REACT_APP_SCALEDRONE_ID`   | `your-scaledrone-channel-id`                        |

4. Click **Deploy** → your site is live at `https://fair-view.vercel.app` (or custom name)

---

### Step 5: Update CORS After All Services Are Live

Go back to the **Render dashboard** for `fair-view-api` and update:

```
ALLOWED_ORIGINS=https://fair-view.vercel.app,https://fair-view-audio.onrender.com
```

Replace `fair-view.vercel.app` with your actual Vercel domain.

---

## Code Changes Required Before Deploying

### 1. Add `render.yaml` (optional - Infrastructure as Code)

Create a `render.yaml` at the repo root for one-click deploy:

```yaml
services:
  - type: web
    name: fair-view-api
    runtime: python
    rootDir: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app:app --host 0.0.0.0 --port $PORT
    plan: free
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: JWT_SECRET_KEY
        sync: false
      - key: ALLOWED_ORIGINS
        sync: false
      - key: DATABASE_URL
        value: sqlite:///./fair_view.db

  - type: web
    name: fair-view-audio
    runtime: node
    rootDir: frontend-video/server
    buildCommand: npm install
    startCommand: node server.js
    plan: free
    envVars:
      - key: PYTHON_API_URL
        sync: false
```

### 2. Audio directory path fix for Node server

The Node server currently saves audio to `../../audio` (relative path going two levels up). On Render, this may fail. Update `server.js` to use a local directory:

```js
// Change from:
const audioDir = path.join(__dirname, '../../audio');
// Change to:
const audioDir = path.join(__dirname, 'audio');
```

### 3. Ensure Python audio directory is created

The Python app already reads `AUDIO_DIR` from env. Just make sure the directory is created on startup. Check that `app.py` handles this (it likely does in the lifespan handler or file upload logic).

---

## Post-Deployment Checklist

- [ ] Python API health: visit `https://fair-view-api.onrender.com/docs` (FastAPI auto-docs)
- [ ] Node bridge health: visit `https://fair-view-audio.onrender.com/`
- [ ] Frontend loads: visit `https://fair-view.vercel.app`
- [ ] Sign up works (creates user in SQLite)
- [ ] Create room → join room → video call connects via ScaleDrone
- [ ] Audio recording uploads and evaluates via Gemini
- [ ] CORS errors: check `ALLOWED_ORIGINS` includes your Vercel domain

---

## Known Limitations (Free Tier)

| Limitation                    | Impact                                           | Mitigation                          |
|-------------------------------|--------------------------------------------------|-------------------------------------|
| Render cold starts (~30-60s)  | First request after 15min idle is slow           | Add a note on the site / README     |
| SQLite is ephemeral           | Data resets on each Render redeploy              | Acceptable for demo; or use Turso (free SQLite cloud) |
| No persistent file storage    | Uploaded audio files lost on redeploy            | Fine for demo purposes              |
| 750 free hours/month on Render| Shared across both services                      | Plenty for a portfolio project      |
| Gemini free tier rate limits  | 15 requests/min, 1M tokens/day                   | More than enough for demos          |

---

## Optional: Custom Domain (Free)

1. Buy a free `.is-a.dev` or similar free subdomain
2. Or just use Vercel's default `*.vercel.app` domain — looks professional enough for a resume

---

## Optional: Keep Services Warm (Prevent Cold Starts)

Use [UptimeRobot](https://uptimerobot.com) (free, 50 monitors) to ping your Render services every 14 minutes:

1. Sign up at uptimerobot.com
2. Add HTTP monitors for:
   - `https://fair-view-api.onrender.com/docs`
   - `https://fair-view-audio.onrender.com/`
3. Set check interval to **every 14 minutes** (keeps services from sleeping, but be aware this uses your 750 free hours faster — roughly 540 hrs/month for both services, still within limit)

---

## Resume Description Example

> **Fair-View** — AI-Powered Interview Platform  
> Full-stack application enabling real-time video interviews with AI-driven candidate evaluation. Built with React, Node.js, FastAPI, and Google Gemini. Features WebRTC video calls, dual-participant audio recording, automated transcript merging, and per-question competency scoring.  
> **Live:** [fair-view.vercel.app](https://fair-view.vercel.app)  
> **GitHub:** [github.com/username/Fair-View](https://github.com/username/Fair-View)
