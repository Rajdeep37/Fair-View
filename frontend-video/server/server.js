const express = require('express');
const multer = require('multer');
const path = require('path');
const cors = require('cors');
const fs = require('fs');
const { spawn } = require('child_process');

const app = express();
const port = 3001;

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

// Function to convert audio to text
function convertAudioToText(audioFile) {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', [
            path.join(__dirname, '../../python/audioToText.py'),
            audioFile
        ]);

        let output = '';
        let error = '';

        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            error += data.toString();
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                console.error(`Python process error for ${audioFile}:`, error);
                reject(new Error(`Failed to convert ${path.basename(audioFile)}: ${error}`));
            } else {
                resolve(output.trim());
            }
        });
    });
}

// Endpoint to save audio file
app.post('/save-audio', upload.single('audio'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No audio file received' });
    }
    res.json({ 
        message: 'Audio file saved successfully',
        filename: req.file.filename,
        path: req.file.path
    });
});

// Endpoint to convert all audio files to text
app.post('/convert-all-to-text', async (req, res) => {
    try {
        const files = fs.readdirSync(audioDir);
        const audioFiles = files.filter(file => 
            file.endsWith('.webm') || file.endsWith('.mp3') || file.endsWith('.wav')
        );

        if (audioFiles.length === 0) {
            return res.json({ 
                message: 'No audio files found to convert',
                results: []
            });
        }

        const results = [];
        for (const file of audioFiles) {
            const filePath = path.join(audioDir, file);
            try {
                console.log(`Converting ${file} to text...`);
                const text = await convertAudioToText(filePath);
                const textFileName = file.replace(/\.[^/.]+$/, '.txt');
                const textFilePath = path.join(audioDir, textFileName);
                
                fs.writeFileSync(textFilePath, text);
                results.push({
                    audioFile: file,
                    textFile: textFileName,
                    text: text
                });
                console.log(`Successfully converted ${file} to text`);
            } catch (error) {
                console.error(`Error converting ${file}:`, error);
                results.push({
                    audioFile: file,
                    error: error.message
                });
            }
        }

        res.json({ 
            message: 'Conversion completed',
            results: results
        });
    } catch (error) {
        console.error('Error in conversion process:', error);
        res.status(500).json({ error: 'Error converting audio files' });
    }
});

// Endpoint to get list of audio files
app.get('/audio-files', (req, res) => {
    fs.readdir(audioDir, (err, files) => {
        if (err) {
            return res.status(500).json({ error: 'Error reading audio directory' });
        }
        res.json({ files });
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
}); 