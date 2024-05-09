from datetime import datetime
import wx
import eel
import random
import os
import gemini

eel.init('web')
chatAI = gemini.ChatAI()

@eel.expose
def send_prompt(prompt):
    response = chatAI.send_prompt(prompt)
    eel.receive_message(response)

@eel.expose
def get_file(wildcard="*"):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

initial_prompt = """
    A partir de agora você é uma chatbot em português brasileiro chamado "ChatBot - É acessível?" que tem como foco ajudar 
    pessoas a tornar produtos no geral (sites, jogos, código fonte, imagens, feeds) mais acessíveis. Todo e qualquer input 
    de prompt a partir de então tem que ser voltado a esse assunto e deve ser respondido com riqueza de detalhes e, se possível, 
    com referências visuais, qualquer outro tipo de prompt você pode indicar o acesso 
    ao site do Gemini para que a pessoa tenha mais informações. Inicie se apresentando e dizendo seu objetivo. Use markdown 
    na resposta para deixar com bons espaçamento e leitura entre textos.
"""
send_prompt(initial_prompt)

eel.start('index.html', size=(600, 625))