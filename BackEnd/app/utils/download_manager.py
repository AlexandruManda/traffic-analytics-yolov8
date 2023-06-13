import pytube

class DownloadManager:
    @staticmethod
    def download_youtube_video(url, output_path):
        try:
            youtube = pytube.YouTube(url)
            video = youtube.streams.get_highest_resolution()
            video.download(output_path=output_path)

            return video.default_filename
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return None