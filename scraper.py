from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

import re
from urllib.parse import unquote

def format_track_filename(url: str) -> tuple[str, str]:
    from urllib.parse import unquote
    import re

    # Extract the filename
    filename = unquote(url.split("/")[-1])

    # Try to extract album, track, title, composer
    match = re.search(r"_(NSM\d+)_TK(\d+)_([A-Z0-9_]+)_([A-Za-z]+_[A-Za-z]+)", filename)
    if not match:
        return ("Unknown Album", "Unknown Track.mp3")

    album = match.group(1)                     # NSM154
    track_num = match.group(2)                 # e.g. 010
    title_raw = match.group(3)                 # e.g. CHEESE_IT
    composer_raw = match.group(4)              # e.g. Ben_Townsend

    title = title_raw.replace("_", " ").title()
    composer = composer_raw.replace("_", " ")

    filename_formatted = f"{composer} - {title} ({album} TK{track_num}).mp3"

    return album, filename_formatted



# Setup Chrome driver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # comment this out if you want to see the browser
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

urlToScrape = input("Please enter the NSM URL you would like to scrape: ")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(urlToScrape)

time.sleep(5)  # Wait for page to load


# Find all expand details buttons
expand_buttons = driver.find_elements(By.CSS_SELECTOR, 'i.fas.fa-chevron-down')

print(f"Found {len(expand_buttons)} expand buttons")

for i, button in enumerate(expand_buttons):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.5)
        button.click()
        time.sleep(1)  # Wait for details to expand
    except Exception as e:
        print(f"Error processing button {i+1}: {e}")

# Find all play buttons
play_buttons = driver.find_elements(By.CSS_SELECTOR, 'a.track__play-pause-button')

print(f"Found {len(play_buttons)} play buttons")

audio_urls = set()


for i, button in enumerate(play_buttons):
    try:
        # Clear previous requests
        del driver.requests

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        time.sleep(0.5)
        button.click()
        time.sleep(3)  # Give time for audio to load

        # Intercept requests for audio
        for request in driver.requests:
            if request.response and 'audio' in request.response.headers.get('Content-Type', ''):
                print(f"[{i+1}] Found audio: {request.url}")
                audio_urls.add(request.url)

        # Stop playback to avoid overlapping
        button.click()
        time.sleep(1)

    except Exception as e:
        print(f"Error processing button {i+1}: {e}")

# Download the audio files
os.makedirs("audio_downloads", exist_ok=True)

for idx, url in enumerate(audio_urls):
    try:
        album, formatted_name = format_track_filename(url)
        album_dir = os.path.join("audio_downloads", album)
        os.makedirs(album_dir, exist_ok=True)
        print(f"Downloading file {idx+1} from {url}")
        r = requests.get(url)
        formatted_name = format_track_filename(url)
        filename = os.path.join("audio_downloads", formatted_name)
        with open(filename, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        print(f"Failed to download from {url}: {e}")

driver.quit()
print("Done.")

