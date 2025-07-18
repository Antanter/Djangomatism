import re

class Censorer:
    FORBIDDEN_GRAMATAS = ['job application', 'fuck', 'bitch']

    @staticmethod
    def censor_text(text):
        for word in Censorer.FORBIDDEN_GRAMATAS:
            pattern = re.compile(r'\b\w*' + re.escape(word) + r'\w*\b', re.IGNORECASE)
            text = pattern.sub(lambda m: '*' * len(m.group()), text)
        return text