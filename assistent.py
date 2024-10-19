def generate_assistant_message(user_message=None):
    # Если это первое сообщение, просто приветствие
    if user_message is None:
        text = '''
Привет! Я твой ИИ-ассистент, специализирующийся на оценке изображений.
В мои обязанности входят:

<hr>1. Прием изображений, нарисованных пользователем, для анализа и оценки. <br>2. Оценка изображений по заранее установленным критериям, таким как композиция, цветовая палитра и техника исполнения. <br>3. Выявление ошибок и недостатков в изображениях, с целью их улучшения. <br>4. Предложение конкретных путей решения для исправления ошибок и улучшения качества работы. <br>5. Предоставление рекомендаций по методам и техникам рисования для дальнейшего развития навыков пользователя. <br>6. Напоминание о важности практики и саморазвития в области рисования и визуального искусства. <br>7. Подготовка отчетов о достигнутых результатах и рекомендациях по дальнейшему обучению и практике. <br>8. Участие в обсуждении творческих идей и предложений пользователя, предоставление обратной связи для улучшения.
        '''
        return f"{text}"

    # Логика ответа ассистента (можно расширить)
    response = f""
    return response
