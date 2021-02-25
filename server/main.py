import communication.mqttClient as to_client
import communication.validation as validate
import communication.encryption as decipher
import communication.dbAccess as db
import thingsBoard.dbThingsBoard as to_dash

util_decrypt = decipher.Encryption()
util_db = db.DBconnection()
util_dash = to_dash.Dashboard()

def processing_message(msg):
    '''
    Ricezione del messaggio:
        - controllo se None
        - decifrazione (testo cifrato -> testo in chiaro)
        - validazione (testo in chiaro -> json)
    '''

    if msg is None:
        return print('Message empty, not processed!')


    plaintext = util_decrypt.decrypt(msg)
    if plaintext is None:
        print('Bad message decription phase!')

    json = validate.validBody(plaintext)
    if json is None:
        return print('Format message error')
    else:
        print('Correct format message')

    print('Message received: ', json)

    #Caricamento del messaggio sul db
    ret = util_db.insert_acquisition(json['message'])
    if ret is None:
        print('Upload db error!')
    else:
        print('Message correctly uploaded to db')


    #Prelievo messaggio dal db
    acq = util_db.retrieve_acquisition()
    if acq is not None:
        #Caricamento messaggio su Dashboard
        util_dash.post_acquisition(acq)
    else:
        print('Retrieving from db failed!')

    return


if __name__ == '__main__':
    '''
    Sequenza di lavoro:
    
    FASE 1:
    - lettura messaggio da broker MQTT
    - decifrazione messaggio -> plaintext -> validazione -> JSON
    - caricamento record sul db
    
    ThingsBoard:
    - lettura record dal db
    - invio record a ThingsBoard tramite API
    
    FbProphet:
    - lettura records dal db
    - caricamento dati su FbPropher
    - previsione
    - invio previsione a ThingsBoard tramite API
    
    REST API: ...
    '''

    ''' LOOP prima versione
    client = mqtt.Client(client_id="Pasquale-receiver", clean_session=False, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.connect(host="broker.mqttdashboard.com", port=1883, keepalive=60, bind_address="")
    #client.on_connect = client.on_connect
    client.on_message = mc.on_message
    client.subscribe(topic="prst/test/fromweb1")
    #client.on_subscribe = c.on_subscribe
    client.loop_forever()'''

    #Per far partire il loop da qui ed avere l'istanza di client
    #client = to_client.connect_mqtt()
    #to_client.subscribe(client)
    #client.loop_forever()

    #Avvio del codice di ricezione dei messaggi senza bisogno dell'istanza client in questo punto
    to_client.run()
