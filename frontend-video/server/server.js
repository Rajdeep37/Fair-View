const express = require('express');
const multer = require('multer');
const path = require('path');
const cors = require('cors');
const fs = require('fs');
const axios = require('axios');
const FormData = require('form-data');

const app = express();
const port = 3001;
// This points to your Python Transcription/Orchestrator API
const PYTHON_API_URL = 'http://127.0.0.1:8000/process-interview';

// Enable CORS
app.use(cors());

// Create audio directory if it doesn't exist
const audioDir = path.join(__dirname, '../../audio');
if (!fs.existsSync(audioDir)) {
    fs.mkdirSync(audioDir, { recursive: true });
}

// Configure multer for audio file storage
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, audioDir);
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname);
    }
});

const upload = multer({ storage: storage });

/**
 * Sends the audio file to the running Python FastAPI server (Port 8000)
 * and returns the processed Q&A + Evaluation JSON.
 */
async function getTranscriptionFromPython(filePath) {
    const form = new FormData();
    // Read file from disk and append to form
    form.append('file', fs.createReadStream(filePath));

    try {
        // Send POST request to Python API
        // This request now takes longer (up to 60s) because of the LLM step
        const response = await axios.post(PYTHON_API_URL, form, {
            headers: {
                ...form.getHeaders()
            },
            maxContentLength: Infinity,
            maxBodyLength: Infinity,
            timeout: 120000 // Set timeout to 2 minutes to be safe
        });

        return response.data;
    } catch (error) {
        console.error('Python API Error:', error.code || error.message);
        if (error.response) {
            console.error('API Response:', error.response.data);
        }
        throw new Error('Failed to communicate with Python analysis server');
    }
}

// Endpoint to save audio file and trigger analysis
app.post('/save-audio', upload.single('audio'), async (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No audio file received' });
    }

    const audioPath = req.file.path;
    console.log(`File uploaded: ${req.file.filename}. Sending to Python API...`);

    try {
        // 1. Send file to Python API (Port 8000)
        // This will now return { transcript, qa_pairs, evaluation_report }
        const apiResult = await getTranscriptionFromPython(audioPath);
        
        console.log("API RESULT RAW:", apiResult);
        console.log("API RESULT KEYS:", Object.keys(apiResult));
        
        // 2. Prepare data to save
        const resultData = {
            audioFile: req.file.filename,
            timestamp: new Date().toISOString(),
            status: apiResult.status,
            full_transcript: apiResult.full_transcript,
            qa_pairs: apiResult.qa_pairs,
            evaluation_report: apiResult.evaluation_report // <--- NEW DATA INCLUDED
        };

        // 3. Save the result as a JSON file next to the audio
        const jsonFileName = req.file.filename.replace(/\.[^/.]+$/, '.json');
        const jsonFilePath = path.join(audioDir, jsonFileName);
        
        fs.writeFileSync(jsonFilePath, JSON.stringify(resultData, null, 2));
        console.log(`Analysis and Evaluation saved to ${jsonFileName}`);

        // 4. Send response back to Frontend
        res.json({ 
            message: 'Interview processed successfully',
            filename: req.file.filename,
            jsonFilename: jsonFileName,
            path: req.file.path,
            transcription: apiResult.full_transcript,
            qa_pairs: apiResult.qa_pairs,
            evaluation_report: apiResult.evaluation_report // <--- SEND GRADES TO FRONTEND
        });

    } catch (error) {
        console.error('Error during processing:', error.message);
        res.status(500).json({ 
            message: 'Audio saved, but analysis failed. Is the Python server running?', 
            error: error.message 
        });
    }
});

app.listen(port, () => {
    console.log(`Node Server running at http://localhost:${port}`);
    console.log(`Make sure Python API is running at ${PYTHON_API_URL}`);
});