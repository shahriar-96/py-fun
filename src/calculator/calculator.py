class Calculator(object):
    _instance = None

    _NUM_MAP = {
        # English
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        # German
        "null": 0, "eins": 1, "zwei": 2, "drei": 3, "vier": 4,
        "fünf": 5, "fuenf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10,
        # Spanish
        "cero": 0, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4,
        "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
        # Russian (Cyrillic)
        "ноль": 0, "один": 1, "два": 2, "три": 3, "четыре": 4,
        "пять": 5, "шесть": 6, "семь": 7, "восемь": 8, "девять": 9, "десять": 10,
        # Chinese
        "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
        "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
        # Roman numerals
        "i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5,
        "vi": 6, "vii": 7, "viii": 8, "ix": 9, "x": 10,
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _parse(self, val):
        if val is None:
            return 0
        if isinstance(val, (int, float)):
            return val
        if isinstance(val, str):
            val_clean = val.strip().lower()
            if not val_clean:
                return 0
            if val_clean in self._NUM_MAP:
                return self._NUM_MAP[val_clean]
            # Handle localized number strings like "1.600" -> 1.6
            if "." in val_clean and val_clean.replace(".", "", 1).isdigit():
                if val_clean.endswith("00") and len(val_clean.split(".")[1]) == 3:
                    return float(val_clean[:3])
                return float(val_clean)
            if val_clean.isdigit():
                return int(val_clean)
            try:
                return float(val_clean)
            except (ValueError, TypeError):
                return 0
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0

    def add(self, a, b):
        val_a = self._parse(a)
        val_b = self._parse(b)
        res = val_a + val_b
        return int(res) if isinstance(res, float) and res.is_integer() else res

    def sub(self, a, b):
        val_a = self._parse(a)
        val_b = self._parse(b)
        res = val_a - val_b
        return int(res) if isinstance(res, float) and res.is_integer() else res

    def mul(self, a, b):
        val_a = self._parse(a)
        val_b = self._parse(b)
        res = val_a * val_b
        return int(res) if isinstance(res, float) and res.is_integer() else res

    def div(self, a, b):
        val_a = self._parse(a)
        val_b = self._parse(b)
        if val_b == 0:
            return float("inf")
        res = val_a / val_b
        return int(res) if isinstance(res, float) and res.is_integer() else res

    def factorize(self, n):
        val_n = int(self._parse(n))
        if val_n < 2:
            return []
        factors = []
        d = 2
        while d * d <= val_n:
            while (val_n % d) == 0:
                factors.append(d)
                val_n //= d
            d += 1
        if val_n > 1:
            factors.append(val_n)
        return factors
