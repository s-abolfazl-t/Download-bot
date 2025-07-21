import instaloader
import os

def download_instagram(url):
    loader = instaloader.Instaloader(dirname_pattern="downloads", save_metadata=False)
    shortcode = url.strip("/").split("/")[-1]
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    loader.download_post(post, target=shortcode)
    folder = f"downloads/{shortcode}"
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith((".mp4", ".jpg", ".jpeg"))]
