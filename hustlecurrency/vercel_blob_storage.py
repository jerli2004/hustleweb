# vercel_blob_storage.py
import os
from urllib.parse import urljoin
from django.core.files.storage import Storage
from django.core.files.base import File
from django.utils.deconstruct import deconstructible
from vercel_blob import put, del_, head
import io

@deconstructible
class VercelBlobStorage(Storage):
    def __init__(self, base_url=None):
        self.base_url = base_url or 'https://hustler-currency-website.vercel.app'

    def _open(self, name, mode='rb'):
        # For Vercel Blob, we need to handle files differently
        # Since Blob is HTTP-based, we'll return a file-like object
        if 'r' in mode:
            # For reading, we need to fetch from blob
            # This would require implementing a read method
            # For now, return a dummy file
            return io.BytesIO(b'')
        else:
            # For writing
            return VercelBlobFile(name, self)

    def _save(self, name, content):
        # Upload file to Vercel Blob
        try:
            # Read the file content
            content.seek(0)
            file_bytes = content.read()
            
            # Upload to Vercel Blob
            result = put(
                name,
                file_bytes,
                options={
                    'token': os.environ.get('BLOB_READ_WRITE_TOKEN'),
                    'contentType': self._get_content_type(name),
                }
            )
            
            # Return the blob URL
            return result.get('url', name)
        except Exception as e:
            print(f"Error uploading to Vercel Blob: {e}")
            # Fallback: save locally if in development
            if os.environ.get('VERCEL') != '1':
                local_path = os.path.join('media', name)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(file_bytes)
                return local_path
            raise

    def exists(self, name):
        # Check if file exists in Vercel Blob
        try:
            result = head(name, {'token': os.environ.get('BLOB_READ_WRITE_TOKEN')})
            return True
        except:
            return False

    def url(self, name):
        # Return full URL for the blob
        if name.startswith(('http://', 'https://')):
            return name
        return f"https://hustler-currency-website.vercel.app/{name}"

    def delete(self, name):
        # Delete from Vercel Blob
        try:
            del_(name, {'token': os.environ.get('BLOB_READ_WRITE_TOKEN')})
        except Exception as e:
            print(f"Error deleting from Vercel Blob: {e}")

    def _get_content_type(self, filename):
        # Map file extensions to content types
        ext = os.path.splitext(filename)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
        }
        return content_types.get(ext, 'application/octet-stream')


class VercelBlobFile(File):
    def __init__(self, name, storage):
        self.name = name
        self.storage = storage
        self._file = None
        self._is_dirty = False

    def write(self, content):
        if self._file is None:
            self._file = io.BytesIO()
        self._file.write(content)
        self._is_dirty = True

    def close(self):
        if self._is_dirty and self._file:
            self._file.seek(0)
            self.storage._save(self.name, self._file)
        if self._file:
            self._file.close()