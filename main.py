import telebot
from flask import Flask
from threading import Thread

# Telegram Bot Token
BOT_TOKEN = "7292391889:AAEwUuw5WfF2loeLys3OiAF0kIjye6DIkms"  # ඔබේ Bot Token එක
bot = telebot.TeleBot(BOT_TOKEN)

# Admin ID
ADMIN_ID = 5491775006  # Admin ID

# File storage dictionary
shared_files = {}

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if len(message.text.split()) > 1:  # Check for file ID
        file_id = message.text.split()[1]
        if file_id in shared_files:
            file_data = shared_files[file_id]
            bot.send_document(
                message.chat.id,
                file_data["file_id"],
                caption=f"📂 {file_data['caption']}"
            )
        else:
            bot.reply_to(message, "❌ File not found.")
    else:
        bot.reply_to(
            message,
            "👋 Hi! Welcome to the File Sharing Bot.\n\n📁 Admin can upload files, and users can download them via unique links.\n\nCommands:\n"
            "/help - Get Help"
        )

# Help Command
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(
        message,
        "📋 Help Menu:\n"
        "1. Admin can send files to generate unique links.\n"
        "2. Users can click the shared link to download the file."
    )

# Handle File Upload (Admin Only)
@bot.message_handler(content_types=['document', 'audio', 'video', 'photo'])
def handle_files(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Only the admin can upload files.")
        return

    file_id = None
    file_name = "file"
    caption = message.caption or "No caption provided."

    # Check file type and save ID
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
    elif message.audio:
        file_id = message.audio.file_id
        file_name = message.audio.file_name or "audio.mp3"
    elif message.video:
        file_id = message.video.file_id
        file_name = message.video.file_name or "video.mp4"
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_name = "photo.jpg"

    if file_id:
        unique_id = f"{message.chat.id}_{message.message_id}"  # Unique identifier
        shared_files[unique_id] = {"file_id": file_id, "caption": caption}

        bot.reply_to(
            message,
            f"✅ File '{file_name}' uploaded successfully!\n\n🔗 Share this link:\n"
            f"https://t.me/{bot.get_me().username}?start={unique_id}\n\n📄 Caption: {caption}"
        )

# Flask server to keep bot alive
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Keep bot alive
keep_alive()

# Run the bot
print("🤖 Bot is running...")
bot.infinity_polling()
