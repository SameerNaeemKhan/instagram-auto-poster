# Instagram Auto-Poster for Pakistan Scenery

## Overview
This Python script automates the process of downloading images from Pexels and uploading them to Instagram. It ensures that each image meets Instagram's aspect ratio requirements and avoids re-uploading previously posted images.

## Features
- Fetches new images of Pakistan's landscapes from the Pexels API.
- Ensures aspect ratio compliance for Instagram.
- Logs uploaded images to prevent duplicates.
- Automatically posts an image to Instagram every 12 hours.
- Uses Instabot for Instagram automation.

## Installation
### Prerequisites
- Python 3.x
- `pip` package manager
- Instagram account credentials
- Pexels API key

### Dependencies
Install required Python packages using:
```sh
pip install requests instabot pillow
```

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/instagram-auto-poster.git
   cd instagram-auto-poster
   ```
2. Add your Instagram credentials and Pexels API key to the script.
3. Ensure an `images/` directory exists in the project folder.
4. Run the script:
   ```sh
   python script.py
   ```

## Usage
- The script will fetch a new image from Pexels and upload it to Instagram.
- If an image has already been posted, it will be skipped.
- The script runs continuously and posts a new image every 12 hours.

## File Structure
```
instagram-auto-poster/
│── images/                 # Directory for downloaded images
│── script.py               # Main automation script
│── posted_images.txt       # Log of uploaded images
│── requirements.txt        # Required Python dependencies
```

## Troubleshooting
- If login issues occur, delete the `config/` folder before running the script.
- If `feedback_required` errors appear, Instagram might have temporarily restricted automation. Wait 24 hours before retrying.

## Future Enhancements
- Implement dynamic hashtag generation.
- Improve error handling and logging.
- Add scheduling options for more flexible posting.

## License
This project is licensed under the MIT License.

## Author
Developed by [Your Name].

