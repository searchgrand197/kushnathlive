import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404


def _resolve_build_path(relative_path=""):
    build_dir = Path(settings.FRONTEND_BUILD_DIR).resolve()
    file_path = (build_dir / relative_path).resolve()

    if file_path != build_dir and build_dir not in file_path.parents:
        raise Http404()

    return file_path


def serve_frontend(request, path=""):
    if path:
        file_path = _resolve_build_path(path)
        if file_path.is_file():
            content_type, _ = mimetypes.guess_type(str(file_path))
            response = FileResponse(
                open(file_path, "rb"),
                content_type=content_type or "application/octet-stream",
            )
            if file_path.suffix == ".html":
                response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            elif file_path.suffix in {".js", ".css"}:
                response["Cache-Control"] = "public, max-age=31536000, immutable"
            return response

    index_path = _resolve_build_path("index.html")
    if not index_path.is_file():
        raise Http404(
            "Frontend build not found. Run 'npm run build' in the front/ directory."
        )

    response = FileResponse(open(index_path, "rb"), content_type="text/html")
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response
