# 🧠 The Manipulator

The Manipulator is an AI-powered dispute analysis application built with Python, Streamlit, and the Google GenAI API.

The application takes two conflicting accounts and a human decision, then analyzes the information to identify agreements, contradictions, important evidence, and differences between the AI analysis and the human decision.

## Features

- Compare two conflicting accounts
- Extract important factual claims
- Identify agreements
- Identify contradictions
- Highlight relevant evidence
- Generate an AI-based neutral analysis
- Compare AI analysis with a human decision
- Retry temporary model/server failures
- Secure API key handling through environment variables
- Clean Streamlit interface

## Technologies Used

- Python
- Streamlit
- Google GenAI API
- python-dotenv

## Project Structure

```text
The-Manipulator/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/The-Manipulator.git
cd The-Manipulator
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a file named `.env` in the project folder.

Use `.env.example` as a template:

```text
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=your_supported_gemini_model
```

Do not upload `.env` to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## How It Works

1. The user enters Account 1.
2. The user enters Account 2.
3. The user provides the human decision.
4. The application sends the information to the configured Gemini model.
5. The AI identifies agreements, contradictions, and relevant evidence.
6. The AI generates a neutral analysis.
7. The application compares the AI analysis with the human decision.

## Future Improvements

- Structured JSON responses
- Better result visualization
- Conversation/history support
- Export analysis as PDF
- Automated testing
- Model selection through the interface
- Streamlit Cloud deployment

## Disclaimer

This project provides AI-generated analysis based only on the information provided by the user.

It should not be treated as a factual, legal, or authoritative determination of responsibility or guilt.
