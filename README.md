# 🎬 AI Video Generator - Free Video Creation Tool

Create stunning videos from text descriptions using AI. Completely FREE, no subscriptions, no hidden costs!

## ✨ Features

✅ **Text to Video** - Convert any text into a beautiful animated video
✅ **AI-Generated Scenes** - Automatic scene generation with colorful backgrounds
✅ **Auto Voice-Over** - Text-to-speech narration in professional quality
✅ **Customizable Duration** - Create videos from 10 to 120 seconds
✅ **Voice Speed Control** - Adjust narration speed from 0.5x to 2.0x
✅ **Beautiful UI** - Modern, responsive web interface
✅ **100% Free** - No watermarks, no subscriptions
✅ **Background Processing** - Generate videos without blocking
✅ **Fast Download** - Download your videos directly

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- 2GB free disk space

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/oprohada/ai-video-generator.git
   cd ai-video-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   python app.py
   ```

5. **Open browser**
   Navigate to `http://localhost:5000`

## 📖 How to Use

1. **Write Your Script** - Describe what you want in the video
2. **Set Duration** - Choose video length (10-120 seconds)
3. **Adjust Voice Speed** - Set narration speed (0.5x to 2.0x)
4. **Click Generate** - Start video creation
5. **Download** - Download your video when ready!

## 🎯 Example Scripts

### Story Example
```
Once upon a time, there was a brave knight who traveled through magical forests. 
He encountered dragons, fairies, and wizards on his epic quest. 
After many adventures, he finally discovered the legendary treasure hidden in the mountains.
```

### Educational Example
```
The water cycle is an important process in nature. 
Evaporation takes water from oceans and lakes into the atmosphere. 
Condensation forms clouds, and precipitation brings water back to earth as rain. 
This continuous cycle sustains all life on our planet.
```

### Marketing Example
```
Welcome to our amazing new product! 
It's designed to make your life easier and more productive. 
With cutting-edge technology and beautiful design, this product is perfect for everyone. 
Get yours today and join thousands of satisfied customers!
```

## 🛠️ Technologies Used

- **Flask** - Web framework
- **MoviePy** - Video editing
- **PIL/Pillow** - Image generation
- **gTTS** - Google Text-to-Speech
- **OpenCV** - Image processing
- **NumPy** - Numerical computing

## 📁 Project Structure

```
ai-video-generator/
├── app.py              # Flask server
├── video_generator.py  # Video generation engine
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Web interface
├── output_videos/      # Generated videos (auto-created)
├── README.md           # Documentation
└── .gitignore          # Git configuration
```

## 🎨 Video Generation Process

1. **Scene Splitting** - Breaks text into multiple scenes
2. **Image Generation** - Creates colorful background images for each scene
3. **Video Assembly** - Combines images into video sequence
4. **Voice Generation** - Converts text to speech using Google TTS
5. **Audio Sync** - Synchronizes audio with video
6. **Video Export** - Encodes and saves final video

## 🔧 API Reference

### Generate Video
```bash
POST /api/generate
Content-Type: application/json

{
  "text": "Your video script here",
  "duration": 30,
  "voice_speed": 1.0
}

Response:
{
  "job_id": "uuid-string",
  "status": "started"
}
```

### Check Status
```bash
GET /api/status/{job_id}

Response:
{
  "status": "processing",
  "progress": 45,
  "message": "Generating images..."
}
```

### Download Video
```bash
GET /api/download/{job_id}
```

### Get Statistics
```bash
GET /api/stats

Response:
{
  "total_videos_generated": 42
}
```

## ⚙️ Configuration

### Video Quality
Edit `video_generator.py`:
```python
width, height = 1280, 720  # Resolution
fps = 24                    # Frames per second
```

### Scene Duration
```python
scene_duration = duration / len(scenes)
```

## 📊 Performance Tips

- **Keep scripts under 500 words** for faster generation
- **Use shorter durations** (10-30 seconds) for quick processing
- **First run** may take longer as dependencies load
- **On slower computers** reduce video resolution
- **Run on GPU** (if available) for 5-10x faster generation

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install --upgrade flask moviepy pillow requests gtts numpy opencv-python
```

### Port 5000 already in use
```bash
# Change port in app.py or use:
python -m flask run --port 5001
```

### Video not downloading
- Check `output_videos` folder permissions
- Ensure disk space available
- Try browser's download folder

### Voice not working
- Check internet connection (for Google TTS)
- Verify speaker/audio output
- Try different voice speed

## 🚀 Future Features

- [ ] Multiple voice options
- [ ] Background music library
- [ ] Subtitle generation
- [ ] Scene transitions
- [ ] Special effects
- [ ] Video quality selector
- [ ] Batch processing
- [ ] Cloud storage integration
- [ ] Social media export
- [ ] Analytics dashboard

## 🤝 Contributing

Contributions welcome! 

1. Fork repository
2. Create feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 💬 Support & Feedback

- 🐛 **Bug Reports**: Open an issue
- 💡 **Feature Requests**: Create a discussion
- ❓ **Questions**: Check documentation or ask in discussions
- 📧 **Email**: Include in issues

## 🙏 Acknowledgments

- MoviePy for video editing
- Google for TTS API
- Flask community
- All contributors!

---

**Made with ❤️ to help creators make amazing videos**

*Create. Share. Inspire.* 🎬✨
