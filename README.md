# AI Asset Identification System

This is a production-quality full-stack application that identifies assets, detects brands, retrieves potential model numbers using web search, and verifies them using a unified AI inference pipeline powered by Google Gemini.

## Key Features
- **Unified AI Pipeline**: Integrates OpenCV for image preprocessing and Google Gemini (Multimodal AI) for zero-shot visual classification, brand detection, and OCR text extraction in a single, robust inference pass.
- **Deterministic Confidence Scoring**: Utilizes a float-based calculation logic combining Gemini's reasoning certainty, extracted text matching, visual features, and Tavily search validation to generate highly accurate confidence metrics.
- **Modern User Interface**: Features a vibrant, high-contrast frontend layout designed for maximum data clarity and an enhanced user experience.
- **Smart Result Filtering**: Intelligent backend logic to ensure unique, highly relevant retrieved models are presented.

## Architecture
- **Frontend**: React, Vite, Tailwind CSS, Axios, Lucide React
- **Backend**: FastAPI, Uvicorn, Pydantic
- **AI/ML**: OpenCV (Preprocessing), Google GenAI / Gemini (Multimodal Classification, OCR, and Reasoning)
- **Web Retrieval**: Tavily Search API, BeautifulSoup

## Setup Instructions

### Prerequisites
- Node.js (v18+)
- Python (3.9+)
- Tavily API Key
- Gemini API Key

### Backend Setup
1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies (this may take a while as it downloads PyTorch and Transformers):
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your `TAVILY_API_KEY` to the `.env` file.
5. Start the backend server:
   ```bash
   python main.py
   ```
   The backend will be available at `http://localhost:8000`.

### Frontend Setup
1. Open a new terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will usually be available at `http://localhost:5173`.

## Usage
1. Open the frontend in your browser.
2. Drag and drop or select an image of an asset (e.g., a mobile phone, microwave, or refrigerator).
3. The AI pipeline will process the image and display the predicted category, detected brand, and the top matching models from the web.
