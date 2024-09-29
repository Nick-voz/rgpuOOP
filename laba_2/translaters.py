class WordTranslater:

    WORDS = {
        "если": "if",
        "то": "then",
        "для": "for",
        "делать": "do",
        "до": "until",
        "пока": "while",
        "в": "in",
        "с": "with",
        "начало": "begin",
        "конец": "end",
        "процедура": "procedure",
        "функция": "function",
        "множество": "set",
        "символ": "symbol",
        "строка": "string",
        "целый": "integer",
        #
        "if": "если",
        "then": "то",
        "for": "для",
        "do": "делать",
        "until": "до",
        "while": "пока",
        "in": "в",
        "with": "с",
        "begin": "начало",
        "end": "конец",
        "procedure": "процедура",
        "function": "функция",
        "set": "множество",
        "symbol": "символ",
        "string": "строка",
        "integer": "целый",
    }

    def __init__(self) -> None:
        self.word = None

    def set_word(self, word: str) -> None:
        if word not in self.WORDS:
            raise ValueError(f"unexpected word for translate: {word}")
        self.word = word

    def translate(self) -> str:
        if self.word is None:
            raise RuntimeError("set_wordd() must be called before translate")
        return self.WORDS[self.word]


class NumTranslater:
    dec_num: int

    def set_num(self, num: str) -> None:
        self.dec_num = int(num)

    def hex(self) -> str:
        return hex(self.dec_num)[2:]

    def bin(self) -> str:
        return bin(self.dec_num)[2:]
