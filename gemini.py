import google.generativeai as genai
import markdown
import config

class ChatAI:
    def __init__(self):
        genai.configure(api_key=config.API_KEY)
        self.model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                                           safety_settings=config.SAFETY_SETTINGS,
                                           generation_config=config.GENERATION_SETTINGS)
        self.pro_vision = genai.GenerativeModel('gemini-pro-vision')
        self.history = []
        self.chat = self.model.start_chat(history=self.history)
    
    def send_prompt(self, prompt, stream=False):
        if stream:
            response = self.pro_vision.generate_content(prompt, stream=stream)
            response.resolve()
        else:
            response = self.chat.send_message(prompt, stream=stream)

        html_content = markdown.markdown(response.text, extensions=['fenced_code', 'codehilite'])
        return html_content

    def get_history(self):
        return self.chat.history
