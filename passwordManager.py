from cryptography.fernet import Fernet

class passwordManager:
    def __init__(self):
        self.key = None
        self.passwordFile = None
        self.passwordDict = None

    def create_key(self, path):
        self.key = Fernet.generate_key()
        # print(self.key)
        with open(path, 'wb') as f:
            f.write(self.key)

    def get_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initialValues=None):
        self.passwordFile = path

        for key, value in initialValues.items():
            # pass # TODO: add passwords to dictionary
            self.add_password(key, value)

    def load_password_file(self, path):
        self.passwordFile = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(':')
                self.passwordDict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.passwordDict[site] = password

        if self.passwordFile is not None:
            with open(self.passwordFile, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + '\n')

    def get_password(self, site):
        return self.passwordDict[site]

def main():
    pm = passwordManager()
    pm.create_key('myKey.key')

if __name__ == '__main__':
    main()