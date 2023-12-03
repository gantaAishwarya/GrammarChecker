from textblob import TextBlob
import requests

URL = "https://services.gingersoftware.com/Ginger/correct/jsonSecured/GingerTheTextFull"
API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"


class GingerIt(object):
    def __init__(self):
        self.url = URL
        self.api_key = API_KEY
        self.api_version = "2.0"
        self.lang = "US"

    def parse(self, text, verify=True):
        session = requests.Session()
        request = session.get(
            self.url,
            params={
                "lang": self.lang,
                "apiKey": self.api_key,
                "clientVersion": self.api_version,
                "text": text,
            },
            verify=verify,
        )
        data = request.json()
        return self._process_data(text, data)

    @staticmethod
    def _change_char(original_text, from_position, to_position, change_with):
        return "{}{}{}".format(
            original_text[:from_position], change_with, original_text[to_position + 1 :]
        )

    def _process_data(self, text, data):
        result = text
        corrections = []

        for suggestion in reversed(data["Corrections"]):
            start = suggestion["From"]
            end = suggestion["To"]

            if suggestion["Suggestions"]:
                suggest = suggestion["Suggestions"][0]
                result = self._change_char(result, start, end, suggest["Text"])

                corrections.append(
                    {
                        "start": start,
                        "text": text[start : end + 1],
                        "correct": suggest.get("Text", None),
                        "definition": suggest.get("Definition", None),
                    }
                )

        return {"text": text, "result": result, "corrections": corrections}

class SpellCheckerModule:
    def __init__(self):
        self.spell_check = TextBlob("")
        self.grammar_check = GingerIt()
    def correct_spell(self,text):
        words = text.split()
        corrected_words = []
        for word in words:
            corrected_word = str(TextBlob(word).correct())
            corrected_words.append(corrected_word)
        return " ".join(corrected_words)

    def correct_grammar(self,text):
        matches = self.grammar_check.parse(text)

        foundmistakes = []
        for error in matches['corrections']:
            foundmistakes.append(error['text'])
        foundmistakes_count = len(foundmistakes)
        return foundmistakes,foundmistakes_count


if __name__  == "__main__":
    obj = SpellCheckerModule()
    message = "Hello world. I like mashine learning. appple. bananana"
    print(obj.correct_spell(message))
    print(obj.correct_grammar(message))
