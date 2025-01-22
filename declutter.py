# import os
# os.environ["PHONEMIZER_ESPEAK_PATH"] = "/opt/homebrew/bin/espeak-ng"  # Path to espeak-ng binary
# os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = "/opt/homebrew/lib/libespeak-ng.dylib"
from kokoro import generate
from models import build_model
from news_fetcher import fetch_news, process_articles_to_df
import summarizer
from audio_generator import generate_and_concatenate
import soundfile as sf

def main():
    # df = pd.read_csv('news_articles.csv')
    # 1. Fetch and save as df
    articles = fetch_news("AI", target_count=5, sort_by="popularity")
    df = process_articles_to_df(articles)
    # df.to_csv("news_articles.csv", index=False)
    # 2. Summarize
    df["Summary"] = df["Full Content"].apply(summarizer.summarize_long_text)
    # 3. Generate Audio FloatArray
    df["AudioFloatArray"] = df["Summary"].apply(lambda text: generate_and_concatenate(text, sample_rate=24000))
    for index, audio_array in enumerate(df["AudioFloatArray"]):
        sf.write(f"output{index+1}.wav", audio_array, 24000)
    print(f"--Wrote {len(df)} TTS outputs--")  


if __name__ == "__main__":
    main()