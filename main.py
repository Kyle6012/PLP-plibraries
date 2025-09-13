import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    # get filename from the url
    # if not found make one using md5 hash
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename or '.' not in filename:
        filename = f"downloaded_{hashlib.md5(url.encode()).hexdigest()[:8]}.jpg"
    return filename

def fetch_image(url, save_dir, known_hashes):
    # fetch one image from url and save it
    try:
        # send request with user agent
        headers = {"User-Agent": "UbuntuImageFetcher/1.0"}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  # check http errors

        # make sure content is an image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped (not an image): {url}")
            return None

        # get filename
        filename = get_filename_from_url(url)
        filepath = os.path.join(save_dir, filename)

        # check duplicates using hash of content
        file_hash = hashlib.md5(response.content).hexdigest()
        if file_hash in known_hashes:
            print(f"✗ Duplicate skipped: {filename}")
            return None

        # save file in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        # remember this file hash
        known_hashes.add(file_hash)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        return filepath

    except requests.exceptions.RequestException as e:
        # handle network errors
        print(f"✗ Connection error: {e}")
    except Exception as e:
        # handle other errors
        print(f"✗ An error occurred: {e}")
    return None

def main():
    # main function
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # allow multiple urls with comma
    urls = input("Please enter image URLs (comma-separated): ").split(",")

    # create folder for saving images
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)

    # set to track duplicate images
    known_hashes = set()

    # loop over all urls
    for url in [u.strip() for u in urls if u.strip()]:
        fetch_image(url, save_dir, known_hashes)

    # final ubuntu message
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
