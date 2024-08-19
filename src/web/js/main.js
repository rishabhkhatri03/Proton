// Add a user message to the chat box
function addUserMsg(msg) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `<div>${msg}</div>`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Add a Proton message to the chat box
function addProtonMsg(msg) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message proton-message';
    messageDiv.innerHTML = `<div>${msg}</div>`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Event listener for the send button
document.getElementById('userInputButton').addEventListener('click', function() {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() !== '') {
        addUserMsg(`User: ${userInput}`);
        eel.getUserInput(userInput);
        document.getElementById('userInput').value = '';
    }
});

// Handle the Enter key to send messages
document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        document.getElementById('userInputButton').click();
    }
});

// Receive messages from the backend
eel.expose(addProtonMsg);
