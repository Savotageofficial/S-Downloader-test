from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from pytubefix import YouTube, Playlist
from pytubefix.exceptions import VideoUnavailable, RegexMatchError


# Create your views here.

def get_client_ip(request):
    """
    Returns the IP of the request, accounting for the possibility of being behind a proxy.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # The first IP in the list is typically the original client IP.
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):

    # file = open("D:\S-Downloader-test\me-as-an-emperor.png" , "rb")


    # return FileResponse(file , as_attachment=True, filename="me-as-an-emperor.png")
    print(f"someone is opening the link from{get_client_ip(request)}")
    return render(request, "home.html")



def show_download_options(request):


    def is_valid_youtube_video_link(link: str) -> bool:
        try:
            yt = YouTube(link)
            # Force fetch to confirm the video exists
            _ = yt.title

            return True
        except (VideoUnavailable, RegexMatchError, Exception):
            return False



    # resolutions = ["1080p" , "720p" , "480p" , "360p" , "240p"]
    link = request.POST.get("link")

    if is_valid_youtube_video_link(link):
        print("video detected")
        lv = []
        lresolutions = []
        yt = YouTube(link)
        resolutionsvid = yt.streams.order_by('resolution').filter(mime_type='video/mp4')
        audio_types = yt.streams.get_default_audio_track()
        print(audio_types)
        print(resolutionsvid)
        for j in resolutionsvid:
            if (j.is_progressive == True):
                lv.append(j)
                lresolutions.append(j.resolution)
            elif ("av01" in j.video_codec):
                if (j.resolution not in lresolutions):
                    lv.append(j)

        return render(request, "download_options.html" , {"resolutions": lv, "title" : yt.title , "audios": audio_types})
    elif "playlist" in link:
        print("playlist detected")
        vids = []
        length = 0
        p = Playlist(link)
        for vid in p.videos:
            vids.append(vid)
            length += int(vid.length)
        length = length // 60
        return render(request , "playlist_download.html", {"vids": vids , "length": length})
    else:
        return HttpResponse("Invalid link brother.....")



def download(request):

    stream = request.POST.get("stream")
    # yt = YouTube(link)
    # vid_title = yt.title
    # vid_stream = yt.streams.get_highest_resolution(progressive=True)
    # return render(request, "download_options.html" , {"vid_title": vid_title})
    return redirect(stream.url)