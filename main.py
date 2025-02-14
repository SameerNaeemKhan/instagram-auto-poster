import requests
import os
import time
import random
from instabot import Bot
from PIL import Image

# API & Instagram Credentials
apiKey = "oz9xi5WovQYc6Oazaf2Bwug6WkqJu55XLeOWikgNvWDQmLZDYAr79hRW"
apiUrl = "https://api.pexels.com/v1/search"
instagramUsername = "pakistanvistas"
instagramPassword = "Har!pu@2007"

# Aspect Ratio Limits
max_aspect_ratio = 1.91
min_aspect_ratio = 4 / 5  # 0.8

# Image Directory
imageDir = "images"
os.makedirs(imageDir, exist_ok=True)

# Delete previous session files to avoid login issues
try:
    os.remove("config/pakistanvistas_uuid_and_cookie.json")
except FileNotFoundError:
    pass

# Login to Instagram
bot = Bot()
bot.login(username=instagramUsername, password=instagramPassword)

# Captions
captions = [
    "Exploring the landscapes of Pakistan! 🇵🇰 #Pakistan #WondersOfNature",
    "Breathtaking views from Pakistan. #ExplorePakistan",
    "The beauty of Pakistan, one photo at a time! #TravelPakistan",
    "Discover the hidden gems of Pakistan's landscapes. 🌄 #HiddenGems #Pakistan",
    "From mountain peaks to serene lakes, Pakistan's beauty is unparalleled. 🏔️ #NaturalWonders #Pakistan",
    "Embrace the breathtaking beauty of Pakistan’s diverse terrain. 🌍 #ExploreMore #Pakistan",
    "Immerse yourself in the picturesque landscapes of Pakistan. 🌅 #ScenicViews #TravelPakistan",
    "Wander through the stunning vistas of Pakistan. 🏞️ #AdventureAwaits #Pakistan",
    "Every corner of Pakistan has a story to tell through its landscapes. 📸 #StoryInEveryView #Pakistan",
    "Experience the awe-inspiring beauty of Pakistan’s natural wonders. 🌲 #NatureLovers #Pakistan",
    "Journey through Pakistan's picturesque landscapes and find your peace. 🌿 #PeacefulPlaces #Pakistan",
    "Let the stunning vistas of Pakistan take your breath away. 🌌 #BreathtakingViews #Pakistan",
    "Unveil the natural splendor of Pakistan's scenic wonders. 🌠 #ScenicSplendor #ExplorePakistan",
    "From lush valleys to desert landscapes, Pakistan offers endless beauty. 🌵 #ValleysAndDeserts #Pakistan",
    "Discover the majestic landscapes that make Pakistan a visual paradise. 🌈 #VisualParadise #Pakistan",
    "Every sunrise and sunset in Pakistan is a masterpiece. 🌞 #SunriseSunset #Pakistan",
    "The vibrant landscapes of Pakistan are a feast for the eyes. 🌺 #VibrantLandscapes #Pakistan",
    "Traverse the diverse landscapes of Pakistan and marvel at its beauty. 🌿 #DiverseLandscapes #ExplorePakistan",
    "Pakistan's natural beauty is a treasure waiting to be discovered. 💎 #NaturalTreasure #Pakistan",
    "Capture the essence of Pakistan’s stunning natural landscapes. 📷 #NatureEssence #Pakistan",
    "Explore the untouched beauty of Pakistan’s landscapes and feel the serenity. 🌄 #UntouchedBeauty #Pakistan",
    "Pakistan's landscapes are a testament to nature’s grandeur. 🌟 #NatureGranduer #ExplorePakistan",
    "Every image from Pakistan reveals a new facet of its beauty. 🌏 #NewFascets #Pakistan",

]

def fetch_pexels_images(query="Pakistan scenery"):
    """Fetch new images from Pexels, ensuring they haven't been uploaded before."""
    headers = {"Authorization": apiKey}
    params = {"query": query, "per_page": 10, "page": 1}

    # Load list of previously posted images
    if os.path.exists("posted_images.txt"):
        with open("posted_images.txt", "r") as file:
            posted_images = set(file.read().splitlines())  # Store already posted image filenames
    else:
        posted_images = set()

    while True:
        response = requests.get(apiUrl, headers=headers, params=params)

        if response.status_code == 200:
            photos = response.json().get('photos', [])
            if not photos:
                print("No more photos found. Exiting.")
                return None

            for photo in photos:
                imgUrl = photo['src']['original']
                imgId = str(photo['id'])
                imgName = os.path.join(imageDir, f"{imgId}.jpg")

                # ✅ Skip image if it has already been uploaded
                if f"{imgId}.jpg" in posted_images:
                    print(f"Skipping {imgName}, already uploaded.")
                    continue

                # Download new image
                imgData = requests.get(imgUrl).content
                with open(imgName, 'wb') as file:
                    file.write(imgData)

                # Validate aspect ratio
                width, height = get_image_dimensions(imgName)
                if not validate_aspect_ratio(width, height):
                    os.remove(imgName)  # Delete invalid image
                    continue

                print(f"✅ Downloaded new image: {imgName}")
                return imgName  # Return first valid new image

        else:
            print(f"Error fetching images: {response.status_code}")
            return None

        params['page'] += 1  # Fetch new images on next iteration



def validate_aspect_ratio(width, height):
    """Check if image aspect ratio is within Instagram's limits."""
    aspect_ratio = width / height
    if min_aspect_ratio <= aspect_ratio <= max_aspect_ratio:
        return True
    print(f"Skipping image: Aspect ratio {aspect_ratio:.2f} is outside allowed range.")
    return False


def get_image_dimensions(image_path):
    """Get image width and height."""
    with Image.open(image_path) as img:
        return img.size


def upload_to_instagram(imagePath):
    """Upload image to Instagram and log it to prevent re-upload."""
    width, height = get_image_dimensions(imagePath)
    if not validate_aspect_ratio(width, height):
        print(f"Skipping {imagePath} due to aspect ratio.")
        os.remove(imagePath)  # Remove invalid image
        return

    caption = random.choice(captions)

    # Remove .REMOVE_ME if exists
    if os.path.exists(imagePath + ".REMOVE_ME"):
        os.remove(imagePath + ".REMOVE_ME")

    try:
        bot.upload_photo(imagePath, caption=caption)
        print(f"✅ Uploaded: {imagePath} with caption: {caption}")

        # ✅ Log the uploaded image ID
        with open("posted_images.txt", "a") as log_file:
            log_file.write(f"{os.path.basename(imagePath)}\n")  # Only store filename, not full path

    except Exception as e:
        if "feedback_required" in str(e):
            print("⚠️ Warning: Instagram rate limit detected. Post was likely successful.")
        else:
            print(f"❌ Error uploading {imagePath}: {e}")
            os.remove(imagePath)  # Delete failed image


def main():
    """Main loop: Fetch an image and upload to Instagram every 12 hours."""
    while True:
        imgPath = fetch_pexels_images()
        if imgPath:
            upload_to_instagram(imgPath)

        time.sleep(12 * 60 * 60)  # 12 hours in seconds


if __name__ == "__main__":
    main()
