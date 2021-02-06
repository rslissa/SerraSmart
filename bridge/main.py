from microcontroller.serialComunication import Bridge

if __name__ == '__main__':
    br = Bridge()
    br.setup()
    br.loop()



