import os
import anthropic
from dotenv import load_dotenv

# .envからAPIキーを読み込む
load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def extract_tasks(minutes_text):
    """議事録からタスクを抽出する"""
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""以下の議事録を読んで、やるべきタスクを抽出してください。

## 出力形式
- 担当者名（不明な場合は「未定」）
- タスク内容
- 期限（記載がない場合は「期限なし」）

## 議事録
{minutes_text}

タスク一覧を箇条書きで出力してください。"""
            }
        ]
    )
    
    return message.content[0].text

def main():
    print("=== 議事録タスク抽出ツール ===")
    print("議事録を貼り付けてください。")
    print("入力が終わったら、空行のままEnterを2回押してください。")
    print()
    
    lines = []
    empty_count = 0
    
    while empty_count < 2:
        line = input()
        if line == "":
            empty_count += 1
        else:
            empty_count = 0
            lines.append(line)
    
    minutes_text = "\n".join(lines)
    
    if not minutes_text.strip():
        print("議事録が入力されていません。")
        return
    
    print()
    print("抽出中...")
    print()
    
    result = extract_tasks(minutes_text)
    
    print("=== 抽出されたタスク ===")
    print(result)

if __name__ == "__main__":
    main()