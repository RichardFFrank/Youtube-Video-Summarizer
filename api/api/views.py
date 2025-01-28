from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from api.models import validate_youtube_url
from youtube_video_summarizer.summarize import summarize
from .models import YouTubeModel, YouTubeModelSerializer
import json


class YouTubeModelView(APIView):
    renderer_classes = [JSONRenderer]  # Disable the browsable API

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            yt_url = data.get("yt_url")
            if not yt_url:
                return JsonResponse(
                    {"error": "Missing 'yt_url' parameter."}, status=400
                )

            # Validate the YouTube URL
            try:
                validate_youtube_url(yt_url)
            except ValidationError as e:
                return JsonResponse({"error": str(e)}, status=400)

            summary = summarize(yt_url)
            return JsonResponse(
                {"message": "Summary Created Successfully.", "summary": summary},
                status=200,
            )
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    def get(self, request, *args, **kwargs):
        return Response(
            """
            <b>This is a headless application, no root page has been configured.</b>
            <br>
            <br>
            To summarize a video, send a post request to this address with a yt_url parameter containing a url to the desired video.
            <br>
            <br>
            Example:\n
                <br>
                <br>
                curl -X POST http://127.0.0.1:8000/validate-yt-url/ \
                <br>
                -H "Content-Type: application/json" \
                <br>
                -d '{"yt_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
        """
        )


# # Create your views here.
# def index(request: HttpRequest):
#     return HttpResponse(
#         """
#             <b>This is a headless application, no root page has been configured.</b>
#             <br>
#             <br>
#             To summarize a video, send a post request to this address with a yt_url parameter containing a url to the desired video.
#             <br>
#             <br>
#             Example:\n
#                 <br>
#                 <br>
#                 curl -X POST http://127.0.0.1:8000/validate-yt-url/ \
#                 <br>
#                 -H "Content-Type: application/json" \
#                 <br>
#                 -d '{"yt_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
#         """
#     )


# @csrf_exempt  # Simplifying CSRF by disabling for now.
# def summarize(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             yt_url = data.get("yt_url")
#             if not yt_url:
#                 return JsonResponse(
#                     {"error": "Missing 'yt_url' parameter."}, status=400
#                 )

#             # Validate the YouTube URL
#             try:
#                 validate_youtube_url(yt_url)
#             except ValidationError as e:
#                 return JsonResponse({"error": str(e)}, status=400)

#             summary = summarize(yt_url)

#             return JsonResponse(
#                 {"message": "Summary Created Successfully.", "summary": summary},
#                 status=200,
#             )
#         except ValidationError as e:
#             return JsonResponse({"error": str(e)}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON payload."}, status=400)
#     return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
