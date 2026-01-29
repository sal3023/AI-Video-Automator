import os
import sys
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import requests

def create_video(text, image_path="background.jpg"):
    output_video = "ai_output.mp4"
    
    # 1. تحويل النص إلى صوت عربي
    tts = gTTS(text=text, lang='ar')
    tts.save("voice.mp3")

    # 2. بناء الفيديو (دمج الصوت مع الصورة)
    audio = AudioFileClip("voice.mp3")
    
    # التحقق من وجود صورة الخلفية
    if os.path.exists(image_path):
        video = ImageClip(image_path).set_duration(audio.duration)
    else:
        # إذا لم نرفع صورة بعد، سيصنع خلفية سوداء تلقائياً
        from moviepy.editor import ColorClip
        video = ColorClip(size=(1280, 720), color=(0,0,0)).set_duration(audio.duration)
    
    video = video.set_audio(audio)
    video.write_videofile(output_video, fps=24, codec="libx264")
    return output_video

def send_to_telegram(video_path):
    # جلب المفاتيح السرية من إعدادات النظام
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendVideo"
    
    with open(video_path, 'rb') as v:
        files = {'video': v}
        data = {'chat_id': chat_id, 'caption': "تم إنتاج الفيديو بنجاح! 🎬"}
        requests.post(url, files=files, data=data)

if __name__ == "__main__":
    # قراءة النص المرسل أو استخدام نص افتراضي
    script_text = sys.argv[1] if len(sys.argv) > 1 else "مرحباً بك، هذا فيديو تجريبي تم إنتاجه آلياً."
    
    video_file = create_video(script_text)
    
    # إرسال لتيليجرام إذا تم ضبط المفاتيح
    if os.getenv('TELEGRAM_TOKEN'):
        send_to_telegram(video_file)
      
