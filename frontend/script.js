const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function scrollToBottom() {
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addMessage(content, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'agent-message'}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    if (isUser) {
        contentDiv.textContent = content;
    } else {
        contentDiv.innerHTML = marked.parse(content);
    }

    messageDiv.appendChild(contentDiv);
    chatHistory.appendChild(messageDiv);
    scrollToBottom();
}

async function sendMessage() {
    const query = userInput.value.trim();
    if (!query) return;

    addMessage(query, true);
    userInput.value = '';
    userInput.disabled = true;

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message agent-message';
    loadingDiv.innerHTML = '<div class="message-content">Typing...</div>';
    chatHistory.appendChild(loadingDiv);
    scrollToBottom();

    try {
        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: "USR-001",
                query: query,
                latitude: 19.10,
                longitude: 72.78
            }),
        });

        const data = await response.json();

        chatHistory.removeChild(loadingDiv);

        addMessage(data.response, false);

    } catch (error) {
        chatHistory.removeChild(loadingDiv);
        addMessage("Sorry, something went wrong. Please try again.", false);
        console.error('Error:', error);
    } finally {
        userInput.disabled = false;
        userInput.focus();
    }
}

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
