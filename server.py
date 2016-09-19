from bottle import route, run, template, static_file
from visualize_youtube import url_to_img

@route('/youtube/<video_id>')
def index(video_id):
    url = "https://www.youtube.com/watch?v={}".format(video_id)
    url_to_img(url, "audio.mp3", "image.png")
    return static_file('image.png', root = "/home/carlos/projects/music_visualization")

run(host='localhost', port=8080)