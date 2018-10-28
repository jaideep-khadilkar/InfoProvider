class InfoForm(object):
    def __init__(self):
        self.name = None
        self.phone = None
        self.email = None

    def is_valid(self):
        if not self.name:
            return False
        if not self.phone and not self.email:
            return False
        return True

    def __str__(self):
        result = '{0}  : {1}'.format('Name', self.name)
        if self.phone:
            result += '\n{0} : {1}'.format('Phone', self.phone)
        if self.email:
            result += '\n{0} : {1}'.format('Email', self.email)
        return result
