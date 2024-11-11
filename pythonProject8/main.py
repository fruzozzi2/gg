from flask import Flask, request, jsonify
from g4f.client import Client

app = Flask(__name__)

# История чатов будет храниться в памяти
chat_history = {}

# Инициализация клиента g4f
client = Client()


@app.route('/chat', methods=['POST'])
def chat():
    # Получаем данные из запроса
    user_id = request.json.get('user_id')
    message = request.json.get('message')

    if not user_id or not message:
        return jsonify({'error': 'user_id and message are required'}), 400

    # Инициализация истории чата для пользователя
    if user_id not in chat_history:
        chat_history[user_id] = []

    # Добавляем сообщение пользователя в историю
    chat_history[user_id].append({"role": "user", "content": message})

    # Отправляем историю чата в модель GPT
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history[user_id]
    )

    # Получаем ответ от модели
    gpt_response = response.choices[0].message.content

    # Добавляем ответ модели в историю
    chat_history[user_id].append({"role": "assistant", "content": gpt_response})

    # Возвращаем ответ пользователю
    return jsonify({"response": gpt_response})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
