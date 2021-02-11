from boto3.exceptions import S3UploadFailedError
from botocore import exceptions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_manager_s3.serializers import ImagesSerializer, ImagePostSerializer
import boto3
from django.conf import settings

from .custom_response import CustomResponse
from .upload_manager import UploadManager
from .models import Images
import logging

logger = logging.getLogger(__name__)


class ManageBucketAPI:

    @staticmethod
    @api_view(['POST'])
    def upload_images(request):
        if request.method == 'POST':
            data = request.data

            serializer = ImagePostSerializer(data=data)
            if serializer.is_valid():
                file = data['file']
                original_name = file.name
                content_type = file.content_type
                extension = str(content_type).split('/')[1]
                uploaded_name = UploadManager().upload_file(extension, file)
                if uploaded_name:
                    try:
                        s3 = boto3.resource('s3')
                        file = 'tmp/' + uploaded_name
                        bucket_name = settings.BUCKET_NAME
                        s3.meta.client.upload_file(file, bucket_name, uploaded_name,
                                                   ExtraArgs={'ACL': 'public-read',
                                                              'ContentType': content_type})
                        location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
                        url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket_name, location, uploaded_name)
                        data = {
                            'name': original_name,
                            'full_path': url,
                            'hash_name': uploaded_name
                        }
                        serializer_image = ImagesSerializer(data=data)
                        if serializer_image.is_valid():
                            try:
                                save_image = Images().save_image(name=original_name, full_path=url,
                                                                 hash_name=uploaded_name)
                                logger.warning(save_image.__dict__)
                                response = CustomResponse.response(
                                    data={
                                        "image_url": url
                                    },
                                    message="Proceso completado con éxito")
                                return Response(response, status=status.HTTP_200_OK)

                            except Exception as e:
                                logger.error('Invalid save')
                                logger.error(e)
                        else:
                            logger.error(serializer_image.errors)
                            response = CustomResponse.response(status='error',
                                                               data=400,
                                                               message="Bad Request")
                            return Response(response, status=status.HTTP_200_OK)

                    except S3UploadFailedError as e:
                        logger.error(e)
                        response = CustomResponse.response(status='error',
                                                           data=403,
                                                           message="Error al subir la imagen")
                        return Response(response, status=status.HTTP_403_FORBIDDEN)

                    except exceptions.ClientError as e:
                        logger.error(e)
                        response = CustomResponse.response(status='error',
                                                           data=403,
                                                           message="Error de permisos")
                        return Response(response, status=status.HTTP_403_FORBIDDEN)
                    except Exception as e:
                        logger.error(e)
                        response = CustomResponse.response(status='error',
                                                           data=403,
                                                           message="Contacte a un administradorr")
                        return Response(response, status=status.HTTP_403_FORBIDDEN)
            else:
                logger.error('Invalid Image')
                logger.error(serializer.errors)
                response = CustomResponse.response(status='error',
                                                   data=400,
                                                   message="Bad Request")
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['GET', 'POST'])
    def list_all_images(request):
        if request.method == 'GET':
            s3 = boto3.resource('s3')
            bucket_name = settings.BUCKET_NAME
            my_bucket = s3.Bucket(bucket_name)
            location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
            for file in my_bucket.objects.all():
                url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket_name, location, file.key)
        return Response()
