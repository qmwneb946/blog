import google.generativeai as genai
import os
import random
from datetime import datetime
import re
import sys

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("错误: GEMINI_API_KEY 未在 GitHub Secrets 中设置。")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 主题和提示词 ---
TOPICS = [
    "微积分的历史", "P vs NP 问题", "量子计算基础", "人工智能在软件开发中的作用",
    "深入探讨神经网络", "理解区块链技术", "欧拉恒等式的优雅", "图论入门",
    "探索斐波那契数列", "密码学基础", "可再生能源技术的未来", "使用 Docker 进行容器化的初学者指南",
    "无服务器架构解析", "5G 技术的影响", "函数式编程原理", "机器学习算法概述",
    "数据结构的重要性", "编译器是如何工作的", "探索曼德博集合"
]

def generate_prompt():
    """选择一个随机主题并为 AI 创建详细的提示。"""
    topic = random.choice(TOPICS)
    prompt = (
        f"你是一位知识渊博的技术和数学博主.你的任务是撰写一篇关于“{topic}”的高质量、有深度的中文博客文章。\n"
        "文章必须结构良好，对技术爱好者有吸引力。\n"
        "输出必须是 Markdown 格式。\n\n"
        "**格式要求:**\n"
        "1.  **标题:** 输出的第一行必须是文章标题，并以 'Title: ' 开头。例如: 'Title: 深入理解神经网络'。\n"
        "2.  **内容:** 在标题行之后，提供完整的 Markdown 格式博客内容。\n"
        "3.  **结构:** 文章应包含引言、包含多个逻辑部分的主体（使用 ## 和 ### 等 Markdown 标题）以及结论段落。\n"
        "4.  **代码块:** 如果适用，请包含注释清晰的代码块。\n"
        "5.  **数学公式:** 对所有数学公式使用 KaTeX 格式，例如 \\( E = mc^2 \\)。\n\n"
        "请现在开始生成这篇博客文章。"
    )
    return prompt

def slugify(text):
    """将标题文本转换为 URL 友好的文件名 (slug)。"""
    # 对于包含中文的标题，使用日期作为文件名更安全，避免乱码问题
    if not all(ord(c) < 128 for c in text):
        return datetime.now().strftime('%Y-%m-%d-%H%M%S')
    text = text.lower()
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^\w-]', '', text)
    text = re.sub(r'--+', '-', text)
    text = text.strip('-')
    return text or datetime.now().strftime('%Y-%m-%d-%H%M%S')

def create_post():
    """生成文章并将其保存为 Markdown 文件。"""
    try:
        print("正在生成中文文章...")
        prompt = generate_prompt()
        response = model.generate_content(prompt)
        
        full_text = response.text
        lines = full_text.splitlines()
        
        if not lines or not lines[0].startswith("Title: "):
            print("AI 响应格式不正确，没有以 'Title: ' 开头。")
            print("完整响应内容:\n", full_text)
            sys.exit(1)
            
        title = lines[0].replace("Title: ", "").strip()
        content = "\n".join(lines[1:]).strip()
        
        print(f"成功生成标题: {title}")

        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d %H:%M:%S')
        filename_slug = slugify(title)
        filename = f"{filename_slug}.md"
        
        # 随机选择分类和标签
        categories = random.choice([["技术"], ["数学"], ["计算机科学"]])
        tags = [categories[0], now.strftime('%Y')]

        # 将 tags 和 categories 格式化为字符串
        tags_str = "\n".join([f"  - {tag}" for tag in tags])
        categories_str = "\n".join([f"  - {cat}" for cat in categories])

        # 创建 Hexo 的 front-matter
        front_matter = f'''---
title: {title}
date: {date_str}
tags:
{tags_str}
categories:
{categories_str}
---

'''
        
        final_content = front_matter + content
        filepath = os.path.join("source", "_posts", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        print(f"成功创建博客文章: {filepath}")
        # 设置输出，以便在后续步骤中使用
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f'title={title}', file=fh)

    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_post()
