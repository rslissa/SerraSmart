class Formatter:
    def __init__(self):
        pass

    def message_formatting(self, acquired):
        if acquired is not None:
            ret = {
                "message": {
                    "id": acquired['id'],
                    "datetime": str(acquired['datetime']),
                    "acquisition_point": acquired['acquisition_point'],
                    "EC": acquired['ec'],
                    "WF": acquired['water_flow'],
                    "GT": acquired['ground_temperature'],
                    "GH": acquired['ground_humidity'],
                    "AT": acquired['air_temperature'],
                    "AH": acquired['air_humidity']
                }
            }

            return ret
        else:
            print('Message formatting error, acquisition None!')
            return
