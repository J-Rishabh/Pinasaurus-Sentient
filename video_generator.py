import os
import shutil
import requests
import json
import re
import ast
from gtts import gTTS
from moviepy.editor import *
from moviepy.video.fx.all import resize, crop, fadein, fadeout
from moviepy.config import change_settings
from dotenv import load_dotenv

load_dotenv()


# === ImageMagick config ===
change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def generate_voice(text, filename):
    tts = gTTS(text=text, lang='en')
    path = os.path.join("voice", filename)
    tts.save(path)
    return path

def load_voice_with_silence(path, duration):
    voice = AudioFileClip(path)
    silence_duration = max(0, duration - voice.duration)
    silence = AudioClip(make_frame=lambda t: [0], duration=silence_duration, fps=44100)
    return concatenate_audioclips([voice, silence]).set_duration(duration)

def prepare_images(final_dir, video_dir, finished_dir, max_images=5):
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(finished_dir, exist_ok=True)

    used = set(os.listdir(finished_dir))
    all_images = [img for img in os.listdir(final_dir) if img.lower().endswith(('.jpg', '.png')) and img not in used]
    selected = all_images[:max_images]

    for img in selected:
        shutil.copy(os.path.join(final_dir, img), os.path.join(video_dir, img))

    return selected

def generate_youtube_caption_custom(description, item_count):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new",
        "max_tokens": 16384,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.6,
        "messages": [
            {
                "role": "user",
                "content": f"""
Please return ONLY a JSON object with the following keys:
- title: an SEO-optimized YouTube title for a video showcasing exactly {item_count} Amazon desk items.
- caption: formatted like this:

🔥 Upgrade your space with the latest & greatest in home decor – all from Amazon! From cozy vibes to modern elegance, these trending pieces will transform your home in 2024. Check them out below 👇

{item_count}. [Affiliate Link Here]
...
1. [Affiliate Link Here]

✨ Don’t miss out—these are perfect for your living room, bedroom, or apartment glow-up!
💬 Which one is your fave? Drop a comment below!

#HomeDecor #AmazonFinds #HomeGlowUp #InteriorDesign #DecorInspo #AmazonMustHaves #RoomTransformation #Affiliate #TrendingNow

The items featured in this video are: {description}
"""
            }
        ]
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('FIREWORKS_API_KEY')}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    raw_text = response.json()["choices"][0]["message"]["content"]

    print("\n=== 🔍 RAW MODEL RESPONSE ===\n")
    print(raw_text)

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if not match:
        raise ValueError("❌ No valid JSON or dict block found in response.")

    json_like = match.group(0)

    try:
        return ast.literal_eval(json_like)
    except Exception as e:
        print("\n❌ literal_eval failed. Here's the extracted text:\n")
        print(json_like)
        raise e

def create_short_video(images_folder, image_names, output_path="short_final.mp4", bgm_path="bgm.mp3"):
    base, ext = os.path.splitext(output_path)
    counter = 1
    dynamic_output = output_path
    while os.path.exists(dynamic_output):
        dynamic_output = f"{base}_{counter}{ext}"
        counter += 1

    os.makedirs("voice", exist_ok=True)
    num_items = len(image_names)
    clips = []

    cleaned = [os.path.splitext(name)[0].replace("_", " ").replace("-", " ") for name in image_names]
    data_string = f"TOP {num_items} AMAZON DESK ITEMS"

    intro_text = TextClip(data_string, fontsize=100, font="Impact", color="white",
                          method="caption", size=(1000, None)).set_duration(2)
    intro_bg = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(2)
    intro_voice_path = generate_voice(data_string, "intro.mp3")
    intro_audio = load_voice_with_silence(intro_voice_path, 2)
    intro = CompositeVideoClip([intro_bg, intro_text.set_position("center").fadein(0.5)]).set_duration(2).set_audio(intro_audio)
    clips.append(intro)

    for idx, img_file in enumerate(image_names):
        rank = num_items - idx
        img_path = os.path.join(images_folder, img_file)

        image_clip = ImageClip(img_path).set_duration(4)
        zoomed = image_clip.fx(resize, height=2200).fx(crop, x_center=540, y_center=960,
                                                       width=1080, height=1920).set_duration(4)

        number_text = TextClip(f"#{rank}", fontsize=180, font="Impact", color='white',
                               stroke_color='black', stroke_width=5).set_position(("center", 80)).fadein(0.3).set_duration(4)

        voice_path = generate_voice(f"Number {rank}", f"voice{idx+1}.mp3")
        voice_audio = load_voice_with_silence(voice_path, 4)

        final = CompositeVideoClip([zoomed, number_text]).set_duration(4).fadein(0.5).fadeout(0.5).set_audio(voice_audio)
        clips.append(final)

        if idx < num_items - 1:
            transition = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(0.4).fadein(0.2).fadeout(0.2)
            clips.append(transition)

    final_video = concatenate_videoclips(clips, method="compose")
    video_duration = final_video.duration

    if os.path.exists(bgm_path):
        bgm = AudioFileClip(bgm_path).volumex(0.1).set_duration(video_duration)
        if final_video.audio:
            final_video = final_video.set_audio(CompositeAudioClip([final_video.audio, bgm]))
        else:
            final_video = final_video.set_audio(bgm)

    final_video.write_videofile(dynamic_output, fps=30)

    finished_dir = "video_finished"
    os.makedirs(finished_dir, exist_ok=True)
    for img in image_names:
        shutil.move(os.path.join(images_folder, img), os.path.join(finished_dir, img))

    return dynamic_output, num_items, image_names

# === MAIN ===
if __name__ == "__main__":
    selected_images = prepare_images("final_images", "video_images", "video_finished", max_images=5)

    if not selected_images:
        print("❌ No new unique images found in final_images.")
    else:
        print("✅ Using the following images for this video:")
        for img in selected_images:
            print(f" - {img}")

        cleaned_names = [os.path.splitext(img)[0].replace("_", " ").replace("-", " ") for img in selected_images]
        combined_description = ", ".join(cleaned_names)

        video_path, item_count, used_images = create_short_video(
            images_folder="video_images",
            image_names=selected_images,
            output_path="short_final.mp4",
            bgm_path="bgm.mp3"
        )

        description_for_model = f"This video features {item_count} useful Amazon desk items: {combined_description}."
        caption_data = generate_youtube_caption_custom(description_for_model, item_count)

        print("\n=== ✅ YOUTUBE TITLE ===\n", caption_data["title"])
        print("\n=== ✅ YOUTUBE CAPTION ===\n", caption_data["caption"])
