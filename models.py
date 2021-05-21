import config

class User():
    name = config.config_get_dashboard_username()
    id = 1
    
    def to_json(self):
        return {"name": self.name}
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)


