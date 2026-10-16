"""Copy existing BlogBoard objects from Backblaze B2 to Supabase Storage."""

import argparse
from typing import Any

import boto3
from blogboard.config.settings import app_settings


def _client(endpoint: str, region: str, access_key: str, secret_key: str):
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="List objects without copying them")
    args = parser.parse_args()

    b2 = app_settings.b2
    supabase = app_settings.supabase
    required = {
        "b2__endpoint": b2.ENDPOINT,
        "b2__bucket_name": b2.BUCKET_NAME,
        "b2__application_key_id": b2.APPLICATION_KEY_ID,
        "b2__application_key": b2.APPLICATION_KEY,
        "supabase__s3_endpoint": supabase.S3_ENDPOINT,
        "supabase__bucket_name": supabase.BUCKET_NAME,
        "supabase__access_key_id": supabase.ACCESS_KEY_ID,
        "supabase__secret_access_key": supabase.SECRET_ACCESS_KEY,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise RuntimeError("Missing migration settings: " + ", ".join(missing))

    source = _client(
        b2.ENDPOINT, b2.REGION, b2.APPLICATION_KEY_ID, b2.APPLICATION_KEY
    )
    destination = _client(
        supabase.S3_ENDPOINT,
        supabase.REGION,
        supabase.ACCESS_KEY_ID,
        supabase.SECRET_ACCESS_KEY,
    )

    copied = 0
    for page in source.get_paginator("list_objects_v2").paginate(Bucket=b2.BUCKET_NAME):
        for item in page.get("Contents", []):
            key = item["Key"]
            print(f"{'Would copy' if args.dry_run else 'Copying'} {key}")
            if args.dry_run:
                continue

            response: dict[str, Any] = source.get_object(Bucket=b2.BUCKET_NAME, Key=key)
            destination.put_object(
                Bucket=supabase.BUCKET_NAME,
                Key=key,
                Body=response["Body"].read(),
                ContentType=response.get("ContentType", "application/octet-stream"),
            )
            copied += 1

    print(f"{'Objects found' if args.dry_run else 'Objects copied'}: {copied}")


if __name__ == "__main__":
    main()
