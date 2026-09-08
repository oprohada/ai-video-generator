import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip
import cv2
from gtts import gTTS
import tempfile
import textwrap

class AIVideoGenerator:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.colors = {
            'backgrounds': [
                [(30, 144, 255), (255, 105, 180)],   # Blue to Pink
                [(255, 200, 100), (255, 150, 50)],   # Orange gradient
                [(200, 220, 240), (150, 180, 220)], # Light blue
                [(135, 206, 250), (70, 130, 180)],   # Sky blue
                [(240, 128, 128), (220, 20, 60)]     # Red gradient
            ]
        }
    
    def create_from_text(self, text, duration=30, voice_speed=1.0, output_path='output.mp4', progress_callback=None):
        """Generate video from text description"""
        print(f"Starting video generation for: {text}")
        
        # Step 0: Split text into scenes (20%)
        scenes = self._split_into_scenes(text, num_scenes=min(4, max(2, len(text.split()) // 15)))
        if progress_callback:
            progress_callback(0, 5)
        
        # Step 1: Generate images (40%)
        image_clips = []
        scene_duration = duration / len(scenes)
        
        for i, scene in enumerate(scenes):
            print(f"Generating image for scene {i+1}: {scene}")
            img = self._generate_scene_image(scene, i)
            
            # Add animation effect
            clip = ImageClip(np.array(img)).set_duration(scene_duration)
            image_clips.append(clip)
        
        if progress_callback:
            progress_callback(1, 5)
        
        # Step 2: Create video from images (60%)
        print("Concatenating images into video...")
        video = concatenate_videoclips(image_clips)
        
        if progress_callback:
            progress_callback(2, 5)
        
        # Step 3: Generate and add speech (80%)
        print("Generating voice-over...")
        audio_path = self._generate_speech(text, voice_speed)
        
        if audio_path and os.path.exists(audio_path):
            try:
                audio = AudioFileClip(audio_path)
                # Adjust video to match audio
                if video.duration < audio.duration:
                    video = video.speedx(video.duration / audio.duration)
                video = video.set_audio(audio)
            except Exception as e:
                print(f"Could not add audio: {e}")
        
        if progress_callback:
            progress_callback(3, 5)
        
        # Step 4: Save video (95%)
        print(f"Saving video to {output_path}...")
        video.write_videofile(output_path, verbose=False, logger=None, fps=24, codec='libx264', audio_codec='aac')
        
        if progress_callback:
            progress_callback(4, 5)
        
        print(f"Video successfully saved to {output_path}")
    
    def _generate_scene_image(self, text, scene_index):
        """Generate a beautiful image for a scene"""
        width, height = 1280, 720
        img = Image.new('RGB', (width, height))
        
        # Select gradient colors
        colors = self.colors['backgrounds'][scene_index % len(self.colors['backgrounds'])]
        
        # Create gradient background
        pixels = img.load()
        for y in range(height):
            ratio = y / height
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        # Add shapes/circles for visual interest
        draw = ImageDraw.Draw(img)
        
        # Draw decorative circles
        circle_color = tuple(colors[0])
        draw.ellipse([100, 50, 300, 250], fill=circle_color, outline=None)
        draw.ellipse([width-300, height-250, width-100, height-50], fill=colors[1], outline=None)
        
        # Add text with shadow
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            font = ImageFont.load_default()
            font_small = font
        
        # Wrap text
        wrapped_text = self._wrap_text(text, 35)
        
        # Calculate text position
        text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw shadow effect
        draw.text((x + 4, y + 4), wrapped_text, fill=(0, 0, 0, 128), font=font, align="center")
        # Draw main text
        draw.text((x, y), wrapped_text, fill=(255, 255, 255), font=font, align="center")
        
        # Add scene number
        scene_text = f"Scene {scene_index + 1}"
        draw.text((30, 30), scene_text, fill=(255, 255, 255), font=font_small)
        
        return img
    
    def _generate_speech(self, text, speed=1.0):
        """Generate speech from text using Google Text-to-Speech"""
        try:
            print(f"Converting text to speech...")
            
            # Limit text length for TTS
            if len(text) > 300:
                text = text[:300] + "..."
            
            audio_path = os.path.join(self.temp_dir, 'speech.mp3')
            
            # Use gTTS for free text-to-speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(audio_path)
            
            return audio_path
        except Exception as e:
            print(f"Speech generation failed: {e}")
            return None
    
    def _split_into_scenes(self, text, num_scenes=4):
        """Split text into multiple scenes"""
        sentences = text.split('. ')
        
        if len(sentences) <= num_scenes:
            return [s.strip() + '.' for s in sentences if s.strip()]
        
        scenes_per_sentence = max(1, len(sentences) // num_scenes)
        scenes = []
        
        for i in range(0, len(sentences), scenes_per_sentence):
            scene = '. '.join(sentences[i:i + scenes_per_sentence])
            if scene.strip():
                scenes.append(scene.strip())
        
        return scenes[:num_scenes]
    
    def _wrap_text(self, text, char_limit=40):
        """Wrap text for display"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > char_limit:
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
