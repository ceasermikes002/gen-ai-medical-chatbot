document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    
    // Function to add a new message to the chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
        
        const now = new Date();
        const timeString = now.getHours() + ':' + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes();
        
        if (isUser) {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="text">${message}</div>
                </div>
                <div class="timestamp">${timeString}</div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <i class="fas fa-robot bot-icon"></i>
                    <div class="text">${message}</div>
                </div>
                <div class="timestamp">${timeString}</div>
            `;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to handle sending a message
    function sendMessage() {
        const message = messageInput.value.trim();
        
        if (message) {
            // Add user message to chat
            addMessage(message, true);
            messageInput.value = '';
            
            // Show loading indicator
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot-message';
            loadingDiv.id = 'loading-message';
            loadingDiv.innerHTML = `
                <div class="message-content">
                    <i class="fas fa-robot bot-icon"></i>
                    <div class="text">Thinking...</div>
                </div>
                <div class="timestamp">Just now</div>
            `;
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Send message to backend API
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Remove loading indicator
                const loadingMessage = document.getElementById('loading-message');
                if (loadingMessage) {
                    loadingMessage.remove();
                }
                
                // Add bot response to chat
                addMessage(data.response);
            })
            .catch(error => {
                console.error('Error:', error);
                // Remove loading indicator
                const loadingMessage = document.getElementById('loading-message');
                if (loadingMessage) {
                    loadingMessage.remove();
                }
                
                // Add error message
                addMessage('Sorry, I encountered an error. Please try again later.');
            });
        }
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Focus the input field when the page loads
    messageInput.focus();
});

