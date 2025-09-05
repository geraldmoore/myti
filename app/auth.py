import os
from boto3 import Session
from .settings import get_settings


def init_aws_session(
    profile_name: str | None = None,
    region_name: str | None = None,
) -> Session:
    """
    Initialize AWS session and set environment variables for boto3/other tools.
    """
    if not profile_name and not region_name:
        settings = get_settings()
        profile_name = settings.aws_profile
        region_name = settings.aws_region

    session = Session(profile_name=profile_name, region_name=region_name)
    credentials = session.get_credentials().get_frozen_credentials()

    os.environ["AWS_PROFILE"] = profile_name
    os.environ["AWS_ACCESS_KEY_ID"] = credentials.access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key
    if credentials.token:
        os.environ["AWS_SESSION_TOKEN"] = credentials.token
    os.environ["AWS_DEFAULT_REGION"] = region_name

    return session


def get_s3_client(session: Session | None = None):
    """Return an S3 client from session (or default session)."""
    if session is None:
        session = Session()
    return session.client("s3")
