document.addEventListener('DOMContentLoaded', function () {
    const inputField = document.getElementById('user-input');

    // Отправка сообщения по нажатию Enter
    inputField.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Отправка сообщения по кнопке
    document.getElementById('send-btn').addEventListener('click', sendMessage);

    function sendMessage() {
        const userInput = inputField.value;

        if (userInput.trim() !== "") {
            addMessageToChat("Вы: " + userInput, 'user');

            // Отправляем сообщение на сервер
            fetch('/send_message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: userInput }),
            })
            .then(response => response.json())
            .then(data => {
                addMessageToChat("🤖: " + data.response, 'gpt');
            });

            // Очищаем поле ввода
            inputField.value = '';
        }
    }

    function addMessageToChat(message, sender) {
        const chatBox = document.getElementById('chat-box');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(sender);
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});