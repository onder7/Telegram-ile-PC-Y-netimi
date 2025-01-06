import os

import subprocess

import logging

import pyautogui

import cv2

from telegram import Update

from telegram.ext import Application, CommandHandler, ContextTypes


 

# Telegram Bot Token

TOKEN = "*******************"


 

# Yetkili kullanıcı ID'leri

AUTHORIZED_USER_IDS = [12345678]  # Buraya kendi Telegram ID'nizi yazın


 

# Loglama ayarları

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


 

# Yetki kontrolü

def is_authorized(update: Update):

    return update.message.from_user.id in AUTHORIZED_USER_IDS


 

# /start komutu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Merhaba! PC yönetim botuna hoş geldiniz.")


 

# /shutdown komutu

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if is_authorized(update):

        await update.message.reply_text("Bilgisayar kapatılıyor...")

        os.system("shutdown /s /t 1")

    else:

        await update.message.reply_text("Yetkiniz yok.")


 

# /restart komutu

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if is_authorized(update):

        await update.message.reply_text("Bilgisayar yeniden başlatılıyor...")

        os.system("shutdown /r /t 1")

    else:

        await update.message.reply_text("Yetkiniz yok.")


 

# /screenshot komutu

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if is_authorized(update):

        screenshot = pyautogui.screenshot()

        screenshot.save("screenshot.png")

        await update.message.reply_photo(photo=open("screenshot.png", "rb"))

    else:

        await update.message.reply_text("Yetkiniz yok.")


 

# /webcam komutu

async def webcam(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if is_authorized(update):

        cap = cv2.VideoCapture(0)

        ret, frame = cap.read()

        if ret:

            cv2.imwrite("webcam.png", frame)

            await update.message.reply_photo(photo=open("webcam.png", "rb"))

        cap.release()

    else:

        await update.message.reply_text("Yetkiniz yok.")


 

# /cmd komutu (Komut çalıştırma)

async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if is_authorized(update):

        command = " ".join(context.args)

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        await update.message.reply_text(f"Komut çıktısı:\n{result.stdout}")

    else:

        await update.message.reply_text("Yetkiniz yok.")


 

# Botu başlatma

def main():

    application = Application.builder().token(TOKEN).build()


 

    # Komutlar

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("shutdown", shutdown))

    application.add_handler(CommandHandler("restart", restart))

    application.add_handler(CommandHandler("screenshot", screenshot))

    application.add_handler(CommandHandler("webcam", webcam))

    application.add_handler(CommandHandler("cmd", cmd))


 

    # Botu başlat

    application.run_polling()


 

if __name__ == "__main__":

    main()
