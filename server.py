from flask import Flask
from queue import Queue


app = Flask(__name__)

url_queue = Queue()
ok_urls = []
with open("ok_urls.txt") as f:
    text = f.read()
    for url in text.strip().split("\n"):
        url = url.strip()
        ok_urls.append(url)

urls = []
with open("urls.txt") as f:
    text = f.read()

for url in text.strip().split("\n"):
    url = url.strip()
    if url in ok_urls:
        continue

    url_queue.put(url)


@app.route("/audio-info")
def get_audio_info():
    url = url_queue.get(block=False)
    with open("ok_urls.txt", "a") as f:
        f.write(url + "\n")

    return url


if __name__ == "__main__":
    app.run()

