import streamlit as st
from utils.text_analysis import (
    get_transcript,
    preprocess_transcript_for_key_points,
    summarize_text_chunks,
    analyze_sentiment,
    explain_sentiment,
)
from utils.gemini_api import gemini_extract_topics, gemini_key_concepts, gemini_contextual_insights
from utils.pdf_generator import generate_and_save_pdf
from dotenv import load_dotenv

load_dotenv() 

# Main Title
st.markdown(
    """
    <div style="text-align: center; width: 100%; padding: 10px 0;">
        <h1 style="font-size: 32px; margin: 0;">🎥 YouTube Summarizer & Contextual Insights with NLP and Generative AI</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Description Section
st.markdown(
    """
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="font-size: 24px; margin-bottom: 15px;">About This App</h3>
        <p style="font-size: 16px; line-height: 1.6;">This application helps you extract, summarize, and analyze YouTube video content. Here's what it does:</p>
        <ul style="font-size: 16px; line-height: 1.8;">
            <li><b>Transcript Extraction:</b> Automatically fetches and displays the video transcript.</li>
            <li><b>Summarization:</b> Provides a concise summary of the video content.</li>
            <li><b>Sentiment Analysis:</b> Analyzes the sentiment of the summarized content.</li>
            <li><b>Topic and Key Concept Extraction:</b> Identifies important topics and concepts.</li>
            <li><b>Contextual Insights:</b> Generates meaningful insights based on the extracted concepts.</li>
            <li><b>PDF Report:</b> Compiles all results into a downloadable PDF file.</li>
        </ul>
        <p style="font-size: 16px; line-height: 1.6;">To get started, enter a YouTube video URL below and click "Start Generative AI Analysis".</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Centered Input Section with Aligned Button
st.markdown("<h3 style='text-align: center;'>Enter YouTube Video URL</h3>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])  # Create two columns: wider column for input, smaller for button

# Place the input field in the first column
with col1:
    video_url = st.text_input("YouTube Video URL", placeholder="Paste your YouTube URL here")

# Place the button in the second column
with col2:
    start_analysis = st.button("Start Generative AI Analysis")

if video_url:
    # Display the video in the app
    st.markdown("<h2 style='text-align: center;'>🎬 Video Preview</h2>", unsafe_allow_html=True)
    st.video(video_url)

if start_analysis:
    if video_url:
        try:
            # Progress Display
            progress = st.progress(0)

            # Step 1: Extract Transcript
            with st.spinner("Extracting transcript..."):
                transcript = get_transcript(video_url)
            progress.progress(20)
            st.success("Transcript extracted successfully!")

            # Display Transcript
            st.markdown(
                f"""
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h2>📜 Transcript</h2>
                    <pre style="white-space: pre-wrap;">{transcript}</pre>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Step 2: Summarize Transcript
            with st.spinner("Summarizing transcript..."):
                clean_transcript = preprocess_transcript_for_key_points(transcript)
                summary = summarize_text_chunks(clean_transcript, max_chunk=400)
            progress.progress(40)
            st.success("Summary generated!")

            # Display Summary
            st.markdown(
                f"""
                <div style="background-color: #f4f4f4; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h2>✍️ Summary</h2>
                    <p>{summary}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Step 3: Sentiment Analysis
            with st.spinner("Analyzing sentiment..."):
                sentiment_result = analyze_sentiment(summary)
                sentiment_label, sentiment_score = sentiment_result.split(" (Score: ")
                sentiment_score = float(sentiment_score[:-1])
                sentiment_explanation = explain_sentiment(summary, sentiment_label)
            progress.progress(60)
            st.success("Sentiment analysis complete!")

            # Display Sentiment
            st.markdown(
                f"""
                <div style="background-color: #e9ffe9; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h2>😊 Sentiment Analysis</h2>
                    <p><b>Sentiment:</b> {sentiment_label} ({sentiment_score:.2f})</p>
                    <p><b>Why is this sentiment?</b> {sentiment_explanation}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Step 4: Extract Topics and Key Concepts
            with st.spinner("Extracting topics and key concepts..."):
                topics = gemini_extract_topics(summary)
                concepts = gemini_key_concepts(summary)
            progress.progress(80)
            st.success("Topics and key concepts identified!")

            # Display Topics and Key Concepts
            st.markdown(
                f"""
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h2>🏷️ Topics</h2>
                    <ul>{''.join([f'<li>{topic}</li>' for topic in topics])}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div style="background-color: #f4f4f4; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h2>💡 Key Concepts</h2>
                    <ul>{''.join([f'<li><b>{concept}</b></li>' for concept in concepts])}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Step 5: Contextual Insights
            with st.spinner("Fetching contextual insights..."):
                insights = gemini_contextual_insights(concepts)
            progress.progress(100)
            st.success("Contextual insights fetched!")

            import re

            # Function to extract video ID
            def extract_video_id(url):
                """
                Extract the YouTube video ID from a URL.
                Handles various formats like:
                - https://www.youtube.com/watch?v=abc123xyz
                - https://youtu.be/abc123xyz
                """
                match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
                if match:
                    return match.group(1)
                else:
                    raise ValueError("Invalid YouTube URL!")

            # Step 6: Generate and Save PDF
            try:
                # Extract video ID and sanitize the filename
                video_id = extract_video_id(video_url)
                pdf_filename = f"{video_id}_notes.pdf"
            except ValueError:
                st.error("Invalid YouTube URL. Unable to generate a valid filename.")
                st.stop()

            with st.spinner("Generating and saving PDF..."):
                pdf_path = generate_and_save_pdf(
                    summary,
                    concepts,
                    sentiment_label,
                    sentiment_score,
                    sentiment_explanation,
                    topics,
                    insights,
                    pdf_filename,
                )
            st.success("PDF generated and saved!")

            # Step 7: Provide Download Button
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download PDF Notes",
                    data=f,
                    file_name=pdf_filename,
                    mime="application/pdf",
                )

        except Exception as e:
            st.error(f"Error: {e}")