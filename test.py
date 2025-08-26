import cv2
from moviepy import VideoFileClip, AudioFileClip

def resize_video(name: str) -> str:
    input_path = f"videos/input_{name}.mp4"
    temp_video_path = f"videos/output_no_audio_{name}.mp4"
    output_path = f"videos/output_with_audio_{name}.mp4"

    # Чтение видео с помощью OpenCV
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError(f"Не удалось открыть видеофайл: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (600, 600))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized = cv2.resize(frame, (600, 600))
        out.write(resized)

    cap.release()
    out.release()

    # Добавление аудио с помощью MoviePy
    video_clip = VideoFileClip(temp_video_path)
    audio_clip = AudioFileClip(input_path)
    final_clip = video_clip.with_audio(audio_clip)

    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

resize_video("5207969556")
