import os
import whisper
import yt_dlp
import ffmpeg
import uuid

def download_audio(video_id, output_path='audio.mp3'):
    url = f'https://www.youtube.com/watch?v={video_id}'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"🔽 音声をダウンロード中: {url}")
        ydl.download([url])
    os.rename('temp.mp3', output_path)
    print(f"✅ 音声保存完了: {output_path}")

def transcribe_audio(audio_path, json_path):
    print("🧠 Whisperによる文字起こしを実行中...")
    model = whisper.load_model("medium")  # 'base', 'small', 'medium', 'large' が選べる
    result = model.transcribe(audio_path, language='ja')
    
    output = []
    for segment in result['segments']:
        output.append({
            "start": round(segment['start'], 2),
            "duration": round(segment['end'] - segment['start'], 2),
            "text": segment['text'].strip()
        })

    with open(json_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ 字幕ファイル出力完了: {json_path}")

def main():
    video_id = input("🎥 YouTubeの動画IDを入力してください: ").strip()
    audio_file = f'{video_id}_{uuid.uuid4().hex}.mp3'
    json_file = f'{video_id}.json'

    download_audio(video_id, output_path=audio_file)
    transcribe_audio(audio_file, json_path=json_file)

    # クリーンアップ
    os.remove(audio_file)
    print(f"🎉 完了！ {json_file} が生成されました。")

if __name__ == "__main__":
    main()
