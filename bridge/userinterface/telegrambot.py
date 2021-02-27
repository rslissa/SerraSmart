from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from database.databaseAPI import DatabaseAPI
from tools.fileConverter import CSVtoXLSX
from userinterface.telegramconfig import BOTKEY

LA = range(1)
class TelegramBot:
    def __init__(self):
        self.db = DatabaseAPI()
        self.db.connect()

    def start(self, update, context):
        update.message.reply_text('Ciao!')
        update.message.reply_text('Mi occuperò di inviarti le notifiche e gli errori (speriamo pochi) '
                                  'dell\'architettura HydroHouse!')
        update.message.reply_text('Oltre alla visualizzazione delle notifiche, il Bot permette anche '
                                  'eseguire alcuni comandi: \n'
                                  '/export_acquisizioni - ritorna un file contenente tutte le acquisizioni \n'
                                  '/export_puntiraccolta - ritorna un file contenente i punti raccolta \n'
                                  '/list_puntiraccolta - ritorna i nomi dei punti raccolta esistenti \n'
                                  '/ultima_acquisizione - ritorna i dettagli dell\'ultima acquisizione del punto di '
                                  'raccolta specificato \n')

    def help_command(self, update, context):
        update.message.reply_text('Ciao!')
        update.message.reply_text('Mi occuperò di inviarti le notifiche e gli errori (speriamo pochi) '
                                  'dell\'architettura HydroHouse!')
        update.message.reply_text('Oltre alla visualizzazione delle notifiche, il Bot permette anche '
                                  'eseguire alcuni comandi: \n'
                                  '/export_acquisizioni - ritorna un file contenente tutte le acquisizioni \n'
                                  '/export_puntiraccolta - ritorna un file contenente i punti raccolta \n'
                                  '/list_puntiraccolta - ritorna i nomi dei punti raccolta esistenti \n'
                                  '/ultima_acquisizione - ritorna i dettagli dell\'ultima acquisizione del punto di '
                                  'raccolta specificato \n')

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

    def get_last_acquisition(self, update, context):
        update.message.reply_text("inserire il punto di raccolta:")
        return LA

    def query_last_acquisition(self, update, context):
        user_input = update.message.text
        ap_number = self.db.get_number_acquisition_points(user_input)
        if ap_number is not None:
            if ap_number == 0:
                update.message.reply_text("Non sono presenti punti di raccolta con codice  %s. \n"
                                          "Digita /list_puntiraccolta per avere una lista dei punti di raccolta"
                                          % user_input)
            else:
                if ap_number > 0:
                    last_acquisition = self.db.get_last_acquisition(user_input)
                    if last_acquisition is None:
                        update.message.reply_text("Non sono presenti acquisizioni nel punto di raccolta %s" % user_input)
                    else:
                        message = ("punto di raccolta:         {0} \n"
                                   "data:                               {1} \n"
                                   "ora:                                 {2} \n"
                                   "EC:                                  {3} us/cm \n"
                                   "flusso acqua:                 {4} L/min \n"
                                   "temperatura terreno:    {5} °C \n"
                                   "umidità terreno:            {6} % \n"
                                   "temperatura aria:          {7} °C \n"
                                   "umidità aria:                  {8} % \n"
                                   .format(last_acquisition.acquisition_point,
                                           last_acquisition.datetime.strftime("%d/%m/%Y"),
                                           last_acquisition.datetime.strftime("%H:%M:%S"),
                                           round(last_acquisition.EC, 2),
                                           round(last_acquisition.WF, 2),
                                           round(last_acquisition.GT, 2),
                                           round(last_acquisition.GH, 2),
                                           round(last_acquisition.AT, 2),
                                           round(last_acquisition.AH, 2)))

                        update.message.reply_text(message)

        return ConversationHandler.END


    def startBot(self):
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
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('ultima_acquisizione', self.get_last_acquisition)],
            fallbacks=[],

            states={
                LA: [MessageHandler(Filters.text, self.query_last_acquisition)],
            },
        )

        self.dp.add_handler(conv_handler)

        # Start the Bot (polling of messages)
        # this call is non-blocking
        updater.start_polling()

        return updater


if __name__ == '__main__':
    tbot = TelegramBot()
    tupdater = tbot.startBot()
    # idle (blocking)
    tupdater.idle()
