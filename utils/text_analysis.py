from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

# Hugging Face pipelines
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
token_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL provided!")

def get_transcript(video_url):
    video_id = extract_video_id(video_url)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t['text'] for t in transcript])
    except Exception as e:
        raise ValueError(f"Failed to fetch transcript: {e}")

def preprocess_transcript_for_key_points(transcript):
    """
    Preprocess the transcript to retain key points and remove filler words.
    """
    # Remove filler words or phrases (e.g., "um", "you know", "[Music]")
    transcript = re.sub(r"\[.*?\]", "", transcript)  # Remove content in brackets
    transcript = re.sub(r"\b(um|uh|you know|like|yeah|right|okay)\b", "", transcript, flags=re.IGNORECASE)

    # Remove excessively long pauses or repetitive phrases
    transcript = re.sub(r"(?:\s+)", " ", transcript).strip()

    return transcript


def summarize_text_chunks(text, max_chunk=400):
    """
    Split text into smaller chunks, preprocess them, and summarize.
    Adjust summarization instructions to explain video content better.
    """
    words = text.split()
    chunks = [" ".join(words[i:i + max_chunk]) for i in range(0, len(words), max_chunk)]
    summaries = []

    for chunk in chunks:
        input_length = len(chunk.split())
        adjusted_max_length = min(150, max(40, int(input_length * 0.8)))  # Adjusted max length to 80% of input
        prompt = f"Summarize this video content as if explaining it to someone who hasn't watched it:\n{chunk}"
        summary = summarizer(prompt, max_length=adjusted_max_length, min_length=20, do_sample=False)[0]["summary_text"]
        summaries.append(summary.strip())

    # Combine all chunk summaries
    combined_summary = " ".join(summaries)

    combined_summary = post_process_summary(combined_summary)

    return combined_summary


def post_process_summary(summary):
    """
    Post-process the summary to improve coherence and remove redundancy.
    """
    summary = summary.replace("..", ".").strip()  # Clean up repeated periods
    sentences = summary.split(". ")  # Split into sentences
    unique_sentences = list(dict.fromkeys(sentences))  # Remove duplicates while preserving order
    return ". ".join(unique_sentences).strip()


def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return f"{result['label']} (Score: {result['score']:.2f})"

def explain_sentiment(text, sentiment_label):
    explanation = token_classifier(
        text,
        candidate_labels=["optimism", "negativity", "challenges", "happiness", "sadness"],
    )
    reasons = ", ".join(explanation["labels"][:3])
    return f"The sentiment is {sentiment_label.lower()} because it contains aspects of {reasons}."
