import os
import requests
from dotenv import load_dotenv
from openai import AzureOpenAI
from utils.config import (
    AZURE_SPEECH_KEY,
    AZURE_SPEECH_ENDPOINT,
    AZURE_SPEECH_DEPLOYMENT_ID,
    AZURE_SPEECH_API_VERSION,
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT_ID,
    AZURE_OPENAI_API_VERSION
)

# Load environment variables
load_dotenv()

AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT", AZURE_OPENAI_DEPLOYMENT_ID)

# ✅ Initialize OpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION
)

# === 1. Essay Evaluation ===
def get_essay_feedback(text: str) -> str:
    prompt = f"""
You're an IELTS examiner. Evaluate the following Task 2 essay with clear, structured feedback under these sections:

1. **Task Response**
- Did the writer fully address the question?
- Was a clear position presented and supported?

2. **Coherence & Cohesion**
- Was the essay well organized?
- Were linking words and paragraphs used logically?

3. **Lexical Resource**
- Comment on vocabulary range, accuracy, and appropriateness.
- Note any strong or weak word choices.

4. **Grammar**
- Identify common grammar mistakes (tenses, structure, punctuation).
- Give 2–3 sentence corrections with explanations.

5. **Paragraph Feedback**
- Briefly review strengths & weaknesses of each paragraph.

6. **Tone**
- Was the style academic and formal enough?

7. **Band Score Estimate**
- Overall Band (1–9)
- Sub-scores: TR / CC / LR / GRA

8. **Word Count & Timing**
- Approx. word count?
- Was it too long/short for 40 mins?

9. **Recommendations**
- Suggest 3–4 practical tips for improvement (grammar, vocab, structure).

Essay:
\"\"\"{text}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are an IELTS examiner evaluating a Writing Task 2 essay."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR]: {str(e)}"

# === 2. Transcribe Speech Audio ===
def transcribe_audio(file_path: str) -> str:
    url = f"{AZURE_SPEECH_ENDPOINT}/openai/deployments/{AZURE_SPEECH_DEPLOYMENT_ID}/audio/transcriptions?api-version={AZURE_SPEECH_API_VERSION}"

    headers = {
        "api-key": AZURE_SPEECH_KEY,
    }

    with open(file_path, "rb") as audio_file:
        files = {
            "file": (os.path.basename(file_path), audio_file, "application/octet-stream")
        }

        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            return response.json()["text"]
        except Exception as e:
            print(f"[Transcription Error]: {e}")
            raise

# === 3. Evaluate Speaking Transcript ===
def evaluate_speaking_transcript(transcript: str) -> str:
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_ID}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY,
    }

    prompt = f"""
You are an IELTS Speaking examiner. Evaluate the candidate's spoken response based on IELTS Speaking Band Descriptors.

The response is transcribed below (infer likely fluency and pronunciation):

\"\"\"{transcript}\"\"\"

Return structured feedback in this format:

1. **Band Score**: 1–9

2. **Fluency & Coherence**
- Was the speech smooth and logical?
- Any noticeable pauses, fillers, or repetition?

3. **Lexical Resource**
- Range and accuracy of vocabulary
- Use of natural expressions or topic-specific words

4. **Grammar**
- Variety and accuracy of sentence structures

5. **Pronunciation**
- Clarity and rhythm (inferred from phrasing)

6. **Suggestions**
- Give 2–3 clear, actionable tips for improvement

Respond in **Markdown** format.
"""


    body = {
        "messages": [
            {"role": "system", "content": "You are a certified IELTS Speaking examiner."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[Speaking Evaluation Error]: {e}")
        raise
