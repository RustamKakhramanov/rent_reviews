import json
import os
import sys


class Translator:
    locale = 'en'  # В конструкторе не видны конфиги .env

    @staticmethod
    async def set_locale(locale: str):
        if Translator.check_exists_locale(locale):
            Translator.locale = locale

    @staticmethod
    def get_locale_path(locale: str):
        return os.path.dirname(sys.modules['__main__'].__file__) + '/../../messages/'+locale

    @staticmethod
    def check_exists_locale(locale: str):
        return os.path.exists(Translator.get_locale_path(locale))

    # def __init__(self) -> None:
    #     if not self.locale:
    #         self.locale = env("DEFAULT_LOCALE", cast=str, default="ru")
    #     print(env(key="DEFAULT_LOCALE", cast=str,))


    def translate(self, key, locale=None, with_file_name=False, variables:dict|None = None):
        if (locale and Translator.check_exists_locale(locale)):
            actual_locale = locale
        else:
            actual_locale = self.locale

        if with_file_name:
            file_name = key.split('.')[0]
            keys = key.split('.')[1:]
        else:
            file_name = "messages"
            keys = key.split('.')

        path = self.get_locale_path(actual_locale)+'/'+file_name+'.json'

        if os.path.exists(path):
            messages = json.load(open(path))
            return self.replace_variables(self.__get_element__(keys, messages), variables)

        return ""
    
    def replace_variables(self, string:str = '', variables:dict|None = None):
        if(not variables):
            return string
    
        for variable in variables:
            string = str(string).replace( "{"+variable+"}", str(variables[variable]) )
        
        return string
        

    # Питон ругается если много раз переопределять переменную  searchable =  messages[key_element]
    def __get_element__(self, keys,  searchable):
        for index, key_element in enumerate(keys):

            if key_element in searchable and type(searchable[key_element]) is dict and len(keys[index:]) >= 1:
                return self.__get_element__(keys[index:], searchable[key_element])

            if key_element in searchable and type(searchable[key_element]) is not dict:
                return searchable[key_element]

        return ""


def t(key, locale=None, with_file_name=False, variables:dict|None = None):
    return Translator().translate(key, locale, with_file_name, variables)
