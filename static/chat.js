document.getElementById('send-button').addEventListener('click', function() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message) {
        const messageContainer = document.createElement('div');
        messageContainer.textContent = message;
        document.getElementById('chat-messages').appendChild(messageContainer);
        messageInput.value = '';
    }
});
