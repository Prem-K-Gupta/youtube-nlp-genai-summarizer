
# 🎥 YouTube Video Summarizer with Contextual Insights

This Streamlit-based application extracts key information from YouTube videos and generates a detailed summary along with sentiment analysis, topics, and contextual insights. A PDF of the results can be downloaded directly from the app.

## 🚀 Features
1. **Transcript Extraction**: Automatically extracts transcripts from YouTube videos.
2. **Summarization**: Provides a concise summary of the video content.
3. **Sentiment Analysis**: Analyzes the sentiment of the summarized content.
4. **Topic and Key Concept Extraction**: Identifies important topics and concepts.
5. **Contextual Insights**: Generates insights based on the extracted concepts.
6. **PDF Report**: Generates a downloadable PDF with all the analysis results.

## 🛠️ Installation

1. Clone this repository:

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Add the `DejaVuSans.ttf` font file to your project directory for proper PDF rendering:
   - Download the font from [DejaVu Fonts](https://dejavu-fonts.github.io/) and place it in the root directory.

4. Run the application:
   ```
   streamlit run app.py
   ```

## 📝 Usage

1. Enter a YouTube video URL in the input field.
2. Click the "Start Generative AI Analysis" button.
3. View the extracted transcript, summary, sentiment analysis, topics, and insights.
4. Download the PDF report using the provided button.

## 🧰 Requirements
- Python 3.8+
- Streamlit
- FPDF
- Google Generative AI
- Transformers
- YouTube Transcript API

## 📁 Directory Structure
```plaintext
youtube-summarizer/
│
├── app.py                 # Main application script
├── requirements.txt       # Python dependencies
├── utils/
│   ├── text_analysis.py   # Text analysis helper functions
│   ├── gemini_api.py      # Functions to interact with Gemini API
│   └── pdf_generator.py   # PDF generation utility
└── DejaVuSans.ttf         # Font file for PDF generation
```

## 🔧 Customization

- **API Key**: Add your API key for the Google Generative AI in the `utils/gemini_api.py` file.
- **PDF Output Directory**: PDFs are saved in the `saved_pdfs` directory. You can customize this in the `generate_and_save_pdf` function.

## 🛑 Known Issues
1. Some YouTube videos might not have transcripts available.
2. The summarization might fail for excessively long transcripts due to token limits. Chunking is already implemented to mitigate this issue.


