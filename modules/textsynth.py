import requests

class completion():
    def __init__(self, config):
        self.name      = config["general"]["completion"]["defaults"]["name"]
        self.backstory = config["general"]["completion"]["defaults"]["backstory"]
        self.prompt    = f"The following is a chat with {self.name}, {self.backstory}.\n"
        self.token     = config["textsynth"]["token"]
    def __updatePrompt(self, username, text):
        print(f"Old prompt: {self.prompt}")
        self.prompt = self.prompt + f"{username}: {text}\n{self.name}:"
        print(f"New prompt: {self.prompt}")
    def __generate(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        data = {
            "prompt": self.prompt,
            "max_tokens": 200,
            "temperature": 0.8,
            "stop": "\n"
        }
        res = requests.post("https://api.textsynth.com/v1/engines/gptj_6B/completions", headers=headers, json=data)
        res = res.json()
        return res["text"]
    def __reset(self):
        self.prompt = self.prompt    = f"The following is a chat with {self.name}, {self.backstory}.\n"
        print(f"Reset log to {self.prompt}")
    def changeShit(self, name=None, backstory=None):
        self.name = name if name else self.name
        self.backstory = backstory if backstory else self.backstory
        print(f"New name: {self.name}\nNew backstory: {self.backstory}")
        self.__reset()
    def complete(self, username, text):
        self.__updatePrompt(username, text)
        generation = self.__generate()
        print(f"Generated response: {generation}")
        self.prompt += generation + "\n"
        return f"[{self.name}] {generation}"
