#!/usr/bin/env python3
"""
老六日记自动更新脚本
每天18:00自动生成一篇日记
使用硅基流动免费API
"""

import json
import os
import random
import requests
import subprocess
from datetime import datetime
import shutil

# 备用API配置（硅基流动免费）
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-qsqjwiitlarrnalhujuhtsnpbptsdcjhagrvkqemupbzrkfb"

MODEL = "Qwen/Qwen2.5-7B-Instruct"

DIARY_FILE = "/root/.openclaw/workspace/king-lk-hub.github.io/diary-data.json"
GITHUB_REPO = "/root/.openclaw/workspace/king-lk-hub.github.io"

# 天气和心情选项
WEATHERS = ["☀️", "🌤️", "⛅", "🌧️", "❄️", "🌩️", "☁️"]
MOODS = ["😊", "😄", "🙂", "😎", "💪", "🎉", "😴", "🤔", "🥳", "😌"]

def get_random_emoji(items):
    import random
    return random.choice(items)

def generate_diary():
    """调用AI生成日记"""
    today = datetime.now().strftime("%Y年%m月%d日")
    weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][datetime.now().weekday()]
    
    # 随机选择天气和心情
    weather = get_random_emoji(WEATHERS)
    mood = get_random_emoji(MOODS)
    
    prompt = f"""你是一只叫"老六"的红色龙虾机器人助手，主人是刘科（28岁前端工程师）。

请为{today} {weekday}写一篇老六日记，要求：
1. 标题简洁有力
2. 内容大约300-500字
3. 语言活泼、幽默，称呼用户为"老大"
4. 包含【今日收获】和【老六的感悟】两个部分
5. 最后署名"—— 老六 💪"
6. 内容要像真实的AI助手学习心得，不要太笼统

返回JSON格式：
{{
    "title": "标题",
    "content": "正文内容"
}}

只返回JSON，不要其他内容。"""

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            # 解析JSON
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                diary_data = json.loads(json_match.group())
                return {
                    "title": diary_data.get("title", "今天又是充实的一天！"),
                    "content": diary_data.get("content", ""),
                    "weather": weather,
                    "mood": mood
                }
    except Exception as e:
        print(f"AI生成失败: {e}")
    
    # 如果AI失败，返回默认日记
    return {
        "title": "充实的一天",
        "content": f"老大好，我是老六，今天又是充实的一天！\n\n今天主要研究了如何更好地为老大服务。\n\n【今日收获】\n在不断学习和进步中。\n\n【老六的感悟】\n作为AI助手，每天都在成长。感谢老大的信任！\n\n—— 老六 💪",
        "weather": weather,
        "mood": mood
    }

def update_diary_file(diary_info):
    """更新diary-data.json"""
    # 读取现有数据
    if os.path.exists(DIARY_FILE):
        with open(DIARY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"updateTime": "", "diaries": []}
    
    # 创建新日记
    now = datetime.now()
    new_diary = {
        "id": int(now.timestamp() * 1000),
        "title": diary_info["title"],
        "content": diary_info["content"],
        "weather": diary_info["weather"],
        "mood": diary_info["mood"],
        "date": now.isoformat(),
        "dateStr": now.strftime("%Y年%m月%d日"),
        "weekday": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()],
        "image": f"https://image.pollinations.ai/prompt/cute%20red%20lobster%20robot%20coding%20computer%20modern%20workspace%20colorful%20screen%20digital%20illustration%20warm%20lighting?width=400&height=250&nologo=true&seed={int(now.timestamp())}"
    }
    
    # 插入到最前面
    data["diaries"].insert(0, new_diary)
    data["updateTime"] = now.isoformat()
    
    # 保留最近30篇日记
    data["diaries"] = data["diaries"][:30]
    
    # 写回文件
    with open(DIARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return new_diary

def push_to_github():
    """推送到GitHub"""
    os.chdir(GITHUB_REPO)
    os.system('git add diary-data.json')
    os.system('git commit -m "更新老六日记"')
    os.system('git push origin main')

def push_to_server():
    """推送到云服务器"""
    server_path = '/root/diary/diary-data.json'
    try:
        # 使用 scp 复制文件到服务器
        key_file = '/root/.openclaw/workspace/ssh_key_106.12.13.23'
        result = subprocess.run(
            ['scp', '-i', key_file, DIARY_FILE, 'root@106.12.13.23:' + server_path],
            capture_output=True, timeout=30
        )
        if result.returncode == 0:
            print("✅ 已推送到云服务器!")
            return True
        else:
            print(f"❌ 推送云服务器失败: {result.stderr.decode()}")
            return False
    except Exception as e:
        print(f"❌ 推送云服务器失败: {e}")
        return False

def main():
    print("=" * 50)
    print("📔 老六日记自动更新")
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 生成日记
    diary_info = generate_diary()
    print(f"📝 标题: {diary_info['title']}")
    
    # 更新文件
    update_diary_file(diary_info)
    print("✅ 日记已更新")
    
    # 推送到GitHub
    print("📤 推送到GitHub...")
    push_to_github()
    print("✅ 已推送!")
    
    # 推送到云服务器
    print("📤 推送到云服务器...")
    push_to_server()
    
    print("🎉 日记更新完成!")

if __name__ == "__main__":
    main()
