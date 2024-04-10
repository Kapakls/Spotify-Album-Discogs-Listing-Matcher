## Spotify Album & Discogs Listing Matcher

This Python script automates the process of finding potential matching listings for albums in your Spotify library on Discogs marketplace.

**Features:**

* Retrieves user data and album information from the Spotify API.
* Scrapes listing data from Discogs for each album in the user's library.
* Analyzes listing titles and identifies potential matches based on Jaccard similarity.

**Requirements:**

* Python 3.x
* `requests` library
* `cloudscraper` library
* `beautifulsoup4` library
* `pycountry` library
* `pathlib` library

**Instructions:**

1. Configure the script with your Spotify API credentials (client ID, client secret, redirect URL), remember to place all three files into the same folder directory.
2. Run `python main.py` to retrieve Spotify Album data, scrape listing data from the Discogs Marketplace and analyze it to identify potential matches which are saved locally and printed in terminal.

**Additional Notes:**

* Ensure you have installed the required libraries using `pip install <library_name>`.
* Just a passion project, this script is provided for educational purposes only and might require modifications depending on your specific needs.

**Disclaimer:**

This code utilizes third-party APIs (Spotify), web-scrapping (Discogs) and libraries. Always refer to their respective terms of service and documentation before using them in your projects.
