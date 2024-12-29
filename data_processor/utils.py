from googletrans import Translator

def translate_text(text, dest='en'):
    translator = Translator()
    return translator.translate(text, dest=dest).text

def get_staged_data_path(data_name):
    return f"../data/{data_name}_data_staged.csv"