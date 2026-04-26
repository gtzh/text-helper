#!/usr/bin/env python
"""Text selection assistant - Flask backend."""

import json
import os
from pathlib import Path
from flask import Flask, jsonify, request, send_file, Response, stream_with_context
import markdown
import config

app = Flask(__name__, static_folder="static")
app.json.ensure_ascii = False

STATIC_DIR = Path(__file__).parent / "static"


@app.after_request
def set_charset(response):
    ct = response.content_type or ""
    if "application/json" in ct and "charset" not in ct:
        response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/popup")
def popup():
    return send_file(STATIC_DIR / "popup.html")


@app.route("/api/config")
def api_config():
    ops = config.get_operations()
    op_list = [{"key": k, "label": v.get("label", k)} for k, v in ops.items()]
    first_op = op_list[0]["key"] if op_list else "translate"
    return jsonify({
        "models": config.get_models(),
        "operations": op_list,
        "default_operation": first_op,
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True) if ("application/json" in (request.content_type or "")) else request.form
    operation = data.get("operation", "translate")
    model = data.get("model", "ds")
    messages = data.get("messages", [])

    if not messages:
        text = data.get("text", "").strip()
        messages = [{"role": "user", "content": text}]

    op_cfg = config.get_operation(operation)
    system_prompt = op_cfg.get("system_prompt", "")

    if not any(m.get("role") == "system" for m in messages):
        messages.insert(0, {"role": "system", "content": system_prompt})

    newapi = config.get_newapi_config()
    base_url = newapi.get("base_url", "").rstrip("/")
    api_key = newapi.get("api_key", "")

    from openai import OpenAI
    client = OpenAI(base_url=base_url, api_key=api_key)

    def generate():
        buf = ""
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    buf += chunk.choices[0].delta.content
                    yield f"data: {json.dumps({'chunk': chunk.choices[0].delta.content}, ensure_ascii=False)}\n\n"
            html = markdown.markdown(buf, extensions=["fenced_code", "tables"])
            yield f"data: {json.dumps({'done': True, 'html': html, 'content': buf}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )


if __name__ == "__main__":
    print("Starting text-helper server on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes"))
