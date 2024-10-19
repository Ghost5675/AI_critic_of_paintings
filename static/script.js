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

    fileInput.addEventListener('change', function () {
        sendFile();
    });

    function sendFile() {
        const fileInput = document.getElementById('fileInput'); // Получаем элемент input для файлов
        const file = fileInput.files[0]; // Получаем первый выбранный файл
        if (file) {
            console.log(`Имя файла: ${file.name}`);
            console.log(`Размер файла: ${file.size} байт`);
            console.log(`Тип файла: ${file.type}`);
    
            // Создаем объект FormData
            const formData = new FormData();
            formData.append('file', file); // Добавляем файл в FormData
    
            fetch('/upload_image/', {
                method: 'POST',
                body: formData, // Отправляем FormData
            })
            .then(response => response.json())
            .then(data => {
                displayResult(data); // Обрабатываем ответ от сервера
            })
            .catch(error => {
                console.error('Error:', error);
            });
    
            // Создаем URL для отображения изображения
            const imageUrl = URL.createObjectURL(file);
    
            // Создаем элемент img для отображения
            const imgElement = document.createElement('img');
            imgElement.src = imageUrl; // Устанавливаем src на URL объекта
            imgElement.alt = "Загруженное изображение";
            imgElement.classList.add('chat-image'); // Добавляем класс для стилизации (если нужно)
    
            // Добавляем изображение в контейнер
            const chatBox = document.getElementById('chat-box');
            chatBox.appendChild(imgElement);
            chatBox.scrollTop = chatBox.scrollHeight; // Прокручиваем вниз
        } else {
            console.log("Файл не выбран.");
        }
    }

    function displayResult(critique) {
        const critiqueElement = document.createElement('div');
        critiqueElement.classList.add('critique');
        critiqueElement.textContent = "🤖: " + critique; // Добавляем текст критики
        
        const chatBox = document.getElementById('chat-box');
        chatBox.appendChild(critiqueElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Прокручиваем вниз
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