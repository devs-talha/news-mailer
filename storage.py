from minio import Minio
import mimetypes
from image import ImageItem
import io
import os

minio=None
def get_minio_client():
    global minio
    if minio is None:
        minio=Minio(
        endpoint=os.getenv('STORAGE_ENDPOINT'),
        access_key=os.getenv('STORAGE_ACCESS_KEY'),
        secret_key=os.getenv('STORAGE_SECRET_KEY'),
    )
    return minio

def upload_images(images: ImageItem):
    for image in images:
        image['url'] = upload_file(image)

def upload_file(image: ImageItem):
    client = get_minio_client()
    bucket_name = os.getenv('STORAGE_BUCKET')
    object_name = f"{os.getenv('STORAGE_PATH_PREFIX')}/{image['newspaper_name']}/{image['date']}/{image['name']}"
    # Upload the image file to MinIO
    client.put_object(
        bucket_name,
        object_name,
        data=io.BytesIO(image['data']),
        length=len(image['data']),
        content_type=mimetypes.guess_type(image['name'])[0]
    )
    url = client.presigned_get_object(bucket_name, object_name).split('?')[0]
    return url