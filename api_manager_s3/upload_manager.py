from datetime import datetime
import random, string
from hashlib import sha1
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated



class UploadManager:
    permission_classes = (IsAuthenticated,)

    def upload_file(self, extension, data):
        uploaded_name = self.random_text() + '.' + extension
        try:
            default_storage.save('tmp/' + uploaded_name, ContentFile(data.read()))
            return uploaded_name
        except ValueError:
            return False

    def random_text(self):
        letters = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        numbers = ''.join(random.choice(string.digits) for i in range(5))
        return sha1((letters + numbers).encode()).hexdigest()
