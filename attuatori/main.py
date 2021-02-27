# POST GET

from flask import Flask, abort, jsonify
from config import Config

from databaseAPI import DatabaseAPI

appname = "IOT - sample1"
app = Flask(appname)
myconfig = Config
app.config.from_object(myconfig)

db = DatabaseAPI()
db.connect()

AP_CODE = 'A01'
# ES: {A01:{roof:25,irrigation:45}}


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/ap/<AP>/roof/<roof>/irrigation/<irrigation>', methods=['POST'])
def post_actuators(AP, roof, irrigation):
    try:
        roof = int(roof)
        irrigation = int(irrigation)
    except:
        abort(400, description="roof and irrigation must be integers")

    if AP != AP_CODE:
        abort(400, description="acquisition point must be " + AP_CODE)
    if 0 < int(roof) > 100 or 0 < int(irrigation) > 100:
        abort(400, description="roof and irrigation must be between 0 and 100")

    db.insert_or_update_actuator(AP, {'roof': roof, 'irrigation': irrigation})

    return 'OK'


@app.route('/ap/<AP>', methods=['GET'])
def get_values(AP):
    if AP != AP_CODE:
        abort(400, description="acquisition point must be " + AP_CODE)
    try:
        return jsonify(db.get_actuator(AP))
    except:
        abort(400, description="the acquisition point %s don't exist" % AP)


if __name__ == '__main__':
    port = 10000
    interface = '127.0.0.1'
    app.run(host=interface, port=port)
