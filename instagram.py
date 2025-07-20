# instagram.py
import os
import instaloader

def download_instagram_post(url):
    loader = instaloader.Instaloader(dirname_pattern="downloads", save_metadata=False)
    shortcode = url.strip("/").split("/")[-1]
    loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target=shortcode)
    return f"downloads/{shortcode}"
