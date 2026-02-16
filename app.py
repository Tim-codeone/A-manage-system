# 最简单的后端服务：POST /predict {"prompt": "..."} -> {"output": "..."}
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def call_local_model(prompt: str) -> str:
    # 本地测试时使用的简单"回显"逻辑，不需要网络或 API Key
    return "本地模拟回答： " + prompt

def call_openai(prompt: str) -> str:
    # 如果你配置了 OPENAI_API_KEY，会尝试使用 openai 包调用（可选)
    try:
        import openai
    except Exception as e:
        raise RuntimeError("缺少 openai 库，请安装 requirements.txt 中的依赖") from e
    openai.api_key = OPENAI_API_KEY
    # 使用简单的 Completion 接口（兼容大多数 OpenAI SDK 版本)
    resp = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=150)
    return resp.choices[0].text.strip()

@app.route("/", methods=["GET"])
def index():
    return "简单 AI 服务：POST /predict 发送 JSON {\"prompt\": \"...\"}"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True, silent=True)
    if not data or "prompt" not in data:
        return jsonify({"error": "请发送 JSON，包含字段 prompt，例如 {\"prompt\":\"你好\"}"}), 400
    prompt = data["prompt"]
    try:
        if OPENAI_API_KEY:
            output = call_openai(prompt)
        else:
            output = call_local_model(prompt)
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 直接用 Flask 启动，便于新手本地调试
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))