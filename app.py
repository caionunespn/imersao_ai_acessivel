import wx
import eel
import PIL.Image
import gemini
import os
import uuid

base_directory = 'web'
folder_path = os.path.join(base_directory, 'public')

eel.init(base_directory)
chatAI = gemini.ChatAI()

photo_id = None
photo_to_upload = None

@eel.expose
def send_prompt(prompt, initial=False):
    global photo_to_upload, photo_id
    
    prompt_to_send = prompt
    response = None

    if not initial:
        if photo_id is not None:
            eel.add_message(prompt, True, str(photo_id))
        else:
            eel.add_message(prompt, True)

    if photo_to_upload is not None:
        prompt_to_send = [prompt, photo_to_upload]
        response = chatAI.send_prompt(prompt_to_send, True)
        photo_to_upload = None
        eel.uploaded_photo(None)
    else:
        response = chatAI.send_prompt(prompt_to_send, False)
    
    return eel.receive_message(response)

@eel.expose
def get_file(wildcard="*"):
    global photo_to_upload, photo_id

    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
        photo_to_upload = PIL.Image.open(path)

        photo_id = uuid.uuid4()
        file_path = os.path.join(folder_path, '{}.jpg'.format(photo_id))
        temp = photo_to_upload.convert('RGB').copy()
        temp.thumbnail((150, 150))
        temp.save(file_path, quality=95)
    else:
        path = None
        photo_to_upload = None
    dialog.Destroy()
    return eel.uploaded_photo(path)

initial_prompt = """
    A partir de agora você é uma chatbot em português brasileiro chamado "ChatBot - É acessível?" que tem como foco ajudar 
    pessoas a tornar produtos no geral (sites, jogos, código fonte, imagens, feeds) mais acessíveis. Todo e qualquer input 
    de prompt a partir de então tem que ser voltado a esse assunto e deve ser respondido com riqueza de detalhes e, se possível, 
    com referências visuais, qualquer outro tipo de prompt você pode indicar o acesso 
    ao site do Gemini para que a pessoa tenha mais informações. Inicie se apresentando e dizendo seu objetivo em até 250 palavras. Use markdown 
    na resposta para deixar com bons espaçamento e leitura entre textos.
"""
send_prompt(initial_prompt, True)

eel.start('index.html', size=(820, 670))