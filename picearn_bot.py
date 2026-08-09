import os
import time
import random
import string
import requests
from groq import Groq

# ---------------- CREDENTIALS ----------------
SUPABASE_URL = "https://ahjdbwntjfteycjoezxi.supabase.co/rest/v1/images?columns=%22user_id%22%2C%22title%22%2C%22description%22%2C%22tags%22%2C%22category%22%2C%22image_url%22%2C%22slug%22%2C%22views%22%2C%22downloads%22%2C%22reward_points%22%2C%22file_size%22%2C%22mime_type%22&select=*"
APIKEY = "sb_publishable_zgeCf0hWa4gfzuY4n7uPFA_YBTf3g5-"
USER_ID = "4d28565f-4c4c-40b2-9d14-95e18ef19a50"

# Pinterest Direct Integration via Session Cookie
PINTEREST_SESS_COOKIE = "TWc9PSZmZ1VlcDEya3hCWXNYZnNodXZQMGwrcWFHMzVDLytGc1lZaENSVFJxRWFGVU1BUFBYSHBsMWFNRll4OXMvNGMwMktPSzMyaXVOcmNLQS92Ky9Ua0E2Z2FncENodFhhK29Gd01oZVg4NG1DR1UxdlIwTDdSVklFOVI4OHd1MjFpRDUxNVlieVY4RjcwZ3lxczFhV2hSZEFPT2ZlYWZlNVdmU2FoMEFyTGpNZXIwRTk4YXR2ZHBybkNDSjQxYnpuOXVjQVlZVEJWRlRnZnVZVkt0OW1yeVkrS3plMUhvVW9mVXBiaXNMTjVmVUhuSUNYdHdEYWZvcFR1SlVianRDdGhoM3ppL1hvOHNhVnA3d0I2T0w3R3lmVTVYZ1o1TklVeW13S1FzelVuRHNtRGhBMmdudVR5OURodVNuQklSdy9vUEhPZ1U3dHY4MUdIdjBkU0NKVTJOdlkrcnd5bjlRb2FodWxhUlFZbDdKM0s5b09oTHVTYW80c3REM1VuM2Q4QlF6Vk9XSi9HdUhWQTVnbTZVZ1V6SXVFTWNVNU1SdVlCdEJaQUxudGltL2tKMkRCcTZ0T0o2M3VNSURXMmtJNW5aVnVhMkFRV0FOTTRFTDVnTFNvaHphc1Fwc2FOa2JpWm96TEM5SGQvQnIrakJkbjVVUy9uMXNZZ3hhZFU1M2YxRGVKaEk5MjNtT3RZSUsrdnBqMjhiK2J1VllSOTY4MGMrUWxXOHdUODVEM2YrZnRFNE1PRmFXZ2dudlRtZWpudFM2ZzFnaG0xZEcwN0ZBZHlqWXFYOXF2Wk84TUhlSG1HR3FLNXRaWHcwc1JDdFRXa3Q2bTlFdUNybG5OM1pFbzVZSWo5MEE2cHdJTm43aW9iQUxSNGx0eGxJS2Y4QlYyUWpFYjFFUFRQK2tTOXBzRTZMMGxoWWlpTnhYVDRzZmVrTlh5VXlGbVNFYnR1TTI3a3dUVUVrNThsWWFLZ1FFMUdQMjRlbHMwUUdiL0lmTFJhRFhkQ3dKaHRsS0dKQWFrWEZRd0k2Mi9McW5TOXpWeS9tdjRhMzlXYWdISjk5dzFZMU9LQzdlQlhyR1E3NjhDWU1sdWM3UGs0M2lxUHJYM1dOSnZaS2lqZnNLeDA1UnlWKzdPUlUwNkJtd0NxZWVUZTZJMDNQNHlRL0c4SmJGdHd2WDBEUzgya0RLR29ZS3oyVTBPNm0xd1kxUHdIcG8vWnhNOTRIZ24xSUM3NHl0eWM0QWVyUHFuTkorVUxlRTJDU3FmMXpEeFZFbCtIWHV1LzdzYkpmUEZ3NDV0QUlDT1ZQM1Y4VWtFWmkycHJFS1NoYXJCRG9Wck5wMGFlT3FhOElMYVZzQitzMDZhRDVkMW16OUpXUW5ORFZhbEdqQ29mWlZmeXlZVndHNzhqNzhNTnh0biszRXNOdTBVaTBsKzQ5a0lKQlRzTm9vRFI3QjhwUUdIQ1prOEc3Y3d0UHVLWFZpbmw3b3BpeFBIbkpIcm1rVEJSQitmV2ZzMjBnZ0tkU1IxRmVSNEFNaC9nWjJaZC8zeGlpZW9qZTh3U3dwcGpVeWEvV3Fuc2FYbFNrcFRNQmQvci8yUE1DallPMG1vYXBNaitQSTk3NzlXYjYwMjNLWGFNeUx0Rno2SjNWUUVPL2dQZmpmTVlhQ0FDeDlSa3UzemNNbk95MFR4ZStqOUJpSDFaNjUxVnFCZUFGaWFwN1NEaGRTc05ZVHcySy9vSm51TS92bE1RVzMrcEVRdmE0MU5VTzFONGZkbVRCZlE4WFRvcVc3SS8yMnZTcGE0QnAmbmFyenU3ZldMS0F1UjV4b0JUSG1Odjl4Rmc4PQ=="
PINTEREST_BOARD_ID = "1143492230328579966"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

HISTORY_FILE = "history.txt"

# अलग-अलग कैटेगरी की लिस्ट ताकि हर बार सब्जेक्ट चेंज हो
CATEGORIES = [
    "A portrait of a person from history or a fantasy figure",
    "A landscape with mountains, rivers, oceans, or waterfalls",
    "A cozy indoor still life with vintage items, flowers, or books",
    "A bustling city street, ancient market, or Venetian canal",
    "A serene nature scene like a deep forest, sunflower field, or autumn park",
    "A dramatic sea storm with ships, lighthouses, or rocky shores"
]

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return set(line.strip().lower() for line in f if line.strip())

def save_to_history(prompt_text):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{prompt_text.strip()}\n")

def generate_random_slug(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def clean_string(text):
    if not text:
        return ""
    text = text.replace('\n', ' ').replace('\r', ' ').replace('"', "'").strip()
    return " ".join(text.split())

def generate_unique_theme(history_set):
    # हर बार एक अलग रैंडम कैटेगरी चुनो
    chosen_category = random.choice(CATEGORIES)
    
    for attempt in range(5):
        idea_prompt = (
            f"Generate a unique, colorful, and vivid concept for a classical oil painting. "
            f"The theme MUST be based on this category: '{chosen_category}'. "
            f"Make sure it is visually unique and different from previous paintings. "
            f"Output ONLY the 1-sentence painting description."
        )
        try:
            res = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": idea_prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.95
            )
            theme = clean_string(res.choices[0].message.content)
            if theme.lower() not in history_set and len(theme) > 10:
                return theme
        except Exception as e:
            print(f"⚠️ Groq Theme Generation Error: {e}")
            break
            
    # Varied Backups (अगर AI फ़ेल भी हो जाए तो भी कभी सेम फ़ोटो नहीं बनेगी)
    diverse_backups = [
        "A peaceful Venetian canal with gondolas reflecting sunset colors",
        "A blooming sunflower field under a bright golden morning sun",
        "A royal Renaissance noblewoman in an elegant silk gown",
        "A rustic wooden table with fruits, wine bottle, and candle glow",
        "A vibrant tropical beach with palm trees and ocean waves at dusk",
        "A magical misty forest with rays of sunlight breaking through trees",
        "A cozy Parisian street cafe illuminated by warm evening lanterns",
        "A snow-capped Alpine mountain peak glowing under sunrise light",
        "An ancient Indian palace courtyard with peacocks and fountains",
        "A vintage steam train crossing a stone bridge over a green valley"
    ]
    
    random.shuffle(diverse_backups)
    for bt in diverse_backups:
        if bt.lower() not in history_set:
            return bt
            
    return f"A unique fine art painting of {chosen_category} {random.randint(1000, 9999)}"

def post_to_pinterest_direct(title, description, destination_url, image_url, retries=2):
    session = requests.Session()
    session.cookies.set("_pinterest_sess", PINTEREST_SESS_COOKIE, domain=".pinterest.com")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "X-Pinterest-AppState": "active",
        "Referer": "https://www.pinterest.com/"
    }

    try:
        session.get("https://www.pinterest.com/", headers=headers, timeout=10)
        csrf_token = session.cookies.get("csrftoken", default="csrftoken")
    except Exception:
        csrf_token = "1"

    headers["X-CSRFToken"] = csrf_token
    endpoint = "https://www.pinterest.com/resource/PinResource/create/"
    
    payload_data = {
        "options": {
            "board_id": str(PINTEREST_BOARD_ID),
            "title": title[:100],
            "description": description[:500],
            "link": destination_url,
            "image_url": image_url,
            "method": "scraped",
            "scrape_metric": {"source": "pinner_upload"}
        },
        "context": {}
    }

    for attempt in range(1, retries + 2):
        try:
            res = session.post(
                endpoint, 
                headers=headers, 
                data={"data": requests.compat.json.dumps(payload_data)},
                timeout=25
            )
            if res.status_code == 200 and "data" in res.json().get("resource_response", {}):
                pin_id = res.json()["resource_response"]["data"].get("id")
                print(f"📌 SUCCESS! Direct Pinned to Pinterest ID: {pin_id}")
                return True
            elif res.status_code == 504 and attempt <= retries:
                print(f"🔄 Timeout 504. Retrying attempt {attempt}/{retries} in 4 seconds...")
                time.sleep(4)
            else:
                print(f"⚠️ Direct Pin Response Code: {res.status_code}, Response: {res.text[:150]}")
                break
        except Exception as e:
            if attempt <= retries:
                print(f"🔄 Network glitch. Retrying {attempt}/{retries}...")
                time.sleep(3)
            else:
                print(f"❌ Error Posting to Pinterest: {e}")
    return False

def generate_and_upload(index, history_set):
    selected_theme = generate_unique_theme(history_set)
    print(f"\n🎨 [{index}/5] Generating Content for NEW Theme: '{selected_theme}'...")
    
    desc_prompt = f"Write a comprehensive, engaging SEO description of AT LEAST 150 WORDS for a classical oil painting depicting '{selected_theme}'. Describe brushstrokes, lighting, and texture. End with hashtags #oilpainting #artgallery #fineart #wallart #masterpiece."

    try:
        res_desc = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": desc_prompt}],
            model="llama-3.1-8b-instant"
        )
        description_text = clean_string(res_desc.choices[0].message.content)
    except Exception:
        description_text = f"Immerse yourself in the timeless beauty of this exquisite classical oil painting capturing {selected_theme}. Hand-crafted with meticulous detail, this masterpiece showcases dramatic brushwork, vivid color palettes, and captivating lightplay on textured canvas. #oilpainting #fineart #artgallery #classicalart #wallart #masterpiece"

    title_prompt = f"Create a short SEO title (5-7 words) for an oil painting about '{selected_theme}'. Output ONLY the title."
    try:
        res_title = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": title_prompt}],
            model="llama-3.1-8b-instant"
        )
        title_text = clean_string(res_title.choices[0].message.content)
    except Exception:
        title_text = f"Masterpiece Oil Painting - {selected_theme[:30]}"

    slug = generate_random_slug()
    download_url = f"https://picearn-9xoo.vercel.app/v/{slug}"

    print(f"🖼️ Title: {title_text}")

    # Seed + Prompt combination ensures 100% unique visual generation
    seed = random.randint(100000, 999999)
    full_art_prompt = f"authentic fine art oil painting on textured canvas, thick impasto brushstrokes, palette knife technique, masterpiece fine art, vibrant colors, realistic oil paint shine, {selected_theme}"
    image_prompt = requests.utils.quote(full_art_prompt)
    direct_image_url = f"https://image.pollinations.ai/prompt/{image_prompt}?width=1080&height=1350&model=flux&nologo=true&seed={seed}"

    headers = {
        'accept': 'application/vnd.pgrst.object+json',
        'apikey': APIKEY,
        'authorization': f'Bearer {APIKEY}',
        'content-profile': 'public',
        'content-type': 'application/json',
        'origin': 'https://picearn-9xoo.vercel.app',
        'prefer': 'return=representation',
        'referer': 'https://picearn-9xoo.vercel.app/'
    }

    payload = [{
        "user_id": USER_ID,
        "title": title_text,
        "description": description_text,
        "tags": "oilpainting,fineart,canvas,wallpaper,artgallery",
        "category": "Art",
        "image_url": direct_image_url,
        "slug": slug,
        "views": 0,
        "downloads": 0,
        "reward_points": 0.1,
        "file_size": 420000,
        "mime_type": "image/jpeg"
    }]

    response = requests.post(SUPABASE_URL, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print(f"🚀 SUCCESS! Posted to PicEarn: {title_text}")
        print(f"🔗 Download Link: {download_url}")
        
        save_to_history(selected_theme)
        history_set.add(selected_theme.lower())
        
        post_to_pinterest_direct(
            title=title_text,
            description=description_text,
            destination_url=download_url,
            image_url=direct_image_url
        )
    else:
        print(f"❌ Upload Failed! Code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    history_set = load_history()
    print(f"📚 Loaded {len(history_set)} previously generated concepts from history.txt")
    
    for i in range(1, 6):
        generate_and_upload(i, history_set)
        if i < 5:
            print("🛑 Waiting 12 seconds before next upload...")
            time.sleep(12)