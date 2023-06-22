import os

directory = "Fonts"
available_fonts = [filename for filename in os.listdir(directory)]


def fonts_dictionary(av_fonts):
    """Creates a dictionary of fonts where key is the font name and values are all the available types of that font"""
    fonts_dic = {}
    for font in av_fonts:
        fonts_dic.update({filename: f"{directory}/{font}/static/{filename}" for filename in os.listdir(f"{directory}/{font}/static")})

    new_dic = {}
    for key, value in fonts_dic.items():
        new_dic[key.split(".")[0]] = value

    return new_dic
