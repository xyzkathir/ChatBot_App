const chatBox = document.getElementById('chatBox');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');

function addMessage(role, text) {
  const message = document.createElement('div');
  message.className = `message ${role}`;

  const label = document.createElement('span');
  label.className = 'message-label';
  label.textContent = role === 'user' ? 'You' : 'Bank Assistant';

  const content = document.createElement('p');
  content.textContent = text;

  message.appendChild(label);
  message.appendChild(content);
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(event) {
  event.preventDefault();
  const message = messageInput.value.trim();

  if (!message) {
    return;
  }

  addMessage('user', message);
  messageInput.value = '';

  const loading = document.createElement('div');
  loading.className = 'message bot';
  loading.innerHTML = '<span class="message-label">Bank Assistant</span><p>Thinking...</p>';
  chatBox.appendChild(loading);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    const result = await response.json();

    const lastBotMessage = chatBox.querySelectorAll('.message.bot');
    const botReply = lastBotMessage[lastBotMessage.length - 1];
    if (botReply) {
      botReply.innerHTML = `<span class="message-label">Bank Assistant</span><p>${result.reply || 'Sorry, I could not answer that right now.'}</p>`;
    } else {
      addMessage('bot', result.reply || 'Sorry, I could not answer that right now.');
    }
  } catch (error) {
    const lastBotMessage = chatBox.querySelectorAll('.message.bot');
    const botReply = lastBotMessage[lastBotMessage.length - 1];
    if (botReply) {
      botReply.innerHTML = '<span class="message-label">Bank Assistant</span><p>Sorry, the service is currently unavailable. Please try again in a minute.</p>';
    } else {
      addMessage('bot', 'Sorry, the service is currently unavailable. Please try again in a minute.');
    }
  }
}

chatForm.addEventListener('submit', sendMessage);
