import logging

from telegram.ext import Updater, CommandHandler
from userinterface.telegramconfig import BOTKEY


class TelegramBot:
    def __init__(self):
        #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logger = logging.getLogger()
        # logger.setLevel(logging.DEBUG)

    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.
    def start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help_command(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def startBot(self):
        global updater
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True
        updater = Updater(BOTKEY, use_context=True)

        # Get the dispatcher to register handlers  (callbacks)
        dp = updater.dispatcher

        # add an handler for each command
        # start and help are usually defined
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help_command))
        # Start the Bot (polling of messages)
        # this call is non-blocking
        updater.start_polling()

        return updater
