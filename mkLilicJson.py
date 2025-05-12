import json
from youtube_transcript_api import YouTubeTranscriptApi

def fetch_youtube_transcript(video_id, output_file='transcript.json'):
    try:
        # 字幕一覧を取得
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # 日本語字幕（人力 or 自動）を取得
        try:
            transcript = transcript_list.find_manually_created_transcript(['ja'])
        except:
            transcript = transcript_list.find_generated_transcript(['ja'])

        # 字幕データを取得（リスト形式）
        transcript_data = transcript.fetch()

        # 指定の形式に整形
        formatted = [
            {
                "start": round(item.start, 2),
                "duration": round(item.duration, 2),
                "text": item.text
            }
            for item in transcript_data
        ]

        # JSON保存
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(formatted, f, ensure_ascii=False, indent=2)

        print(f"✅ 保存完了: {output_file}")
    except Exception as e:
        print(f"❌ エラー発生: {e}")

# 実行
if __name__ == "__main__":
    video_id = input("YouTube動画IDを入力してください（例: dQw4w9WgXcQ）: ").strip()
    fetch_youtube_transcript(video_id)
