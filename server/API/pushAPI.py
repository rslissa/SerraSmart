from requests import post, get
import config


class PushAPI:
    def __init__(self):
        self.HOST = config.LOCALHOST_API

    def valid(self, parameter):
        if parameter is not None:
            return True
        else:
            return False

    def post_roof_and_irrigation(self, acquisition_point, roof, irrigation):
        if not self.valid(acquisition_point) or not self.valid(roof) or not self.valid(irrigation):
            return None
        else:
            r = None
            try:
                r = post(f"{self.HOST}/ap/{acquisition_point}/roof/{roof}/irrigation/{irrigation}")
            except:
                return r.status_code

        return 200

    def get_roof_and_irrigation(self, acquisition_point):
        if not self.valid(acquisition_point):
            return None
        else:
            r = get(f"{self.HOST}/ap/{acquisition_point}").json()
            if r is None:
                return r.status_code

            roof = r[acquisition_point]['roof']
            irrigation = r[acquisition_point]['irrigation']

        return roof, irrigation

'''
if __name__ == '__main__':
    print(PushAPI().get_roof_and_irrigation("A01"))
'''