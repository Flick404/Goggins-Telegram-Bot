import asyncio
import string
from datetime import datetime
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN: Final = '6731040588:AAEUViofJ5mURXagReuXDA4Q2eV8QKm6cDo'
BOT_USERNAME: Final = "@David_Goggins_Messages_Bot"

# Conversation state
TIME_INPUT = 1

# Messages to be sent
MESSAGES = [
    "Rise, warrior! Your destiny isn't going to wait for you to get enough sleep. It demands action, effort, and relentless drive. Get up and chase it down.",
    "Wake up and smell the battle. Today's another chance to prove yourself, to fight against all odds. Get out of bed and into the arena. It's time to show the world what you're made of.",
    "Today's a gift you're wasting in bed. Get up! Life's a race, and you're stuck at the starting line while everyone else is sprinting. Time to catch up.",
    "Your dreams are calling, and they're fucking pissed you're still in bed. Get up and start making them a reality. Today's not a day for lazy bones.",
    "You're not going to conquer the world by sleeping in. Wake up and start building your empire. Every second counts in the game of life.",
    "Stop hitting snooze like a coward. Face the day like a warrior. Your bed is your enemy right now. Defeat it and start your conquest.",
    "This is your life, not a rehearsal. Every morning you waste is a scene you'll never get back. Get up and make your life a masterpiece.",
    "Wake up, or life's going to kick your ass. You've got mountains to move, and you can't do that under your sheets. Rise and start pushing.",
    "You're not just waking up; you're rising above mediocrity. Every moment in bed is a moment you're not at your best. Get up and excel.",
    "This isn't just a morning; it's a wake-up call to greatness. Your bed is holding you back. Break free and start achieving.",
    "You think today's going to wait for you? Hell no! Get out of bed and start chasing it down. Today's a predator, and you're its prey if you don't move.",
    "Rise and grind! Every dream you have is just outside your comfort zone. That bed is your comfort zone. Get the fuck out and go after your dreams.",
    "Your alarm is sounding the charge. Get up and lead the charge against your own limitations. Today's a day for breaking barriers, not for breaking sleep.",
    "You're sleeping while your dreams are dying. Wake up and save them. Every second in bed is a second they fade away. Rise and make them real.",
    "Get up! Your future's not going to build itself. Every moment you waste is a brick missing from the empire you're meant to build.",
    "Your bed's a liar. It promises comfort but delivers mediocrity. Break free from its grasp and start living a life worth telling stories about.",
    "This morning is a battlefield, and your alarm is the war cry. Get up and fight for your dreams, your goals, your future. Today's not a day for cowards.",
    "Wake up, or get left behind. Life's moving fast, and you're stuck in neutral. Shift into gear and start accelerating towards your goals.",
    "You think winners sleep in? Bullshit. They're out there, grinding while you're dreaming. Time to join the ranks of the relentless.",
    "Today's not just another day; it's a new chance to prove yourself. Get out of bed and seize it with both hands. Today's for the bold, not the sleepy.",
    "Rise! Every second you're in bed, you're telling the world you're okay with being average. Fuck average. Be extraordinary.",
    "Your bed is a trap, a comfort zone that's killing your ambition. Break out and start chasing the life you deserve. No more excuses.",
    "This isn't a vacation, it's life. And life's not going to wait for you to get enough sleep. Get up and start living it to the fullest.",
    "Your alarm's not a suggestion; it's a command. Get the hell up and start facing your challenges head-on. Today's a day for warriors.",
    "You're not just waking up; you're declaring war on mediocrity. Every moment you stay in bed, you're losing ground. Get up and fight back.",
    "Today's not a day for rest; it's a day for battle. Get out of bed and start fighting for your dreams. They're not going to come to you.",
    "Wake up, or you'll sleepwalk through life. You've got a destiny to fulfill, and it's not going to happen in your dreams. Get up and make it happen."
]


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Good choice")

async def SetTime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter a time in 24-hour format (HH:MM).")
    return TIME_INPUT

async def get_time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in context.user_data:
        set_time = context.user_data[user_id]
        await update.message.reply_text(f"You have set your time to: {set_time}")
    else:
        await update.message.reply_text("You haven't set a time yet. Use /settime to set a time.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here are the commands you can use:\n"
        "/start - Get a welcome message.\n"
        "/settime - Set a reminder time.\n"
        "/gettime - Retrieve your set time.\n"
        "/help - Get information about the bot commands.\n"
        "/contact - Learn how to contact the author of the bot."
    )
    await update.message.reply_text(help_text)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Contact author (mention bot name in subject): lionholder@yandex.ru")

# Function to handle the time input
async def handle_time_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    time_input = update.message.text

    if validate_time_format(time_input):
        context.user_data[user_id] = time_input
        await update.message.reply_text("Time set successfully.")

        # Schedule the message sending
        schedule_time = datetime.strptime(time_input, "%H:%M")
        asyncio.create_task(send_messages_at_time(schedule_time, update, context, user_id))

        return ConversationHandler.END
    else:
        await update.message.reply_text("Invalid time format. Please use HH:MM format.")
        return TIME_INPUT

# Function to send messages at the scheduled time
async def send_messages_at_time(schedule_time, update, context, user_id):
    now = datetime.now()
    wait_seconds = (schedule_time - now).total_seconds()
    if wait_seconds > 0:
        await asyncio.sleep(wait_seconds)

        for message in MESSAGES:
            await context.bot.send_message(chat_id=user_id, text=message)

# Validate time format function
def validate_time_format(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# Responses
def handle_response(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    if "hello" in text:
        return "What's up my boy?"
    return "Say that again"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User {update.message.chat.id} in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "")
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot: ", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Conversation handler for settime command
settime_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('settime', SetTime_command)],
    states={
        TIME_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_time_input)],
    },
    fallbacks=[]
)

if __name__ == '__main__':
    print("Starting Bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('contact', contact_command))
    app.add_handler(CommandHandler('gettime', get_time_command))
    app.add_handler(settime_conv_handler)
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval = 3)