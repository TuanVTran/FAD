
class DataService:
    def __init__(self):
        self.service_collection = {}

    def add_service(self, name, service):
        self.service_collection[name] = service