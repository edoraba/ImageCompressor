import os
from PIL import Image
import time
from tqdm import tqdm

# Function to resize the image while maintaining the aspect ratio
def resize_image(img, max_size):
    width, height = img.size
    if width <= max_size and height <= max_size:
        return img
    if width > height:
        new_width = max_size
        new_height = int((max_size / width) * height)
    else:
        new_height = max_size
        new_width = int((max_size / height) * width)
    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Function to compress and convert images to WebP format
def compress_and_convert_to_webp(image_path, output_path, max_size=2000, quality=80):
    try:
        img = Image.open(image_path)
        img = resize_image(img, max_size)

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        img.save(output_path, 'webp', quality=quality)
    except Exception as e:
        raise RuntimeError(f"Error saving {output_path}: {e}")

# Function to process multiple images
def process_images(image_files, output_directory, max_size=2000, quality=80, stop_requested=False):
    start_time = time.time()

    if not os.path.isdir(output_directory):
        raise RuntimeError(f"Invalid output directory: {output_directory}")

    with tqdm(total=len(image_files), desc="Processing images", unit="image") as pbar:
        for image_file in image_files:
            if stop_requested:
                print("Process stopped by user.")
                break

            filename = os.path.basename(image_file).replace(" ", "_")
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".webp")

            if not output_path or not os.path.isdir(os.path.dirname(output_path)):
                print(f"Invalid output path: {output_path}")
                continue

            try:
                compress_and_convert_to_webp(image_file, output_path, max_size, quality)
            except Exception as e:
                print(f"Error processing {image_file}: {e}")

            pbar.update(1)

    elapsed_time = time.time() - start_time
    if not stop_requested:
        print(f"Processing completed in {elapsed_time:.2f} seconds")
