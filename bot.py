from telethon import TelegramClient, events, Button
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import os

api_id = '26850724'
api_hash = 'b89dc1ae48cb08103d18266e067ed890'
bot_token = '7000850548:AAH5oF7R6AYdDp5RJCaPiK2-bx5EwygoaG4'

if not os.path.exists('temp'):
    os.makedirs('temp')

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

processing_photos = {}

async def pencil_sketch(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    return cv2.divide(gray, 255 - blurred, scale=256.0)

async def cartoon_effect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    return cv2.bitwise_and(color, color, mask=edges)

async def watercolor_effect(img):
    img_water = cv2.stylization(img, sigma_s=60, sigma_r=0.6)
    return img_water

async def oil_painting(img):
    img_oil = cv2.xphoto.oilPainting(img, 7, 1, dynRatio=1)
    return img_oil

async def emboss_effect(img):
    kernel = np.array([[0,-1,-1],
                      [1,0,-1],
                      [1,1,0]])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.filter2D(gray, -1, kernel)

async def sepia_effect(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                      [0.349, 0.686, 0.168],
                      [0.393, 0.769, 0.189]])
    return cv2.transform(img, kernel)

async def sketch_color(img):
    sk_gray, sk_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    return sk_color

async def invert_effect(img):
    return cv2.bitwise_not(img)

async def blur_effect(img):
    return cv2.GaussianBlur(img, (15, 15), 0)

async def sharpen_effect(img):
    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    return cv2.filter2D(img, -1, kernel)

async def grayscale_effect(img):
    return cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

async def edge_detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

async def vintage_effect(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                      [0.349, 0.686, 0.168],
                      [0.393, 0.769, 0.189]])
    sepia = cv2.transform(img, kernel)
    gaussian_blur = cv2.GaussianBlur(sepia, (7,7), 0)
    return cv2.addWeighted(sepia, 0.7, gaussian_blur, 0.3, 0)

async def winter_effect(img):
    blue_channel = img[:,:,0]
    blue_channel = cv2.add(blue_channel, 30)
    img[:,:,0] = blue_channel
    return img

async def summer_effect(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_hsv[:,:,1] = cv2.add(img_hsv[:,:,1], 30)
    return cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

EFFECTS = {
    'pencil': ('âï¸ ÙØ¯Ø§Ø¯', pencil_sketch),
    'cartoon': ('ð¨ Ú©Ø§Ø±ØªÙÙÛ', cartoon_effect),
    'watercolor': ('ð¦ Ø¢Ø¨Ø±ÙÚ¯', watercolor_effect),
    'oil': ('ð ÙÙØ§Ø´Û Ø±ÙÚ¯ Ø±ÙØºÙ', oil_painting),
    'emboss': ('ð¿ Ø¨Ø±Ø¬Ø³ØªÙ', emboss_effect),
    'sepia': ('ð ÙØ¯ÛÙÛ', sepia_effect),
    'sketch_color': ('ð¨ Ø·Ø±Ø§Ø­Û Ø±ÙÚ¯Û', sketch_color),
    'invert': ('ð ÙØ¹Ú©ÙØ³', invert_effect),
    'blur': ('ð« ÙØ­Ù', blur_effect),
    'sharpen': ('â¨ Ø´Ø§Ø±Ù¾', sharpen_effect),
    'grayscale': ('â«ï¸ Ø³ÛØ§Ù Ù Ø³ÙÛØ¯', grayscale_effect),
    'edge': ('âï¸ ÙØ¨ÙâÛØ§Ø¨Û', edge_detect),
    'vintage': ('ð· ÙÛÙØªÛØ¬', vintage_effect),
    'winter': ('âï¸ Ø²ÙØ³ØªØ§ÙÛ', winter_effect),
    'summer': ('âï¸ ØªØ§Ø¨Ø³ØªØ§ÙÛ', summer_effect),
}

@client.on(events.NewMessage(pattern="ÙÙØ§Ø´Û"))
async def start_process(event):
    if not event.message.is_reply:
        await event.respond("ÙØ·ÙØ§ Ø±ÙÛ ÛÚ© Ø¹Ú©Ø³ Ø±ÛÙ¾ÙØ§Û Ú©ÙÛØ¯")
        return

    replied = await event.get_reply_message()
    if not replied.photo and not replied.document:
        await event.respond("ÙØ·ÙØ§ Ø±ÙÛ ÛÚ© Ø¹Ú©Ø³ Ø±ÛÙ¾ÙØ§Û Ú©ÙÛØ¯")
        return

    photo = await replied.download_media(bytes)
    processing_photos[event.chat_id] = photo

    buttons = [
        [Button.inline(effect[0], data=f"effect_{name}") 
         for name, effect in list(EFFECTS.items())[i:i+2]]
        for i in range(0, len(EFFECTS), 2)
    ]

    await event.respond("ÙØ·ÙØ§ Ø§ÙÚ©Øª ÙÙØ±Ø¯ ÙØ¸Ø± Ø±Ø§ Ø§ÙØªØ®Ø§Ø¨ Ú©ÙÛØ¯:", buttons=buttons)

@client.on(events.CallbackQuery(pattern=r"effect_(.+)"))
async def apply_effect(event):
    effect_name = event.data.decode().split('_')[1]
    
    try:
        photo_data = processing_photos.get(event.chat_id)
        if not photo_data:
            await event.answer("ÙØ·ÙØ§ Ø¯ÙØ¨Ø§Ø±Ù Ø´Ø±ÙØ¹ Ú©ÙÛØ¯")
            return

        await event.edit("Ø¯Ø± Ø­Ø§Ù Ù¾Ø±Ø¯Ø§Ø²Ø´ ØªØµÙÛØ±...")

        image = Image.open(BytesIO(photo_data))
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        effect_func = EFFECTS[effect_name][1]
        processed = await effect_func(img)

        temp_path = f'temp/effect_{effect_name}.jpg'
        cv2.imwrite(temp_path, processed)

        await client.send_file(
            event.chat_id,
            temp_path,
            caption=f"ð¨ Ø§ÙÚ©Øª {EFFECTS[effect_name][0]} Ø§Ø¹ÙØ§Ù Ø´Ø¯!"
        )

        os.remove(temp_path)
        del processing_photos[event.chat_id]

    except Exception as e:
        print(f"Error: {str(e)}")
        await event.respond(f"ÙØªØ£Ø³ÙØ§ÙÙ Ø®Ø·Ø§ÛÛ Ø±Ø® Ø¯Ø§Ø¯. ÙØ·ÙØ§ Ø¯ÙØ¨Ø§Ø±Ù ØªÙØ§Ø´ Ú©ÙÛØ¯.")

    finally:
        await event.answer()

print("Bot is running...")
client.run_until_disconnected()
