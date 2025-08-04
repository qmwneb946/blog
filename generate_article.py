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

def get_topic_from_file(filepath="TOPICS.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if not lines:
            print(f"错误: 主题文件 '{filepath}' 为空。")
            return None
            
        topic = lines[0].strip()
        remaining_lines = lines[1:]
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(remaining_lines)
            
        print(f"已使用主题: '{topic}'。并已从文件中移除。")
        return topic
        
    except FileNotFoundError:
        print(f"错误: 主题文件 '{filepath}' 未找到。")
        return None
    except Exception as e:
        print(f"读取主题文件时发生错误: {e}")
        return None

def generate_prompt_from_topic(topic):
    prompt = (
        f"你是一位知识渊博的技术和数学博主.你的任务是撰写一篇关于“{topic}”的高质量、有深度的中文博客文章。大约 1w 字。博主的名字是 qmwneb946\n"
        "文章必须结构良好，对技术爱好者有吸引力。\n"
        "输出必须是 Markdown 格式。\n\n"
        "**格式要求:**\n"
        "1.  **标题:** 输出的第一行必须是文章标题，并以 'Title: ' 开头。例如: 'Title: 深入理解神经网络'。\n"
        "2.  **内容:** 在标题行之后，提供完整的 Markdown 格式博客内容。\n"
        "3.  **结构:** 文章应包含引言、包含多个逻辑部分的主体（使用 ## 和 ### 等 Markdown 标题）以及结论段落。注意在 ### 后面不要有 1.1 ; 1.2 只要文字就行了,例如 \"### 工作原理\"\n"
        "4.  **代码块:** 如果适用，请包含注释清晰的代码块。\n"
        "5.  **数学公式:** 对所有数学公式使用 KaTeX 格式，例如 $E = mc^2$。\n\n"
        "请现在开始生成这篇博客文章。"
    )
    return prompt

def slugify(text):
    if any(ord(c) > 128 for c in text):
        return datetime.now().strftime('%Y-%m-%d-%H%M%S')
    text = text.lower()
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^\w-]', '', text)
    text = re.sub(r'--+', '-', text)
    text = text.strip('-')
    return text or datetime.now().strftime('%Y-%m-%d-%H%M%S')

def create_post():
    topic = get_topic_from_file("TOPICS.txt")
    if not topic:
        sys.exit(1)

    try:
        print(f"正在为主题 '{topic}' 生成中文文章...")
        prompt = generate_prompt_from_topic(topic)
        
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
        
        categories = random.choice([["技术"], ["数学"], ["计算机科学"], ["科技前沿"]])
        tags = [topic, categories[0], now.strftime('%Y')]

        tags_str = "\n".join([f"  - {tag}" for tag in tags])
        categories_str = "\n".join([f"  - {cat}" for cat in categories])

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
        
        output_dir = os.path.join("source", "_posts")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        print(f"成功创建博客文章: {filepath}")

        if 'GITHUB_OUTPUT' in os.environ:
            with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
                print(f'title={title}', file=fh)

    except Exception as e:
        print(f"创建文章过程中发生错误: {e}")
        with open("TOPICS.txt", "r+", encoding="utf-8") as f:
            content = f.read()
            f.seek(0, 0)
            f.write(topic + '\n' + content)
        print(f"已将主题 '{topic}' 写回 TOPICS.txt 文件。")
        sys.exit(1)

if __name__ == "__main__":
    create_post()
