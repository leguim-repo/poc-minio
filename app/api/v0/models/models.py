from typing import List, Union

from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: str
    processed_files: List[str]


class S3Object(BaseModel):
    key: str
    size: int = 0
    eTag: str = ""
    contentType: str = ""


class S3Bucket(BaseModel):
    name: str
    arn: str = ""


class S3Info(BaseModel):
    bucket: S3Bucket
    object: S3Object


class Record(BaseModel):
    eventName: str
    s3: S3Info


class WebhookRequest(BaseModel):
    Records: List[Record]


class WebhookResponse(BaseModel):
    status: str
    error: Union[str, None] = None
