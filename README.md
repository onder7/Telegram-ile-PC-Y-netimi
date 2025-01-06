Tabii, işte blogunuzda yayınlayabileceğiniz bir makale örneği:

---

# **Telegram ile PC Yönetimi: Kendi Botunuzu Geliştirin**

Telegram, sadece bir mesajlaşma uygulaması olmanın ötesinde, sunduğu Bot API'si ile birçok otomasyon işlemini kolayca gerçekleştirebileceğiniz bir platform haline geldi. Bu makalede, Telegram üzerinden bilgisayarınızı yönetebileceğiniz bir botun nasıl geliştirileceğini adım adım anlatacağım. Bu bot sayesinde bilgisayarınızı uzaktan kapatabilir, yeniden başlatabilir, ekran görüntüsü alabilir ve hatta kameradan görüntü elde edebilirsiniz. Hadi başlayalım!

---

## **Neler Yapacağız?**

Bu projede, Python programlama dili ve Telegram Bot API'si kullanarak aşağıdaki özelliklere sahip bir bot geliştireceğiz:

1. **Bilgisayarı Kapatma/Yeniden Başlatma**: Bilgisayarınızı uzaktan kapatabilir veya yeniden başlatabilirsiniz.
2. **Ekran Görüntüsü Alma**: Bilgisayarınızın ekran görüntüsünü alıp Telegram üzerinden gönderebilirsiniz.
3. **Kameradan Görüntü Alma**: Bilgisayarınızın kamerasını açarak görüntü alabilirsiniz.
4. **Komut Çalıştırma**: Bilgisayarda komut satırı komutlarını çalıştırabilirsiniz.

---

## **Gereksinimler**

Projeyi geliştirmek için aşağıdaki araçlara ihtiyacınız olacak:

1. **Python** (3.6 veya üzeri)
2. **Telegram Bot API** (BotFather ile bot oluşturulacak)
3. **Gerekli Python Kütüphaneleri**:
   ```bash
   pip install python-telegram-bot pyautogui opencv-python
   ```

---

## **1. Telegram Bot Oluşturma**

İlk adım, Telegram üzerinde bir bot oluşturmak. Bunun için:

1. Telegram'da **BotFather**'ı arayın ve başlatın.
2. `/newbot` komutunu gönderin.
3. Botunuz için bir ad ve kullanıcı adı belirleyin.
4. BotFather size bir **API Token** verecek. Bu token'i kaydedin, çünkü botunuzu yönetmek için gerekecek.

---

## **2. Proje Yapısı**

Botumuz, aşağıdaki bileşenlerden oluşacak:

- **Yetkilendirme Mekanizması**: Sadece yetkili kullanıcılar botu kullanabilecek.
- **Komutlar**: Bilgisayarı kapatma, ekran görüntüsü alma gibi işlevler.
- **Güvenlik**: Yetkisiz erişimi engellemek için önlemler.

---

## **3. Kodun Adım Adım Açıklanması**

### **a. Gerekli Kütüphanelerin İçe Aktarılması**

Öncelikle, projemiz için gerekli kütüphaneleri içe aktarıyoruz:

```python
import os
import subprocess
import logging
import pyautogui
import cv2
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
```

### **b. Yetkilendirme Mekanizması**

Botun sadece belirli kullanıcılar tarafından kullanılmasını sağlamak için bir yetkilendirme mekanizması ekliyoruz:

```python
AUTHORIZED_USER_IDS = [123456789]  # Yetkili kullanıcı ID'leri

def is_authorized(update: Update):
    return update.message.from_user.id in AUTHORIZED_USER_IDS
```

### **c. Bot Komutları**

Botun temel komutlarını tanımlıyoruz:

#### **/start**: Botu başlatır.
```python
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! PC yönetim botuna hoş geldiniz.")
```

#### **/shutdown**: Bilgisayarı kapatır.
```python
async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_authorized(update):
        await update.message.reply_text("Bilgisayar kapatılıyor...")
        os.system("shutdown /s /t 1")
    else:
        await update.message.reply_text("Yetkiniz yok.")
```

#### **/screenshot**: Ekran görüntüsü alır.
```python
async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_authorized(update):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        await update.message.reply_photo(photo=open("screenshot.png", "rb"))
    else:
        await update.message.reply_text("Yetkiniz yok.")
```

#### **/webcam**: Kameradan görüntü alır.
```python
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
```

#### **/cmd**: Komut çalıştırır.
```python
async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_authorized(update):
        command = " ".join(context.args)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        await update.message.reply_text(f"Komut çıktısı:\n{result.stdout}")
    else:
        await update.message.reply_text("Yetkiniz yok.")
```

### **d. Botu Başlatma**

Son olarak, botu başlatıyoruz:

```python
def main():
    application = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    # Komutlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shutdown", shutdown))
    application.add_handler(CommandHandler("screenshot", screenshot))
    application.add_handler(CommandHandler("webcam", webcam))
    application.add_handler(CommandHandler("cmd", cmd))

    # Botu başlat
    application.run_polling()

if __name__ == "__main__":
    main()
```

---

## **4. Botu Çalıştırma**

1. Kodu bir Python dosyasına kaydedin (örneğin, `pc_bot.py`).
2. Terminalde dosyayı çalıştırın:
   ```bash
   python pc_bot.py
   ```
3. Telegram'da botunuzu başlatın ve komutları kullanın.

---

## **5. Güvenlik Önerileri**

- **Bot Token'ını Koruyun**: Bot token'ınızı asla paylaşmayın.
- **Yetkilendirme Mekanizması**: Sadece yetkili kullanıcıların botu kullanmasına izin verin.
- **Hassas Komutları Sınırlandırın**: Bilgisayarı kapatma gibi hassas komutları sadece güvendiğiniz kullanıcılara açın.

---

## **Sonuç**

Bu makalede, Telegram üzerinden bilgisayarınızı yönetebileceğiniz bir botun nasıl geliştirileceğini adım adım anlattık. Bu bot sayesinde bilgisayarınızı uzaktan kontrol edebilir ve çeşitli işlemler gerçekleştirebilirsiniz. Projeyi geliştirerek daha fazla özellik ekleyebilir ve kendi ihtiyaçlarınıza göre özelleştirebilirsiniz.

Eğer bu projeyi denerseniz, deneyimlerinizi yorumlarda paylaşmayı unutmayın. Bir sonraki makalede görüşmek üzere!

---

**Ek Kaynaklar:**
- [Telegram Bot API Dokümantasyonu](https://core.telegram.org/bots/api)
- [Python Telegram Bot Kütüphanesi](https://github.com/python-telegram-bot/python-telegram-bot)
- [OpenCV Dokümantasyonu](https://docs.opencv.org/)
- [PyAutoGUI Dokümantasyonu](https://pyautogui.readthedocs.io/)

---

Umarım bu makale, okuyucularınız için faydalı olur! Başka sorularınız varsa bana her zaman ulaşabilirsiniz. 😊
