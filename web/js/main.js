eel.expose(receive_message);
function receive_message(message) {
  addMessage(message, false);
}

const chatMessages = document.getElementById('chat-messages');

const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const uploadButton = document.getElementById('upload-button');

function addMessage(message, isSent) {
    const messageElement = document.createElement('div');

    if (isSent) {
      messageElement.textContent = message;
    } else {
      messageElement.innerHTML = message;
    }
    messageElement.classList.add('message');
    messageElement.classList.add(isSent ? 'sent' : 'received');
    messageElement.markdown = "1"
    const idMessage = document.createElement('span');
    idMessage.textContent = isSent ? 'Você' : 'É acessível?';
    idMessage.classList.add('message-author');
    chatMessages.appendChild(idMessage);
    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendButton.addEventListener('click', () => {
    const message = chatInput.value.trim();
    if (message) {
        addMessage(message, true);
        eel.send_prompt(message);
        chatInput.value = '';
    }
});

chatInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendButton.click();
    }
});

uploadButton.addEventListener('click', async () => {
  const filePath = await eel.get_file();
  console.log(filePath);
});