# CrimeVision AI

Intelligent Multimodal Forensic Analysis Platform

CrimeVision AI is an AI-powered forensic analysis and decision-support platform that processes images, videos, audio recordings, and natural-language queries using computer vision, speech recognition, and large language models.

## ⚠️ Important Disclaimer

**This is a prototype for investigative decision support. Model outputs are preliminary analytical findings, not established facts.**

- Never automatically declare a person guilty or identify a suspect solely from visual appearance
- Distinguish observed evidence from model-generated interpretations and hypotheses
- Never fabricate evidence, timestamps, quotations, confidence scores, or citations
- Record uncertainty and conflicting evidence explicitly
- Keep human investigators responsible for conclusions and decisions
- This system must be validated before operational forensic use

## Technology Stack

### Backend
- Python 3.9+
- Flask (REST API)
- SQLAlchemy (Database)
- SQLite (Local development)
- PyTorch (Model inference)
- OpenCV (Image/video processing)
- Faster-Whisper (Audio transcription)
- Groq API (LLM reasoning)
- ReportLab (PDF generation)

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Lucide React (Icons)
- React Router (Navigation)
- Axios (API communication)
- Recharts (Analytics)
- Three.js / React Three Fiber (3D visualization)

## Project Structure

```
crimevision-ai/
├── backend/
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── ai/             # AI model adapters
│   │   └── utils/          # Utilities
│   ├── storage/            # Evidence and reports
│   ├── tests/              # Automated tests
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── types/          # TypeScript types
│   ├── package.json
│   └── vite.config.ts
├── docs/                   # Documentation
├── .gitignore
└── README.md
```

## Setup Instructions (Windows)

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- PowerShell

### Backend Setup

1. Navigate to the backend directory:
```powershell
cd backend
```

2. Create a Python virtual environment:
```powershell
python -m venv .venv
```

3. Activate the virtual environment:
```powershell
.venv\Scripts\Activate.ps1
```

**Note:** If you encounter a PowerShell execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Then try activation again.

4. Upgrade pip:
```powershell
python -m pip install --upgrade pip
```

5. Install dependencies:
```powershell
pip install -r requirements.txt
```

6. Create environment configuration:
```powershell
Copy .env.example .env
```

7. Edit `.env` and configure your settings (optional for initial setup):
```env
GROQ_API_KEY=your_api_key_here
```

8. Start the backend server:
```powershell
python run.py
```

The backend will start on `http://127.0.0.1:5000`

### Frontend Setup

1. Open a new PowerShell terminal and navigate to the frontend directory:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Create environment configuration:
```powershell
Copy .env.example .env
```

4. Start the development server:
```powershell
npm run dev
```

The frontend will start on `http://localhost:5173`

### Verify Installation

1. Check backend health:
```powershell
curl http://127.0.0.1:5000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "CrimeVision AI Backend",
  "version": "0.1.0",
  "environment": "development"
}
```

2. Open your browser and navigate to `http://localhost:5173` to see the frontend dashboard.

## Features

### Overview Dashboard
- Evidence statistics
- Recent activity
- Quick actions

### Evidence Vault
- Upload images, videos, and audio
- File validation and hashing
- Evidence metadata management

### Image Analysis
- Object detection
- Scene captioning
- Bounding box visualization
- Confidence filtering

### Video Analysis
- Frame extraction and sampling
- Object detection on frames
- Timestamped event detection
- Processing job management

### Audio Analysis
- Speech-to-text transcription
- Timestamped transcript segments
- Transcript search and export

### Forensic Timeline
- Unified event timeline
- Cross-modal evidence correlation
- Event filtering and navigation

### AI Investigation Assistant
- Evidence-grounded queries
- Persistent conversation history
- Structured responses with citations
- Hypothesis generation

### 3D Scene Viewer
- Interactive 3D visualization
- Detected object markers
- Scene layout reconstruction

### Forensic Reports
- Professional PDF generation
- Evidence inventory
- Analysis results
- AI-generated content disclaimer

## API Endpoints

### Health
- `GET /api/v1/health` - Backend health check
- `GET /api/v1/capabilities` - System capabilities

### Evidence
- `POST /api/v1/evidence/upload` - Upload evidence
- `GET /api/v1/evidence` - List evidence
- `GET /api/v1/evidence/{id}` - Get evidence details
- `DELETE /api/v1/evidence/{id}` - Delete evidence

### Analysis
- `POST /api/v1/analysis/image/{id}` - Run image analysis
- `POST /api/v1/analysis/video/{id}` - Start video processing
- `POST /api/v1/analysis/audio/{id}` - Start transcription

### Timeline
- `GET /api/v1/timeline` - Retrieve timeline events
- `POST /api/v1/timeline/events` - Create event

### AI Assistant
- `POST /api/v1/chat/conversations` - Create conversation
- `GET /api/v1/chat/conversations/{id}` - Get conversation
- `POST /api/v1/chat/conversations/{id}/messages` - Send message

### Reports
- `POST /api/v1/reports` - Generate report
- `GET /api/v1/reports/{id}/download` - Download PDF

## Development Milestones

- ✅ Milestone 1: Project Foundation
- ⏳ Milestone 2: Image Analysis
- ⏳ Milestone 3: Audio Analysis
- ⏳ Milestone 4: Video Analysis
- ⏳ Milestone 5: Multimodal Intelligence
- ⏳ Milestone 6: Reporting and Visualization
- ⏳ Milestone 7: Testing and Deployment

## Troubleshooting

### PowerShell Virtual Environment Activation
If activation fails with execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\Activate.ps1
```

Or use the Python executable directly:
```powershell
.venv\Scripts\python.exe run.py
```

### Port Already in Use
If port 5000 or 5173 is in use, change the port in:
- Backend: `backend/.env` (PORT variable)
- Frontend: `frontend/vite.config.ts` (server.port)

### Missing API Keys
The application will start without Groq API key configured. AI-powered features will show informative messages when unavailable.

### Model Download Failures
Large model downloads may fail due to network or disk space. Configure smaller models in `.env` or ensure adequate disk space and network connectivity.

## Security Considerations

- Never commit `.env` files or real API keys
- Validate all uploaded files
- Store evidence outside public directories
- Implement authentication before production use
- Treat all uploaded evidence as untrusted input
- Log analysis operations for audit trails

## License

This project is provided as a prototype for forensic analysis research and development.

## Support

For issues, questions, or contributions, please refer to the project documentation in the `docs/` directory.
