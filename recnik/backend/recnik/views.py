import mimetypes
from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def serve_media_file(request, file_path):
    absolute_path = f'{settings.MEDIA_ROOT}/{file_path}'
    content_type, encoding = mimetypes.guess_type(absolute_path)
    response = FileResponse(open(absolute_path, 'rb'), as_attachment=True, content_type=content_type)
    return response
