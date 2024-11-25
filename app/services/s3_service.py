from typing import Dict, List, Union

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import HTTPException, UploadFile

from app.core.config import Config


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION,
        )

    async def get_s3_object(self, object_key: str) -> Union[bytes, str]:
        try:
            response = self.s3_client.get_object(Bucket=Config.S3_BUCKET_NAME, Key=object_key)
            content_type = response.get("ContentType", "")

            if content_type not in [
                "audio/flac",
                "audio/m4a",
                "audio/mp3",
                "audio/wav",
                "audio/ogg",
                "audio/webm",
                "audio/mpeg",
            ]:
                raise HTTPException(status_code=400, detail=f"Unsupported audio format: {content_type}")

            if "text" in content_type or "json" in content_type:
                return response["Body"].read().decode("utf-8")
            else:
                return response["Body"].read()

        except self.s3_client.exceptions.NoSuchKey:
            raise HTTPException(status_code=404, detail="Object not found")
        except NoCredentialsError:
            raise HTTPException(status_code=403, detail="AWS credentials not found")
        except PartialCredentialsError:
            raise HTTPException(status_code=403, detail="Incomplete AWS credentials")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_files_from_s3(self, file_objects: List[Dict[str, str]]) -> List[Dict[str, str]]:
        s3_files = []

        for file_object in file_objects:
            path = file_object["path"]
            file_data = await self.get_s3_object(path)
            file_type = file_object["type"]

            s3_files.append({"type": file_type, "data": file_data})

        return s3_files

    async def upload_s3_object(self, object_key: str, file: UploadFile) -> str:
        try:
            self.s3_client.upload_fileobj(
                file.file,
                Config.S3_BUCKET_NAME,
                object_key,
                ExtraArgs={"ContentType": file.content_type},
            )
            return object_key

        except NoCredentialsError:
            raise HTTPException(status_code=403, detail="AWS credentials not found")
        except PartialCredentialsError:
            raise HTTPException(status_code=403, detail="Incomplete AWS credentials")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


def get_s3_service():
    return S3Service()
