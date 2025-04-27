import os
from PIL import Image

def remove_metadata(input_path, output_path):
    with Image.open(input_path) as img:
        data = list(img.getdata())
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(data)
        clean_img.save(output_path)

def process_all_images():
    input_folder = "generated_images"
    output_folder = "final_images"

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Process each image file
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Skip if already processed
            if os.path.exists(output_path):
                print(f"Skipping (already cleaned): {filename}")
                continue

            try:
                remove_metadata(input_path, output_path)
                print(f"Cleaned: {filename}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    process_all_images()
