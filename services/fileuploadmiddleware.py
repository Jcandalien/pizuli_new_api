from fastapi import UploadFile, File
from starlette.middleware.base import BaseHTTPMiddleware
import aiofiles
import os

class FileUploadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method == "POST" and "multipart/form-data" in request.headers.get("Content-Type", ""):
            form = await request.form()
            for field_name, field_value in form.items():
                if isinstance(field_value, UploadFile):
                    file_path = await self.save_upload_file(field_value)
                    request.state.files = getattr(request.state, "files", {})
                    request.state.files[field_name] = file_path
        response = await call_next(request)
        return response

    async def save_upload_file(self, file: UploadFile) -> str:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
        return file_path