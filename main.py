import os
import json
import datetime

from cryptography.fernet import Fernet


class FernetEncrypter:

    def __init__(self, key_path: str) -> None:

        self.key = None
        self.time_key = None
        self.get_key(key_path)

        self.filter_ascii_char = lambda x: ''.join(e if e.isascii() else '' for e in x )

    def string_cryptor(self, string: str, encode: bool) -> str:

        # Instance the Fernet class with the key
        fernet = Fernet(self.key)

        # then use the Fernet class instance
        if encode:
            cryp_string = str(fernet.encrypt(string.encode()), 'UTF-8')
        else:
            cryp_string = fernet.decrypt(string).decode()

        return cryp_string
    
    def file_cryptor(self, new_file:str, encode:bool) -> None:

        # using the generated key
        fernet = Fernet(self.key)

        # opening the original file to encrypt
        with open(new_file, 'rb') as eFile:
            original = eFile.read()

        if encode:
            # encrypting the file
            crypted = fernet.encrypt(original)
        else:
            # decrypting the file
            crypted = fernet.decrypt(original)

        # opening the file in write mode and
        # writing the encrypted data
        with open(new_file, 'wb') as crypted_file:
            crypted_file.write(crypted)

    def rename_file(self, folder_path:str, file:str, encode:bool) -> str:

        if encode:
            new_file_name = self.filter_ascii_char(str(os.path.basename(file)))
        else:
            new_file_name = str(os.path.basename(file))

        new_file_name = self.string_cryptor(new_file_name, encode)
        new_file = os.path.join(folder_path, new_file_name)
        os.rename(file, new_file)

        return new_file

    def get_key(self, key_path: str) -> None:

        if not os.path.exists(key_path):
            key = Fernet.generate_key()

            # string the key in a file
            with open(key_path, 'wb') as filekey:
                filekey.write(key)

        # opening the key
        with open(key_path, 'rb') as filekey:
            self.key = filekey.read()

        # self.check_time(check=False)

    def check_time(self, check: bool, write: bool = False) -> None:

        val_path = 'val.t'
        time_format = "%Y-%m-%d %H:%M:%S"
        now = datetime.datetime.today().strftime(time_format)
        date_obj = lambda x: datetime.datetime.strptime(x, time_format)

        if check:
            diff = date_obj(now) - date_obj(self.time_key['last_date'])
            if not diff.days > self.time_key['date_diff']:
                raise NotImplementedError(f"Be strong!!! \nMax days of {self.time_key['date_diff']} has not passed !!")
            else:
                write = True

        if write:

            self.time_key['last_date'] = now

            # string the key in a file
            with open(val_path, 'w') as filekey:
                filekey.write(self.string_cryptor(json.dumps(self.time_key), encode=True))

        else:
            # opening the key
            with open(val_path, 'r') as filekey:
                self.time_key = json.loads(self.string_cryptor(filekey.read(), encode=False))

    def folder_cryptor(self, folder_path: str, encode: bool) -> None:
        
        # if not encode:
        # self.check_time(check=True)

        # iterate over files in that directory
        for filename in os.listdir(folder_path):
            file = os.path.join(folder_path, filename)

            # checking if it is a file
            if os.path.isfile(file):

                # rename_file
                new_file = self.rename_file(folder_path, file, encode)

                print(f'crypting old {file} -> new {new_file}')
                self.file_cryptor(new_file, encode)

            # else calling itself
            else:
                self.folder_cryptor(file, encode)

                # rename folder
                self.rename_file(folder_path, file, encode)
        


if __name__ == '__main__':
    enc = FernetEncrypter('key.k')
    enc.folder_cryptor(r"", 1)

    print('done')