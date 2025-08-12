__author__ = 'Mr. Pangu'

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import subprocess
import json
import os
import time
from urllib.request import urlretrieve
from PIL import Image, ImageTk
import requests
from io import BytesIO

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Youder - Youtube Downloader")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.video_info = None
        self.download_thread = None
        self.start_time = None
        self.output_dir = os.path.normpath(os.path.expanduser("~/Downloads"))
        self.format_types = {}  # Store format types for smart handling
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL input section
        url_frame = ttk.LabelFrame(main_frame, text="YouTube Video URL", padding="5")
        url_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=70)
        url_entry.grid(row=0, column=0, padx=(0, 5))
        
        fetch_btn = ttk.Button(url_frame, text="Fetch Info", command=self.fetch_video_info)
        fetch_btn.grid(row=0, column=1)
        
        # Video info section
        self.info_frame = ttk.LabelFrame(main_frame, text="Video Information", padding="5")
        self.info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Thumbnail
        self.thumbnail_label = ttk.Label(self.info_frame)
        self.thumbnail_label.grid(row=0, column=0, rowspan=4, padx=(0, 10))
        
        # Video details
        self.title_label = ttk.Label(self.info_frame, text="", wraplength=400, justify="left")
        self.title_label.grid(row=0, column=1, sticky=(tk.W), pady=2)
        
        self.uploader_label = ttk.Label(self.info_frame, text="")
        self.uploader_label.grid(row=1, column=1, sticky=(tk.W), pady=2)
        
        self.duration_label = ttk.Label(self.info_frame, text="")
        self.duration_label.grid(row=2, column=1, sticky=(tk.W), pady=2)
        
        self.view_count_label = ttk.Label(self.info_frame, text="")
        self.view_count_label.grid(row=3, column=1, sticky=(tk.W), pady=2)
        
        # Quality selection section
        quality_frame = ttk.LabelFrame(main_frame, text="Download Quality", padding="5")
        quality_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(quality_frame, text="Select Quality:").grid(row=0, column=0, padx=(0, 5))
        
        self.quality_var = tk.StringVar()
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                                         state="readonly", width=50)
        self.quality_combo.grid(row=0, column=1, padx=(0, 10))
        
        # Output directory section
        dir_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="5")
        dir_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.dir_var = tk.StringVar(value=self.output_dir)
        dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_var, width=60, state="readonly")
        dir_entry.grid(row=0, column=0, padx=(0, 5))
        
        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_btn.grid(row=0, column=1)
        
        # Download section
        download_frame = ttk.LabelFrame(main_frame, text="Download", padding="5")
        download_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.download_btn = ttk.Button(download_frame, text="Start Download", 
                                      command=self.start_download, state="disabled")
        self.download_btn.grid(row=0, column=0, pady=(0, 10))
        
        # Progress section
        self.progress_var = tk.StringVar(value="Ready to download...")
        progress_label = ttk.Label(download_frame, textvariable=self.progress_var)
        progress_label.grid(row=1, column=0, sticky=(tk.W), pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(download_frame, mode='determinate', length=400)
        self.progress_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.time_label = ttk.Label(download_frame, text="")
        self.time_label.grid(row=3, column=0, sticky=(tk.W))
        
        # Status bar
        self.status_var = tk.StringVar(value="Enter a YouTube URL to get started")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief="sunken")
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Footer with developer info (centered)
        footer_frame = ttk.Frame(main_frame, padding="5")
        footer_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))

        try:
            github_username = "PurushothMathav"
            avatar_url = f"https://github.com/{github_username}.png"
            response = requests.get(avatar_url, timeout=5)
            avatar_img = Image.open(BytesIO(response.content))
            avatar_img.thumbnail((32, 32), Image.Resampling.LANCZOS)
            avatar_photo = ImageTk.PhotoImage(avatar_img)

            # Inner frame to hold avatar + text
            inner_frame = ttk.Frame(footer_frame)
            inner_frame.pack(anchor="center")  # Center horizontally

            avatar_label = ttk.Label(inner_frame, image=avatar_photo, cursor="hand2")
            avatar_label.image = avatar_photo
            avatar_label.pack(side=tk.LEFT, padx=(0, 5))

            def open_github(event):
                import webbrowser
                webbrowser.open(f"https://github.com/{github_username}")

            avatar_label.bind("<Button-1>", open_github)

            dev_label = ttk.Label(
                inner_frame,
                text=f"Developed by {github_username}",
                foreground="blue",
                cursor="hand2"
            )
            dev_label.pack(side=tk.LEFT)
            dev_label.bind("<Button-1>", open_github)

        except Exception:
            ttk.Label(footer_frame, text="Developed by Mr. Pangu").pack(anchor="center")

# Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        url_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        quality_frame.columnconfigure(1, weight=1)
        dir_frame.columnconfigure(0, weight=1)
        download_frame.columnconfigure(0, weight=1)
        
    def fetch_video_info(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        self.status_var.set("Fetching video information...")
        self.download_btn.config(state="disabled")
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._fetch_video_info_thread, args=(url,))
        thread.daemon = True
        thread.start()
        
    def _fetch_video_info_thread(self, url):
        try:
            # Get video info using yt-dlp with additional options to handle YouTube issues
            cmd = [
                'yt-dlp', 
                '--dump-json',
                '--no-download',
                '--no-check-certificates',
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                '--referer', 'https://www.youtube.com/',
                '--extractor-retries', '3',
                '--fragment-retries', '3',
                '--retry-sleep', '1',
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.video_info = json.loads(result.stdout)
            
            # Update GUI in main thread
            self.root.after(0, self._update_video_info)
            
        except subprocess.CalledProcessError as e:
            # Try to update yt-dlp and retry once
            self.root.after(0, lambda: self._try_update_ytdlp(url, e.stderr))
        except json.JSONDecodeError:
            self.root.after(0, lambda: self._show_error("Failed to parse video information"))
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Unexpected error: {str(e)}"))
            
    def _update_video_info(self):
        if not self.video_info:
            return
            
        # Update video details
        title = self.video_info.get('title', 'Unknown Title')
        uploader = self.video_info.get('uploader', 'Unknown Uploader')
        duration = self.video_info.get('duration', 0)
        view_count = self.video_info.get('view_count', 0)
        
        self.title_label.config(text=f"Title: {title}")
        self.uploader_label.config(text=f"Uploader: {uploader}")
        
        # Format duration
        if duration:
            minutes, seconds = divmod(duration, 60)
            hours, minutes = divmod(minutes, 60)
            if hours:
                duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                duration_str = f"{minutes:02d}:{seconds:02d}"
            self.duration_label.config(text=f"Duration: {duration_str}")
        else:
            self.duration_label.config(text="Duration: Unknown")
            
        # Format view count
        if view_count:
            self.view_count_label.config(text=f"Views: {view_count:,}")
        else:
            self.view_count_label.config(text="Views: Unknown")
            
        # Load thumbnail
        self._load_thumbnail()
        
        # Update quality options
        self._update_quality_options()
        
        self.download_btn.config(state="normal")
        self.status_var.set("Video information loaded successfully")
        
    def _load_thumbnail(self):
        try:
            thumbnail_url = self.video_info.get('thumbnail')
            if thumbnail_url:
                # Download thumbnail
                response = requests.get(thumbnail_url, timeout=10)
                img = Image.open(BytesIO(response.content))
                
                # Resize thumbnail
                img.thumbnail((160, 120), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                self.thumbnail_label.config(image=photo)
                self.thumbnail_label.image = photo  # Keep a reference
        except Exception as e:
            print(f"Failed to load thumbnail: {e}")
            
    def _update_quality_options(self):
        formats = self.video_info.get('formats', [])
        quality_options = []
        self.format_types = {}  # Reset format types
        
        # Separate video-only, audio-only, and combined formats
        video_formats = []
        combined_formats = []
        audio_formats = []
        
        for fmt in formats:
            vcodec = fmt.get('vcodec', 'none')
            acodec = fmt.get('acodec', 'none')
            height = fmt.get('height', 0)
            fps = fmt.get('fps', 0)
            filesize = fmt.get('filesize') or fmt.get('filesize_approx', 0)
            ext = fmt.get('ext', 'unknown')
            format_id = fmt['format_id']
            
            if vcodec != 'none' and acodec != 'none' and height > 0:
                # Combined video+audio formats
                size_str = f" (~{filesize // (1024*1024)}MB)" if filesize else ""
                fps_str = f"@{fps}fps" if fps else ""
                quality_str = f"{height}p{fps_str} ({ext}) [Combined]{size_str}"
                combined_formats.append((height, fps, format_id, quality_str))
                
            elif vcodec != 'none' and acodec == 'none' and height > 0:
                # Video-only formats (higher quality)
                size_str = f" (~{filesize // (1024*1024)}MB)" if filesize else ""
                fps_str = f"@{fps}fps" if fps else ""
                quality_str = f"{height}p{fps_str} ({ext}) [Video Only - Will Auto-Merge Audio]{size_str}"
                video_formats.append((height, fps, format_id, quality_str))
                
            elif vcodec == 'none' and acodec != 'none':
                # Audio-only formats
                abr = fmt.get('abr', 0)
                size_str = f" (~{filesize // (1024*1024)}MB)" if filesize else ""
                bitrate_str = f" {abr}kbps" if abr else ""
                quality_str = f"Audio Only ({ext}){bitrate_str}{size_str}"
                audio_formats.append((abr or 0, 0, format_id, quality_str))
        
        # Sort formats by quality
        video_formats.sort(key=lambda x: (x[0], x[1]), reverse=True)
        combined_formats.sort(key=lambda x: (x[0], x[1]), reverse=True)
        audio_formats.sort(key=lambda x: x[0], reverse=True)
        
        # Add auto-select options first
        quality_options.append(("best", "🏆 Best Quality Available (Auto-select)"))
        self.format_types["🏆 Best Quality Available (Auto-select)"] = "auto"
        
        quality_options.append(("best[height<=?1080]", "🎯 Best Quality ≤1080p (Recommended)"))
        self.format_types["🎯 Best Quality ≤1080p (Recommended)"] = "auto"
        
        quality_options.append(("best[height<=?720]", "📱 Best Quality ≤720p (Mobile Friendly)"))
        self.format_types["📱 Best Quality ≤720p (Mobile Friendly)"] = "auto"
        
        # Add video-only formats (these will auto-merge with best audio)
        if video_formats:
            quality_options.append(("separator1", "--- High Quality Video (Auto-Merges with Best Audio) ---"))
            for height, fps, format_id, quality_str in video_formats[:8]:  # Top 8 video qualities
                quality_options.append((format_id, quality_str))
                self.format_types[quality_str] = "video_only"
        
        # Add combined formats (if any good ones exist)
        if combined_formats:
            quality_options.append(("separator2", "--- Combined Video+Audio (Direct Download) ---"))
            for height, fps, format_id, quality_str in combined_formats[:5]:  # Top 5 combined
                quality_options.append((format_id, quality_str))
                self.format_types[quality_str] = "combined"
        
        # Add audio-only formats
        if audio_formats:
            quality_options.append(("separator3", "--- Audio Only ---"))
            quality_options.append(("bestaudio", "🎵 Best Audio Quality (Auto-select)"))
            self.format_types["🎵 Best Audio Quality (Auto-select)"] = "audio_only"
            
            for abr, _, format_id, quality_str in audio_formats[:3]:  # Top 3 audio qualities
                quality_options.append((format_id, quality_str))
                self.format_types[quality_str] = "audio_only"
        
        # Filter out separators for the format mapping
        format_options = [(opt[0], opt[1]) for opt in quality_options if not opt[0].startswith("separator")]
        
        # Update combobox (including separators for display)
        display_values = []
        for format_id, description in quality_options:
            if format_id.startswith("separator"):
                display_values.append(description)  # Separator text
            else:
                display_values.append(description)
        
        self.quality_combo['values'] = display_values
        self.quality_formats = {desc: fmt_id for fmt_id, desc in format_options}
        
        if quality_options:
            self.quality_combo.current(0)  # Select "Best Quality Available"
            
    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir)
        if directory:
            self.output_dir = directory
            self.dir_var.set(directory)
            
    def start_download(self):
        if not self.video_info:
            messagebox.showerror("Error", "Please fetch video information first")
            return
            
        if not self.quality_var.get():
            messagebox.showerror("Error", "Please select a quality")
            return
            
        self.download_btn.config(state="disabled")
        self.progress_bar['value'] = 0
        self.progress_var.set("Starting download...")
        self.start_time = time.time()
        
        # Start download in separate thread
        self.download_thread = threading.Thread(target=self._download_thread)
        self.download_thread.daemon = True
        self.download_thread.start()
        
    def _download_thread(self):
        try:
            selected_quality = self.quality_var.get()
            format_id = self.quality_formats.get(selected_quality, 'best')
            url = self.url_var.get().strip()
            format_type = self.format_types.get(selected_quality, "auto")
            
            # Get video title for safe filename
            video_title = self.video_info.get('title', 'video').replace('/', '_').replace('\\', '_')
            safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            # Base command options
            base_cmd = [
                'yt-dlp',
                '-o', os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                '--no-check-certificates',
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                '--referer', 'https://www.youtube.com/',
                '--extractor-retries', '3',
                '--fragment-retries', '10',
                '--retry-sleep', '1',
                '--file-access-retries', '3',
                '--embed-metadata',  # Add metadata to the file
                '--embed-thumbnail',  # Embed thumbnail in video file
                '--newline'
            ]
            
            # Handle different format types
            if format_type == "video_only":
                # For video-only formats, explicitly download video + best audio and merge
                self.root.after(0, lambda: self.progress_var.set("Downloading video and audio streams..."))
                cmd = base_cmd + [
                    '-f', f"{format_id}+bestaudio",  # Download specific video + best audio
                    '--merge-output-format', 'mp4',  # Force merge to mp4
                    '--embed-subs',  # Also embed subtitles if available
                    url
                ]
            elif format_type == "audio_only":
                # For audio-only, just download audio (no thumbnail embedding for audio)
                self.root.after(0, lambda: self.progress_var.set("Downloading audio stream..."))
                cmd = [
                    'yt-dlp',
                    '-o', os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                    '--no-check-certificates',
                    '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    '--referer', 'https://www.youtube.com/',
                    '--extractor-retries', '3',
                    '--fragment-retries', '10',
                    '--retry-sleep', '1',
                    '--file-access-retries', '3',
                    '--embed-metadata',  # Add metadata to audio file
                    '--newline',
                    '-f', format_id,
                    '--extract-audio',  # Ensure audio extraction
                    url
                ]
            else:
                # For auto-select and combined formats
                self.root.after(0, lambda: self.progress_var.set("Downloading..."))
                cmd = base_cmd + [
                    '-f', format_id,
                    '--merge-output-format', 'mp4',  # Merge to mp4 when possible
                    '--embed-subs',  # Also embed subtitles if available
                    url
                ]
            
            # Check if ffmpeg is available for merging and thumbnail embedding
            ffmpeg_available = self._check_ffmpeg()
            if not ffmpeg_available:
                if format_type == "video_only":
                    self.root.after(0, lambda: messagebox.showwarning(
                        "FFmpeg Not Found",
                        "FFmpeg is required for:\n"
                        "• Merging video and audio streams\n"
                        "• Embedding thumbnails in video files\n"
                        "• Embedding subtitles\n\n"
                        "Please install FFmpeg for full functionality.\n"
                        "The download will proceed but may lack these features."
                    ))
                elif format_type != "audio_only":
                    self.root.after(0, lambda: messagebox.showinfo(
                        "FFmpeg Recommended",
                        "FFmpeg is recommended for:\n"
                        "• Embedding thumbnails in video files\n"
                        "• Better video processing\n\n"
                        "Download will proceed without thumbnail embedding."
                    ))
            
            # Start download process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True
            )
            
            # Monitor progress
            for line in process.stdout:
                line = line.strip()
                if '[download]' in line and '%' in line:
                    self._parse_progress(line)
                elif '[Merger]' in line or 'Merging formats' in line:
                    self.root.after(0, lambda: self.progress_var.set("Merging video and audio streams..."))
                elif '[EmbedThumbnail]' in line or 'thumbnail' in line.lower():
                    self.root.after(0, lambda: self.progress_var.set("Embedding thumbnail..."))
                elif '[EmbedSubtitle]' in line or 'subtitle' in line.lower():
                    self.root.after(0, lambda: self.progress_var.set("Embedding subtitles..."))
                elif 'Deleting original file' in line:
                    self.root.after(0, lambda: self.progress_var.set("Cleaning up temporary files..."))
                elif '[ExtractAudio]' in line:
                    self.root.after(0, lambda: self.progress_var.set("Extracting audio..."))
                elif '[Metadata]' in line:
                    self.root.after(0, lambda: self.progress_var.set("Adding metadata..."))
                    
            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, self._download_complete)
            else:
                self.root.after(0, lambda: self._download_error("Download failed. Check if the video is available and try again."))
                
        except Exception as e:
            self.root.after(0, lambda: self._download_error(f"Download error: {str(e)}"))
    
    def _check_ffmpeg(self):
        """Check if ffmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def _parse_progress(self, line):
        try:
            # Parse progress line from yt-dlp
            if '%' in line and 'of' in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if '%' in part:
                        progress = float(part.replace('%', ''))
                        self.root.after(0, lambda p=progress: self._update_progress(p))
                        break
        except:
            pass
            
    def _update_progress(self, progress):
        self.progress_bar['value'] = progress
        
        elapsed_time = time.time() - self.start_time
        
        if progress > 0:
            total_time = elapsed_time * 100 / progress
            remaining_time = total_time - elapsed_time
            
            elapsed_str = self._format_time(elapsed_time)
            remaining_str = self._format_time(remaining_time)
            
            self.progress_var.set(f"Downloading... {progress:.1f}%")
            self.time_label.config(text=f"Elapsed: {elapsed_str} | Remaining: {remaining_str}")
        else:
            self.progress_var.set("Downloading... 0.0%")
            
    def _format_time(self, seconds):
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds//60)}m {int(seconds%60)}s"
        else:
            return f"{int(seconds//3600)}h {int((seconds%3600)//60)}m"
            
    def _download_complete(self):
        self.progress_bar['value'] = 100
        self.progress_var.set("Download completed successfully!")
        elapsed_time = time.time() - self.start_time
        self.time_label.config(text=f"Total time: {self._format_time(elapsed_time)}")
        self.download_btn.config(state="normal")
        self.status_var.set("Download completed")
        messagebox.showinfo("Success", "Video downloaded successfully!")
        
    def _download_error(self, error_msg):
        self.progress_var.set("Download failed")
        self.download_btn.config(state="normal")
        self.status_var.set("Download failed")
        messagebox.showerror("Download Error", error_msg)
        
    def _try_update_ytdlp(self, url, error_msg):
        """Try to update yt-dlp and retry fetching video info"""
        response = messagebox.askyesno(
            "yt-dlp Update Required", 
            "The video fetch failed, likely due to YouTube changes. "
            "Would you like to try updating yt-dlp and retry?\n\n"
            "This will run: pip install --upgrade yt-dlp"
        )
        
        if response:
            self.status_var.set("Updating yt-dlp...")
            thread = threading.Thread(target=self._update_ytdlp_thread, args=(url,))
            thread.daemon = True
            thread.start()
        else:
            detailed_error = (
                "Failed to fetch video info. YouTube frequently changes their systems, "
                "causing temporary issues with yt-dlp.\n\n"
                "Suggestions:\n"
                "1. Update yt-dlp: pip install --upgrade yt-dlp\n"
                "2. Try a different video URL\n"
                "3. Wait a few minutes and try again\n\n"
                f"Technical details:\n{error_msg[:500]}..."
            )
            self._show_error(detailed_error)
    
    def _update_ytdlp_thread(self, url):
        """Update yt-dlp in a separate thread"""
        try:
            # Update yt-dlp
            update_cmd = ['pip', 'install', '--upgrade', 'yt-dlp']
            subprocess.run(update_cmd, capture_output=True, text=True, check=True)
            
            # Wait a moment and retry
            time.sleep(2)
            self.root.after(0, lambda: self.status_var.set("Retrying video fetch..."))
            
            # Retry fetching video info
            self._fetch_video_info_thread(url)
            
        except Exception as e:
            error_msg = f"Failed to update yt-dlp: {str(e)}"
            self.root.after(0, lambda: self._show_error(error_msg))

    def _show_error(self, error_msg):
        self.status_var.set("Error occurred")
        messagebox.showerror("Error", error_msg)

def main():
    # Check if yt-dlp is installed
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True, text=True)
        version = result.stdout.strip()
        print(f"yt-dlp version: {version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        response = messagebox.askyesno(
            "yt-dlp Not Found",
            "yt-dlp is required but not found.\n\n"
            "Would you like to install it automatically?\n"
            "This will run: pip install yt-dlp"
        )
        if response:
            try:
                subprocess.run(['pip', 'install', 'yt-dlp'], check=True)
                messagebox.showinfo("Success", "yt-dlp installed successfully!")
            except subprocess.CalledProcessError:
                messagebox.showerror(
                    "Installation Failed",
                    "Failed to install yt-dlp automatically.\n\n"
                    "Please install it manually using:\n"
                    "pip install yt-dlp\n\n"
                    "Or visit: https://github.com/yt-dlp/yt-dlp"
                )
                return
        else:
            return
    
    # Check if ffmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("FFmpeg is available for video/audio merging")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: FFmpeg not found. Video+audio merging may not work properly.")
        print("Install FFmpeg from: https://ffmpeg.org/download.html")
    
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()