eel.expose(receive_message);
function receive_message(message) {
  add_message(message);
}

eel.expose(uploaded_photo);
function uploaded_photo(imagePath) {
  const uploadButton = document.getElementById('upload-button');
  if (imagePath) {
    uploadButton.innerHTML = "1 foto (X)";
  } else {
    uploadButton.innerText = "Anexar";
  }
}

const chatMessages = document.getElementById('chat-messages');

const chatInput = document.getElementById('chat-input');
const sendButton = document.getElementById('send-button');
const uploadButton = document.getElementById('upload-button');

eel.expose(add_message);
function add_message(message, isSent = false, image = null) {
    const messageElement = document.createElement('div');
    if (isSent) {
      if (image) {
        const messageImage = document.createElement('img');
        messageImage.src = `public/${image}.jpg`;
        messageImage.classList.add('message-image');

        messageElement.appendChild(messageImage);

        const messageText = document.createElement('p');
        messageText.textContent = message;
        
        messageElement.appendChild(messageText);
      } else {
        messageElement.textContent = message;
      }
    } else {
      messageElement.innerHTML = message;
    }

    messageElement.classList.add('message');
    messageElement.classList.add(isSent ? 'sent' : 'received');
    messageElement.markdown = "1";

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
  await eel.get_file();
});