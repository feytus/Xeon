from random import randint

class Color:
    def get_color(type: str):
        if type == "lite":
            colors = [0x42ff75, 0x34ebb4, 0xa9fa52]
        elif type == "sanction":
            colors = [0xf06930, 0x700137, 0xf53145]
        return colors[randint(0, len(colors)-1)]