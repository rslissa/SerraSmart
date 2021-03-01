import communication.validation as validate
import communication.encryption as decipher
import communication.dbAccess as db
import thingsBoard.dbThingsBoard as to_dash
from FbProphet.prevision import Previson

util_decrypt = decipher.Encryption()
util_db = db.DBconnection()
util_dash = to_dash.Dashboard()
util_prevision = Previson()


def processing_message(msg):
    # Ricezione del messaggio:
    #    - controllo se None
    #   - decifrazione (testo cifrato -> testo in chiaro)
    #   - validazione (testo in chiaro -> json)

    if msg is None:
        return 'Message empty, not processed!'
    else:
        print('Received:\n', msg)

    plaintext = util_decrypt.decrypt(msg)
    if plaintext is None:
        return 'Bad message decription phase!'

    json = validate.validBody(plaintext)
    if json is None:
        return 'Format message error'
    else:
        print('Correct format message')

    print('Message received: ', json)

    # Caricamento del messaggio sul db
    ret = util_db.insert_acquisition(json['message'])
    if ret is None:
        return 'Upload db error!'
    else:
        print('Message correctly uploaded to db')

    # Prelievo messaggio dal db
    acq = util_db.retrieve_acquisition()
    if acq is not None:
        # Caricamento messaggio su Dashboard
        util_dash.post_acquisition(acq)
    else:
        return 'Retrieving from db failed!'

    return
