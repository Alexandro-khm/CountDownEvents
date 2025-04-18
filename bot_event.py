from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from bot_backend import *
from backend import *


TOKEN = TELEGRAM_TOKEN

async def start(update, context):
    await send_text(update, context, 'Головне меню\n'
                                     'Для відображення усіх подій /events\n'
                                     'Для відображення найближчої події /nearest')
    await show_main_menu(update, context, {
        'start': 'Головне меню',
        'events': 'Показати всі події',
        'nearest': 'Показати найближчу подію'
    })

async def events(update, context):
    events = load_events(JSON_FILENAME)
    events = sort_events(events)
    await send_text(update, context, 'Усі події')
    for event in events:
        time = time_to_go(event['date'], event['time'])
        await send_text(update, context, f"{event['event']} {event['date']} залишилось {time[0]} днів")

async def nearest(update, context):
    events = load_events(JSON_FILENAME)
    events = sort_events(events)
    if not events:
        await send_text(update, context, 'Немає подій у списку')
        return
    else:
        time = time_to_go(events[0]['date'], events[0]['time'])
        await send_text(update,context, f"{events[0]['event']} {events[0]['date']} {time[0]} днів")



async def hello(update, context):
    await send_text(update, context, 'Привіт набери /start для початку роботи')


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('events', events))
app.add_handler(CommandHandler('nearest', nearest))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.run_polling()
