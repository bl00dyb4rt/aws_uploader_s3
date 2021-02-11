from django.urls import path
from api_manager_s3 import views, manager_bucket_api

urlpatterns = [
    path('api/v1/upload_image', manager_bucket_api.ManageBucketAPI.upload_images),
    path('api/v1/list_all_images', manager_bucket_api.ManageBucketAPI.list_all_images),
]
