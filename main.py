import sys
import AppKit
import requests
from pathlib import Path
from PIL import Image
import objc
import time
import shutil

BASE_URL = "https://sdo.gsfc.nasa.gov"

DOWNLOAD_PATH = Path.home() / "Downloads" / "SDO_Wallpapers"


def set_wallpaper(image_path: Path, screen: AppKit.NSScreen):
    ws = AppKit.NSWorkspace.sharedWorkspace()
    url = AppKit.NSURL.fileURLWithPath_(image_path.as_posix())
    options = {}
    error = objc.nil

    ws.setDesktopImageURL_forScreen_options_error_(url, screen, options, error)

    if error:
        raise RuntimeError("Error in PyObjC setting desktop image: {error}")


def resize_and_center_image(
    image_path: Path,
    final_width: int,
    final_height: int,
    background_color: tuple[int, int, int],
):
    # Load the original image
    original_image = Image.open(image_path)

    # Resize image if it is larger than the final dimensions
    final_size = int(final_width), int(final_height)
    original_image.thumbnail(final_size, Image.Resampling.LANCZOS)

    # Calculate the padding
    original_width, original_height = original_image.size
    padding_left = int((final_width - original_width) // 2)
    padding_top = int((final_height - original_height) // 2)

    # Create new image with background color
    new_image = Image.new("RGB", final_size, background_color)

    # Paste original image onto the center of the new image
    new_image.paste(original_image, (padding_left, padding_top))

    # Save the result
    new_image.save(image_path)
    return image_path


def download(url: str, folder: Path):
    """
    download image and wait for download to finish
    """
    # delete file if exists
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True, exist_ok=True)

    impath = folder / f"current-sdo-image_{int(time.time())}.jpg"

    response = requests.get(url, stream=True)
    with open(impath, "wb") as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    return impath


def main():
    src = "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_4096_HMII.jpg"
    screen = AppKit.NSScreen.screens()[0]
    src = src
    dimensions = screen.devicePixelCounts()
    dl_path = download(src, DOWNLOAD_PATH)
    padded_img = resize_and_center_image(
        dl_path,
        dimensions.width,
        dimensions.height,
        background_color=(0, 0, 0),
    )
    set_wallpaper(padded_img, screen)


if __name__ == "__main__":
    sys.exit(main())
