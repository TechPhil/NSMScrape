# 🎵 NSM Audio Scraper

This Python script scrapes audio tracks from [No Sheet Music](https://www.nosheetmusic.tv/) album pages by simulating play button clicks using Selenium. It then downloads and renames each track into a readable format, organizing them into folders by album.

---

## 📦 Features

- Automatically clicks all track play buttons to reveal audio file URLs
- Intercepts and downloads each `.mp3` file
- Renames files to:  
  **`Composer - Title (Album TK###).mp3`**
- Saves all audio into:  
  **`audio_downloads/NSM###/`** folders

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/nsm-audio-scraper.git
cd nsm-audio-scraper
```

### 2. Set up environment
```bash
python3 -m venv scrape-env
source scrape-env/bin/activate
pip install -r requirements.txt
```

### 3. Run the scraper
```bash
python scraper.py
```

You’ll be prompted to paste an album URL, such as:

```
https://www.nosheetmusic.tv/albums/nsm154
```

---

## 📝 Notes

- Requires [Google Chrome](https://www.google.com/chrome/) installed.
- Works best with stable internet connection (audio files are fetched dynamically).
- If tracks fail to download, re-run the script — only new files will be added.

---

## ⚙️ Dependencies

- `selenium`
- `selenium-wire`
- `webdriver-manager`
- `requests`
- `blinker<1.8` (compat fix)

All dependencies are listed in [`requirements.txt`](requirements.txt).

---

## ✅ License

This tool is provided for **educational and archival purposes**. Always ensure you have the right to download and use any media.

---

## 🧑‍💻 Author

Developed by Phil Hughes  
Feel free to fork, suggest improvements, or raise issues!
