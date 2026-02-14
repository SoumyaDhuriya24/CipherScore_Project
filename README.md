# CipherScore: Security Evaluation of Lightweight Ciphers

CipherScore is a security evaluation tool designed to analyze and audit cryptographic algorithms, specifically focusing on lightweight ciphers suitable for IoT devices. It provides metrics on Avalanche Effect, Encryption Speed, Memory Usage, and Attack Resistance.

## Project Structure

- **`core/`**: Core logic for the audit agent and analysis.
- **`ciphers/`**: Implementations of various ciphers (Ascon, Simon, Speck, etc.).
- **`backend/`**: FastAPI backend server exposing the analysis logic.
- **`frontend/`**: React-based user interface.

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+

### Installation

1.  **Install Backend Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Install Frontend Dependencies**:
    ```bash
    cd frontend
    npm install
    ```

## Usage

### 1. Start the Backend Server

From the project root directory:

```bash
python -m uvicorn backend.main:app --reload
```
*Server will start at http://localhost:8000*

### 2. Start the Frontend Application

Open a new terminal, navigate to the frontend directory, and start the vite server:

```bash
cd frontend
npm run dev
```
*Application will be accessible at http://localhost:5173*

## Features

- **Standard Ciphers**: Test pre-implemented ciphers like Ascon, Simon, Speck, and PRESENT.
- **Custom Ciphers**: Paste your own Python cipher implementation to audit it dynamically.
- **Visual Analytics**: View avalanche effect charts and performance metrics.
