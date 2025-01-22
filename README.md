# Declutter Project

Declutter is an intelligent content processing system that helps users stay informed by automatically fetching, summarizing, and converting news articles into audio format. The system combines several AI technologies to create a seamless information consumption experience.

## How Declutter Works

1. **News Fetching (news_fetcher.py)**: Declutter automatically retrieves the latest news articles from various sources using the News API.
2. **Content Summarization (summarizer.py)**: Using OpenAI's GPT models, it employs a chunk-based iterative summarization approach:
   - Chunk the text into smaller segments
   - Summarize each chunk individually to get partial summaries
   - Merge partial summaries and summarize again for a final, concise summary
   This approach ensures better context preservation and more accurate summarization of long articles.
3. **Audio Generation (audio_generator.py)**: The summarized content is converted into high-quality audio using a chunk-based approach:
   - Split input text into sentences
   - Generate audio for each sentence separately
   - Concatenate individual audio clips into a continuous stream
   - Normalize the final waveform for consistent volume
   This approach was developed to overcome Kokoro's 30-second limitation per audio generation, allowing for arbitrary-length audio output while maintaining high quality and natural pacing.
4. **Output Management (declutter.py)**: The system organizes the processed content into structured audio files for easy access and playback.

## Kokoro-82M Integration

Declutter utilizes the Kokoro-82M text-to-speech system for audio generation. Kokoro-82M is a state-of-the-art TTS model that produces natural-sounding speech with various voice options.

## File Structure

```
Kokoro-82M/
├── models/                # Kokoro model files
├── voices/                # Pre-trained voice models
├── fp16/                  # Half-precision utilities
├── demo/                  # Example outputs
├── audio_generator.py     # Audio generation module
├── declutter.py           # Main application
├── news_fetcher.py        # News fetching module
├── summarizer.py          # Text summarization
├── models.py              # Model architecture
├── plbert.py              # PL-BERT implementation
├── istftnet.py            # ISTFT network
├── kokoro.py              # Kokoro interface
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # This file
```

## Installation

To use Declutter with Kokoro-82M:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Kokoro-82M.git
cd Kokoro-82M
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Kokoro model:
```bash
git clone https://huggingface.co/hexgrad/Kokoro-82M models/Kokoro-82M
```

4. Set up environment variables by creating a .env file:
```bash
touch .env
```

Edit the .env file to include:
- OpenAI API key (for summarization)
- News API key (for article fetching)

The file should follow this format:
```
OPENAI_API_KEY=your_openai_key_here
NEWS_API_KEY=your_newsapi_key_here
```

### Running the Application
Run the main script:
```bash
python declutter.py
```

### Configuration Options:
1. **Fetching Topic**: Edit config.json to set your desired news topic (e.g., "technology", "business", "sports")
2. **Number of Articles**: Set the "max_articles" parameter in config.json (default: 5)
3. **Output Location**: Audio files are saved in the "output/" directory, organized by date

The system will:
1. Fetch news articles based on your configured topic
2. Summarize content using AI
3. Generate audio from the summarized text
4. Save output as WAV files in the output directory

## File Structure

```
Kokoro-82M/
├── models/                # Kokoro model files
├── voices/                # Pre-trained voice models
├── fp16/                  # Half-precision utilities
├── demo/                  # Example outputs
├── audio_generator.py     # Audio generation module
├── declutter.py           # Main application
├── news_fetcher.py        # News fetching module
├── summarizer.py          # Text summarization
├── models.py              # Model architecture
├── plbert.py              # PL-BERT implementation
├── istftnet.py            # ISTFT network
├── kokoro.py              # Kokoro interface
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # This file
```

## Dependencies

- Python 3.8+
- PyTorch 1.10+
- Kokoro-82M model
- OpenAI API key (for summarization)
- News API key (for article fetching)

## Configuration

### Environment Variables
We use a .env file for storing sensitive information such as API keys. This file is not tracked by Git for security reasons, following industry best practices for handling credentials. Create a .env file and include your API keys following the format shown in the Installation section.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
>>>>>>> d4bc6e1 (first commit)
