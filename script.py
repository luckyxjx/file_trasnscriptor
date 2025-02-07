import os
import json
import whisper
from pathlib import Path

def find_media_files(directory):
    
    media_extensions = {'.mp3', '.mp4', '.wav', '.m4a' ,'.mov'}
    media_files = []
    
    for root, _, files in os.walk(directory):
        print(f"Folder: {root}")
        for file in files:
            file_path = Path(root) / file
            print(f"  - {file_path.suffix} | {file}")
            if file_path.suffix.lower() in media_extensions:
                media_files.append(file_path)
    
    if media_files:
        print("Media files found.")
    else:
        print("No supported media files found.")
    
    return media_files

def transcribe_media_files(media_files, model):
    transcriptions = {}
    for file_path in media_files:
        print(f"Transcribing: {file_path} ...")
        result = model.transcribe(str(file_path))
        transcriptions[file_path] = result["text"]
    return transcriptions

def save_transcriptions(transcriptions):
    for file_path, transcript_text in transcriptions.items():
        output_dir = file_path.parent / "transcriptions"
        output_dir.mkdir(exist_ok=True)
        
        # Save as .txt
        txt_path = output_dir / f"{file_path.stem}.txt"
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(transcript_text)
        
        # Save as .json
        json_path = output_dir / f"{file_path.stem}.json"
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump({"transcription": transcript_text}, json_file, indent=4)
        
        print(f"Transcription saved: {txt_path}, {json_path}")

def main():
    choice = input("Do you want to scan the current directory? (yes/no): ").strip().lower()
    if choice == 'yes':
        input_path = Path.cwd()
    else:
        input_dir = input("Enter the path of the directory to scan: ").strip()
        input_path = Path(input_dir)
    
    if not input_path.exists():
        print("Error: Directory does not exist!")
        return
    
    model = whisper.load_model("tiny")
    media_files = find_media_files(input_path)
    if media_files:
        transcriptions = transcribe_media_files(media_files, model)
        save_transcriptions(transcriptions)

if __name__ == "__main__":
    main()


    