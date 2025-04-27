from captioner import generate_caption

def main():
    description = """
  ☞Perfect for Diy Glam Hollywood Style Vanity - If you have always wanted a Hollywood style vanity but not enough to spend hundreds of dollars on one. These led vanity mirror lights give you that look for next to nothing.
☞Easy & Stress-free Installation - No wall or holes drilling. Your best beauty investment. No assembly or electrical wiring is required, just stick firmly these led vanity lights to a wall, mirror, or mirror frame and you’re good to go!
☞Multiply Application - These makeup mirror lights are waterproof. Ideal for Living room, Bathroom mirror-front lighting, Mural, Vanity table and Art display or home use, chose wisely on where you would like your lights.
☞Smart Touch Dimmer - Come with smart touch dimmer, touch to adjust brightness and turn off/on.Perfect, affordable lighted wall mirror you can use daily while applying makeup, taking photos of makeup looks, and even recording makeup tutorials.
☞Nice Look - This led vanity light is beautiful, very bright and chic ! Perfect for your vanity mirror! Perfect solution for your search to add better lighting for your make up table.
"""

    image_path = ""

    # Generate caption using the captioner
    caption = generate_caption(description)
    print(f"Title: {caption['title']}")
    print(f"Caption: {caption['caption']}")
    print(f"Alt Text: {caption['alt_text']}")
    print(f"Tagged Topics: {caption['tagged_topics']}")

    confirmation = input("Do you want to post this caption with the image? (y/n): ").strip().lower()
    if confirmation == "y":
        # Here you would call your Pinterest API to post the image with the caption
        # For example:
        # pinterest_api.post_image(image_path, caption)
        print(f"Posting image {image_path} with caption: {caption}")
    else:
        print("Post cancelled.")

if __name__ == "__main__":
    main()