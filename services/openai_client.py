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
You are an expert IELTS examiner and academic coach. Evaluate the following IELTS Writing Task 2 essay and provide detailed, structured feedback.

Please break your response into these sections:

1. Task Response
- Did the essay fully address the prompt?
- Was a clear thesis/position stated and maintained?
- Were arguments well-supported with relevant examples?

2. Coherence and Cohesion
- Was the essay logically organized?
- Were transitions and cohesive devices used effectively?
- Was paragraphing appropriate?

3. Lexical Resource
- Analyze vocabulary range and accuracy.
- Highlight advanced words or idiomatic usage.
- Flag inappropriate or awkward word choices with alternatives.

4. Grammatical Range and Accuracy
- Identify issues with tenses, articles, agreement, sentence structure, punctuation.
- Provide 2–3 example sentences from the essay and explain errors + corrections.

5. Paragraph-Level Suggestions
- Go through each paragraph and mention:
    • Strengths
    • Specific improvements (e.g., clarity, structure, detail)

6. Tone and Register
- Assess if the tone was academic/formal enough.
- Flag any casual or informal language.

7. Band Score Estimation
- Provide an overall band score (1–9)
- Also give sub-scores for:
    • Task Response
    • Coherence & Cohesion
    • Lexical Resource
    • Grammar

8. Word Count and Time Efficiency
- Estimate word count.
- Suggest ideal time taken to write this essay during an exam (e.g., 35–40 mins).
- Was the essay too long or short?

9. Comparative Feedback (optional)
- If the essay is Band 8+, describe what a Band 9 would improve slightly better (e.g., nuance, conciseness, lexical depth).

10. Recommendations to Improve
- Suggest 3–5 actionable steps with links if possible.
    • Grammar: [e.g., Perfect Tense practice]
    • Vocabulary: [e.g., Academic Word List drills]
    • Structure: [e.g., Cohesive devices guide]

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
You are an IELTS Speaking examiner. Evaluate the following candidate's **spoken** response based on IELTS Speaking Band Descriptors.

The response is transcribed below (please infer pronunciation and fluency from likely speech patterns):

\"\"\"{transcript}\"\"\"

Respond with structured feedback in this format:

1. **Band Score**: Overall score from 1 to 9

2. **Fluency and Coherence**
- Is the speech smooth and logical?
- Are there hesitations, fillers, or self-corrections?

3. **Lexical Resource**
- Vocabulary range and appropriateness
- Use of idiomatic or topic-specific expressions

4. **Grammatical Range and Accuracy**
- Use of various sentence structures
- Grammatical accuracy

5. **Pronunciation**
- Clarity, stress, intonation, rhythm (infer based on errors or awkward phrasing in transcript)

6. **Suggestions for Improvement**
- Give 2–3 targeted tips

Format in Markdown.
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
