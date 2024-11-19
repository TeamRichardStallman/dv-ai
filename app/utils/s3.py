from typing import Dict, List

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import HTTPException

from app.core.config import Config

s3_client = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION,
)


async def get_s3_object(object_key: str):
    try:
        response = s3_client.get_object(Bucket=Config.S3_BUCKET_NAME, Key=object_key)
        data = response["Body"].read().decode("utf-8")

        return {"data": data}

    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Object not found")
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="AWS credentials not found")
    except PartialCredentialsError:
        raise HTTPException(status_code=403, detail="Incomplete AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_files_from_s3(file_objects: List[Dict[str, str]]):
    s3_files = []

    for file_object in file_objects:
        path = file_object["path"]
        file_data = await get_s3_object(path)
        file_type = file_object["type"]

        s3_files.append({"type": file_type, "data": file_data})

    return s3_files
