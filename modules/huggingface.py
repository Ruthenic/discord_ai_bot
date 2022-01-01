import requests, re 

class completion():
    def __init__(self, config):
        self.API_URL = "https://api-inference.huggingface.co/models/" + "EleutherAI/gpt-neo-2.7B"
        self.headers = {"Authorization": "Bearer " + config["huggingface"]["token"]}
        self.NAME = config["general"]["completion"]["defaults"]["name"]
        self.BACKSTORY = config["general"]["completion"]["defaults"]["backstory"]
        self.prefix = 'The following is a chat with ' + self.NAME + ', ' + self.BACKSTORY + '.\n'
        self.memory = []

    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()

    def genCleanMessage(self, optPrompt, userName):
        completePrompt = self.prefix + '\n'
        for turn in self.memory[-3:]:
            completePrompt += turn['User'] + ': "' + turn['Prompt'] + '"\n' + self.NAME + ': "' + turn['Reply'] + '"\n'
        completePrompt += userName + ': "' + optPrompt + '"\n' + self.NAME + ': "'
        print('\nPROMPT:\n' + completePrompt)
        text_generation_parameters = {
            'max_new_tokens': 50,
            'temperature': 0.8,
            'repetition_penalty': 1.8,
            'top_k': 40,
            'return_full_text': False
        }
        output_list = self.query({"inputs": completePrompt, "parameters": text_generation_parameters})
        response = output_list[0]["generated_text"]
        print('\nGENERATED:\n' + response)
        truncate = 0
        cleanStr = ''
        truncate = response.find('"')
        cleanStr = response[:truncate]
        if re.search(r'[?.!]', cleanStr):
            trimPart = re.split(r'[?.!]', cleanStr)[-1]
            cleanStr = cleanStr.replace(trimPart,'')
        print('\nEXTRACTED:\n' + cleanStr)
        if not cleanStr:
            cleanStr = 'Idk how to respond to that lol. I broke.'
        self.memory.append({'User': userName, 'Prompt': optPrompt, 'Reply': cleanStr})
        return cleanStr
    def changeShit(self, name=None, backstory=None):
        self.NAME = name if name else self.NAME
        self.BACKSTORY = backstory if backstory else self.BACKSTORY
        print(f"New name: {self.BACKSTORY}\nNew backstory: {self.BACKSTORY}")
        self.prefix = 'The following is a chat with ' + self.NAME + ', ' + self.BACKSTORY + '.\n'
        self.memory = []
    def complete(self, username, text):
        genMessage = self.genCleanMessage(text, username)
        return f"[{self.NAME}] {genMessage}"
