import os
import cv2
import ffmpeg
from PIL import Image
import numpy as np

def get_video_metadata(video_file):
    """Extract video metadata ? why was this again"""
    probe = ffmpeg.probe(video_file)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    
    if video_stream is None:
        raise ValueError("no video stream in file")
    
    metadata = {
        'width': int(video_stream['width']),
        'height': int(video_stream['height']),
        'bit_rate': int(video_stream['bit_rate']),
        'frame_rate': eval(video_stream['r_frame_rate']), 
        'duration': float(video_stream['duration']),
    }
    
    return metadata

def extract_frames(video_file, output_folder, target_width, target_height, bit_depth):
    """extract frame and save as png with consistent bit depth of 8"""
    # open video
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        print("cannot open this video file")
        return
    
    # create folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # exit when video ends
        
        resized_frame = cv2.resize(frame, (target_width, target_height))

        #BGR = openCV format, RGB = pil format
        image = Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB))
        
        #we want this constant to avoid the player imploding again
        if bit_depth == 8:
            # convert to 8 bit per channel if neccesary
            image = image.convert('RGB')

        # save the image
        output_file = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        image.save(output_file)
        frame_count += 1
    
    cap.release()
    print(f"Extracted {frame_count} frames to {output_folder}")

if __name__ == "__main__":
    video_file = 'badapple.mp4'
    output_folder = 'apple'

    #target values
    target_width = 64
    target_height = 36
    bit_depth = 8

    metadata = get_video_metadata(video_file)
    print("Video Metadata:", metadata)

    extract_frames(video_file, output_folder, target_width, target_height, bit_depth)
