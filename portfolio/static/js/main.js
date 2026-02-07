// document.getElementById('chatbot-toggle').onclick = () => {
//     const bot = document.getElementById('chatbot');
//     bot.style.display = bot.style.display === 'block' ? 'none' : 'block';
// };

// function sendMessage() {
//     const input = document.getElementById('chatbot-input');
//     const msgContainer = document.getElementById('chatbot-messages');
//     const msg = document.createElement('div');
//     msg.textContent = input.value;
//     msg.classList.add('mb-1', 'text-end');
//     msgContainer.appendChild(msg);
//     input.value = '';
//     msgContainer.scrollTop = msgContainer.scrollHeight;
// }






document.getElementById('chatbot-toggle').onclick = () => {
    const bot = document.getElementById('chatbot');
    bot.style.display = bot.style.display === 'block' ? 'none' : 'block';
};

function sendMessage() {
    const input = document.getElementById('chatbot-input');
    const msgContainer = document.getElementById('chatbot-messages');
    const userMsg = input.value.trim();
    if(!userMsg) return;

    // Show user message
    const msg = document.createElement('div');
    msg.textContent = userMsg;
    msg.classList.add('mb-1', 'text-end');
    msgContainer.appendChild(msg);
    input.value = '';
    msgContainer.scrollTop = msgContainer.scrollHeight;

    // Send AJAX request
    fetch("{% url 'chatbot' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: "message=" + encodeURIComponent(userMsg)
    })
    .then(response => response.json())
    .then(data => {
        if(data.bot_message){
            const botMsg = document.createElement('div');
            botMsg.textContent = data.bot_message;
            botMsg.classList.add('mb-1', 'text-start', 'fw-bold');
            msgContainer.appendChild(botMsg);
            msgContainer.scrollTop = msgContainer.scrollHeight;
        }
    })
    .catch(err => console.error(err));
}