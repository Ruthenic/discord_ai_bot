import openai

class completion():
    def __init__(self, config):
        self.name      = config["general"]["completion"]["defaults"]["name"]
        self.backstory = config["general"]["completion"]["defaults"]["backstory"]
        self.prompt    = f"The following is a chat with {self.name}, {self.backstory}.\n\n"
        self.model     = config["openai"]["model"]
        openai.api_key = config["openai"]["token"]
    def __updatePrompt(self, username, text):
        print(f"Old prompt: {self.prompt}")
        self.prompt = self.prompt + f"{username}: {text}\n{self.name}: "
        print(f"New prompt: {self.prompt}")
    def __generate(self):
        response = openai.Completion.create(
            engine = "davinci",
            prompt = self.prompt,
            max_tokens=100,
            temperature=0.85,
            stop=["\n"]
        )
        return response["choices"][0]["text"]
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
        try:
            generation = self.__generate()
        except Exception as e:
            return f"ERROR: {str(e)}"
        print(f"Generated response: {generation}")
        self.prompt += generation + "\n"
        return f"[{self.name}]{generation}" if generation.startswith(" ") else f"[{self.name}] {generation}"
