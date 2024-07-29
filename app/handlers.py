import os

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
import yt_dlp

# from bot import bot

from aiogram.types import Message, FSInputFile

router = Router()

@router.message(CommandStart())
async def start_main(message:Message):
    await message.answer('Hello!') # change hello

@router.message(F.text == 'Download music from youtube')
async def prompt_for_link(message: Message):
    await message.reply("Please send me the YouTube link you want to download.")

@router.message(F.text.startswith('https://www.youtube.com/watch'))
async def download_music(message: Message):
    url = message.text
    await message.reply('Loading and Converting your mp3')

    #path to download file
    download_path = f"downloads/{message.from_user.id}" #mp3 deleted
    os.makedirs(os.path.dirname(download_path),exist_ok=True) # creating directory

    #yt-dlp settings
    ydl_options = {
        'format':'bestaudio/best',
        #'outtmpl': download_path,
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',  # Сохраняем файл с названием видео
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }], 'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([url]) # taking url from message

            info_dict = ydl.extract_info(url, download=True)  # Извлекаем информацию и скачиваем
            title = info_dict.get('title', 'audio')  #

            #sending audio file to user
            audio = FSInputFile(f'{download_path}/{title}.mp3')

            from bot import bot #importing bot for send audio
            #idk any idea how do it in another way

            await bot.send_audio(chat_id=message.chat.id, audio =audio)

    except Exception as e:
        await message.reply(f'there is [ERROR]{e}')