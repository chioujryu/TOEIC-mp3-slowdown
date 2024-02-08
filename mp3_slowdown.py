"""
MP3 File Speed Changer

This script allows users to change the playback speed of MP3 files in a specified folder. 
The script will create a new folder with modified files, where the folder name indicates 
the speed change (e.g., "_speed80" for 80% speed).

Usage:
    Run this script with two arguments:
    1. The path to the folder containing the MP3 files you want to modify.
    2. The speed factor to apply:
        - Less than 1 to slow down the playback speed.
        - More than 1 to increase the playback speed.
        
    Example command:
    python mp3_slowdown.py "path/to/your/folder" 0.8
    
    This will slow down the playback speed of all MP3 files in the specified folder to 80% of their original speed.

Requirements:
    - Python 3
    - pydub library
    - ffmpeg installed and accessible in the system's PATH.
"""


from pydub import AudioSegment
import os
import argparse

# 調整速度的函數
def change_speed(sound, speed=1.0):
    # Change the audio speed while keeping the same pitch
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

# 主函數
def slow_down_mp3(input_folder, speed_factor=0.5):
    # 計算速度百分比，用於資料夾命名
    speed_percentage = int(speed_factor * 100)
    
    # 遍歷輸入資料夾
    for root, dirs, files in os.walk(input_folder):
        for name in dirs:
            original_dir_path = os.path.join(root, name)
            # 根據速度因子修改資料夾名稱
            new_dir = f"{original_dir_path}_speed{speed_percentage}"
            os.makedirs(new_dir, exist_ok=True)
        
        for file in files:
            if file.endswith('.mp3'):
                original_path = os.path.join(root, file)
                # 修改這裡以正確建立新路徑
                new_dir_root = f"{root}_speed{speed_percentage}"
                os.makedirs(new_dir_root, exist_ok=True)  # 確保新目錄存在
                new_path = os.path.join(new_dir_root, file)
                
                # 讀取MP3檔案
                sound = AudioSegment.from_file(original_path)
                
                # 調整速度
                slower_sound = change_speed(sound, speed_factor)
                
                # 儲存新的MP3檔案
                slower_sound.export(new_path, format="mp3")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MP3 File Speed Changer')
    parser.add_argument('input_folder', type=str, help='Path to the folder containing MP3 files')
    parser.add_argument('speed_factor', type=float, help='Speed factor (less than 1 to slow down, more than 1 to speed up)')
    
    args = parser.parse_args()
    
    slow_down_mp3(args.input_folder, args.speed_factor)