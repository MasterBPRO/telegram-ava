from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.sync import TelegramClient
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
from pytz import timezone
import pyowm


API_ID = "YOUR_API"
API_HASH = "YOU_API_HASH"
SESSION_NAME = "SESION_NAME"
owm = pyowm.OWM('OPENWEATHERMAP_API_KEY')
client = TelegramClient(session=SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
client.start()
client.connect()
now_time = ''


def get_time():
    """
    Function for getting current time, please check the timezone
    """
    return datetime.now(timezone('Europe/Moscow')).strftime('%H:%M')


def get_date():
    """
    Function for getting current date, please check the timezone
    """
    return datetime.now(timezone('Europe/Moscow')).strftime('%d.%m.%Y')


def get_temp():
    """
    Function for getting current temperature in "Celsius", pls check observation
    """
    observation = owm.weather_at_place('Moscow,RU')
    mess = observation.get_weather()
    temp = mess.get_temperature('celsius')['temp']
    return str(temp).split('.')[0]


def get_image(time, date, temp):
    """
    Function for draw image
    """
    img = Image.new('RGB', (500, 500), color='black')
    W, H = img.size
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font='font.otf', size=235)
    wt, ht = draw.textsize(time, font=font)
    draw.text(((W - wt) / 1.9, (H - ht - 60) / 2), time, font=font, fill='#ffffff')

    font = ImageFont.truetype(font='font.otf', size=50)
    draw.text((W / 7, H / 4.6), f"Температура: {temp}°C", font=font, fill='#ffffff')

    font = ImageFont.truetype(font='font.otf', size=78)
    draw.text((W / 4, H / 1.6), date, font=font, fill='#ffffff')

    font = ImageFont.truetype(font='font.otf', size=50)
    draw.text((W / 2.4, H / 1.17), "NICK", font=font, fill='#ffffff')
    img.save('now.jpg')


while True:  # Delete/Upload image
    if not now_time == get_time():
        current_time = get_time()
        now_time = current_time
        get_image(current_time, get_date(), get_temp())
        image = client.upload_file('now.jpg')
        client(DeletePhotosRequest(client.get_profile_photos('me')))
        client(UploadProfilePhotoRequest(image))
