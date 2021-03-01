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
            try:
                r = post(f"{self.HOST}/ap/{acquisition_point}/roof/{roof}/irrigation/{irrigation}")
            except:
                print('API POST not succeded!')

        return 'ok'

    def get_roof_and_irrigation(self, acquisition_point):
        roof = None
        irrigation = None
        if not self.valid(acquisition_point):
            return None
        else:
            try:
                r = get(f"{self.HOST}/ap/{acquisition_point}").json()

                roof = r[acquisition_point]['roof']
                irrigation = r[acquisition_point]['irrigation']
            except:
                print('API GET not succeded!')

        return roof, irrigation

'''
if __name__ == '__main__':
    print(PushAPI().post_roof_and_irrigation("A01", 25, 3))
    print(PushAPI().get_roof_and_irrigation("A01"))
'''