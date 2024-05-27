from flask import Flask, request, jsonify,Response
import tiktoken
import openai
import json

app = Flask(__name__)

@app.route('/encode', methods=['POST'])
def encode_text():
    # 获取请求数据
    data = request.get_json()
    model_name = data.get('model')
    text = data.get('text')

    # 如果模型名称或文本内容未提供,返回错误
    if not model_name or not text:
        return jsonify({'error': 'Missing model or text'}), 400

    try:
        # 获取指定模型的编码器
        encoding = tiktoken.encoding_for_model(model_name)

        # 对输入文本进行编码
        tokens = encoding.encode(text)

        # 将结果作为JSON响应返回
        return jsonify({'tokens': tokens})
    except Exception as e:
        # 如果出现任何错误,返回错误信息
        return jsonify({'error': str(e)}), 500

# 静态文件路由
@app.route('/.well-known/acme-challenge/<path:filename>')
def serve_well_known(filename):
    return send_from_directory(os.path.join(app.root_path, '.well-known/acme-challenge'), filename)


@app.route('/openai/chat', methods=['POST'])
def chat():
    data = request.json
    if 'api_key' not in data:
        return jsonify({'error': 'No API key provided'}), 400
    if 'messages' not in data:
        return jsonify({'error': 'No messages provided'}), 400

    openai.api_key = data['api_key']
    def generate():
        response = openai.ChatCompletion.create(
            model=data.get('model', 'gpt-3.5-turbo'),
            messages=data['messages'],
            stream=True,
            max_tokens=data.get('max_tokens', 150),
            temperature=data.get('temperature', 0.7)
        )
        for chunk in response:
            if chunk.choices[0].delta.get('content'):
                yield f"data: {json.dumps(chunk.choices[0].delta['content'])}\n\n"
    
    return Response(generate(), content_type='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)