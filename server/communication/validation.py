from marshmallow import Schema, fields, ValidationError


class InsideSchema(Schema):
    id = fields.Integer(required=True, allow_none=False, validate=lambda x: x > 0)
    datetime = fields.Str(required=True, allow_none=False)
    acquisition_point = fields.Str(required=True, allow_none=False, validate=lambda x: len(x) == 3)
    EC = fields.Float(required=True, allow_none=True)
    WF = fields.Float(required=True, allow_none=True)
    GT = fields.Float(required=True, allow_none=True)
    GH = fields.Float(required=True, allow_none=True)
    AT = fields.Float(required=True, allow_none=True)
    AH = fields.Float(required=True, allow_none=True)


class OutsideSchema(Schema):
    message = fields.Nested(InsideSchema())


def validBody(json):
    try:
        ret = OutsideSchema().load(json)
    except ValidationError:
        return None
    return ret


'''
if __name__ == '__main__':
    json = {
        "message": {
            "id": 217,
            "datetime": "2021-02-11T10:11:05.700700",
            "acquisition_point": "A01",
            "EC": 742.913000977517,
            "WF": 4.63489736070381,
            "GT": None,
            "GH": 4.6,
            "AT": None,
            "AH": 3.2
        }
    }

    print(validBody(json)['message']['id'])
'''
