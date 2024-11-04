from fastapi import APIRouter, HTTPException
import boto3
from app.config import Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

router = APIRouter(prefix="/aws", tags=["AWS"])

s3_client = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION,
)


@router.get("/get-s3-object")
async def get_s3_object(bucket_name: str, object_key: str):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
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


@router.get("/list-s3-objects")
async def list_s3_objects(bucket_name: str):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" not in response:
            return {"message": "No objects found in bucket"}

        object_keys = [obj["Key"] for obj in response["Contents"]]
        return {"object_keys": object_keys}

    except s3_client.exceptions.NoSuchBucket:
        raise HTTPException(status_code=404, detail="Bucket not found")
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="AWS credentials not found")
    except PartialCredentialsError:
        raise HTTPException(status_code=403, detail="Incomplete AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
