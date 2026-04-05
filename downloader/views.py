from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from pytubefix import YouTube, Playlist
from pytubefix.exceptions import VideoUnavailable, RegexMatchError


def get_client_ip(request):
    """
    Returns the IP of the request, accounting for the possibility of being behind a proxy.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@ensure_csrf_cookie
def home(request):
    print(f"someone is opening the link from {get_client_ip(request)}")
    return render(request, "home.html")


def show_download_options(request):

    def is_valid_youtube_video_link(link: str) -> bool:
        try:
            yt = YouTube(link , client="WEB")
            _ = yt.title
            return True
        except (VideoUnavailable, RegexMatchError, Exception):
            return False

    link = request.POST.get("link")

    if not link:
        return JsonResponse({"type": "error", "message": "No link provided"}, status=400)

    try:
        if is_valid_youtube_video_link(link):
            print("video detected")
            lv = []
            lresolutions = []
            yt = YouTube(link , client="WEB")
            resolutionsvid = yt.streams.order_by('resolution').filter(mime_type='video/mp4')
            audio_tracks = yt.streams.get_default_audio_track()

            for j in resolutionsvid:
                if j.is_progressive:
                    lv.append(j)
                    lresolutions.append(j.resolution)
                elif "av01" in j.video_codec:
                    if j.resolution not in lresolutions:
                        lv.append(j)

            # Serialize video streams to plain dicts
            video_options = []
            for stream in lv:
                video_options.append({
                    "resolution": stream.resolution,
                    "url": stream.url,
                    "is_progressive": stream.is_progressive,
                    "filesize": stream.filesize,
                })

            # Serialize audio streams to plain dicts
            audio_options = []
            if audio_tracks:
                try:
                    for stream in audio_tracks:
                        audio_options.append({
                            "abr": stream.abr,
                            "url": stream.url,
                            "filesize": stream.filesize,
                        })
                except TypeError:
                    # Single stream object, not iterable
                    audio_options.append({
                        "abr": audio_tracks.abr,
                        "url": audio_tracks.url,
                        "filesize": audio_tracks.filesize,
                    })

            return JsonResponse({
                "type": "video",
                "title": yt.title,
                "thumbnail": yt.thumbnail_url,
                "resolutions": video_options,
                "audio": audio_options,
            })

        elif "playlist" in link:
            print("playlist detected")
            vids = []
            length = 0
            p = Playlist(link)
            for vid in p.videos:
                vids.append({
                    "title": vid.title,
                    "watch_url": vid.watch_url,
                    "thumbnail": vid.thumbnail_url,
                    "length": vid.length,
                })
                length += int(vid.length)
            length = length // 60

            return JsonResponse({
                "type": "playlist",
                "title": p.title if hasattr(p, 'title') else "Playlist",
                "length": length,
                "videos": vids,
            })
        else:
            return JsonResponse({"type": "error", "message": "Invalid link"}, status=400)

    except Exception as e:
        print(f"Error processing link: {e}")
        return JsonResponse({"type": "error", "message": "Failed to process the link. Please try again."}, status=500)


def download(request):
    stream = request.POST.get("stream")
    return redirect(stream.url)