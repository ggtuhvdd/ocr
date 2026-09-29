#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ddddocr 免费 OCR API 服务
部署到 Render / Railway / Koyeb 免费层即可
手机 TVBox 源 POST 验证码图到此接口识别
"""
import base64
import io
import re
from flask import Flask, request, jsonify
import ddddocr

app = Flask(__name__)
ocr = ddddocr.DdddOcr(show_ad=False)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'ok', 'msg': 'ddddocr API 运行中'})


@app.route('/ocr', methods=['POST'])
def ocr_api():
    """
    接收 base64 图片或纯二进制图片，返回识别结果
    用法：
      POST /ocr  body=base64图片数据  →  text/plain 返回识别码
      POST /ocr  body=二进制图片      →  text/plain 返回识别码
    """
    try:
        data = request.get_data()
        if not data:
            return 'error: no image', 400

        # 尝试当 base64 解码
        try:
            img_bytes = base64.b64decode(data)
        except Exception:
            img_bytes = data

        code = ocr.classification(img_bytes)
        code = re.sub(r'[^a-zA-Z0-9]', '', code)[:4]
        return code
    except Exception as e:
        return f'error: {e}', 500


@app.route('/ocr_json', methods=['POST'])
def ocr_json():
    """JSON 格式接口：POST {"image": "base64"} → {"code": "xxxx"}"""
    try:
        body = request.get_json()
        img_b64 = body.get('image', '')
        img_bytes = base64.b64decode(img_b64)
        code = ocr.classification(img_bytes)
        code = re.sub(r'[^a-zA-Z0-9]', '', code)[:4]
        return jsonify({'code': code})
    except Exception as e:
        return jsonify({'code': '', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
