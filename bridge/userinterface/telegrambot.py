
from telegram.ext import Updater, CommandHandler

from database.databaseAPI import DatabaseAPI
from tools.fileConverter import CSVtoXLSX
from userinterface.telegramconfig import BOTKEY, chatID

class TelegramBot:
    def __init__(self):
        self.db = DatabaseAPI()
        self.db.connect()

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help_command(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def export_acquisition(self, update, context):
        csv_path = self.db.export_acquisition()
        chat_id = update.message.chat_id
        xlsx_path = CSVtoXLSX(csv_path)
        file = open(xlsx_path, 'rb')
        self.dp.bot.send_document(chat_id=chat_id, document=file)

    def export_acquisition_point(self, update, context):
        csv_path = self.db.export_acquisition_point()
        chat_id = update.message.chat_id
        xlsx_path = CSVtoXLSX(csv_path)
        file = open(xlsx_path, 'rb')
        self.dp.bot.send_document(chat_id=chat_id, document=file)

    def list_acquisition_point(self, update, context):
        acquisition_points = self.db.list_acquisition_points()
        for code in acquisition_points:
            update.message.reply_text(code)

    # def get_last_acquisition(self, update, context):
    #     update.message.reply_text("inserire il codice del punto di raccolta interessato:")
    #     ap_number = self.db.get_number_acquisition_points(user_input)
    #     if ap_number is not None:
    #         if ap_number == 0:
    #             update.message.reply_text("Non sono presenti punti di raccolta con questo codice")
    #         else:
    #             if ap_number > 0:
    #                 last_acquisition = self.db.get_last_acquisition(user_input)
    #                 if last_acquisition is None:
    #                     update.message.reply_text("Non sono presenti acquisizioni nel punto di raccolta %s" %user_input)
    #                 else:
    #                     update.message.reply_text(last_acquisition.tostring())

    def startBot(self):
        global updater
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True
        updater = Updater(BOTKEY, use_context=True)

        # Get the dispatcher to register handlers  (callbacks)
        self.dp = updater.dispatcher

        # add an handler for each command
        # start and help are usually defined
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("help", self.help_command))
        self.dp.add_handler(CommandHandler("export_acquisizioni", self.export_acquisition))
        self.dp.add_handler(CommandHandler("export_puntiraccolta", self.export_acquisition_point))
        self.dp.add_handler(CommandHandler("list_puntiraccolta", self.list_acquisition_point))
        self.dp.add_handler(CommandHandler("ultima_acquisizione", self.get_last_acquisition))
        # Start the Bot (polling of messages)
        # this call is non-blocking
        updater.start_polling()

        return updater


if __name__ == '__main__':
    tbot = TelegramBot()
    tupdater = tbot.startBot()
    # idle (blocking)
    tupdater.idle()
