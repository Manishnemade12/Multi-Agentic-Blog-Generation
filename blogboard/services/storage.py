import json
import boto3
from typing import Optional, List, Dict, Any
from botocore.exceptions import ClientError
from blogboard.config.settings import app_settings


class SupabaseStorageService:
    """S3-compatible storage service for Supabase Storage."""

    def __init__(self):
        settings = app_settings.b2
        endpoint = app_settings.S3_ENDPOINT
        self.bucket_name = settings.BUCKET_NAME.strip().strip(' ="')
        if not endpoint or not settings.APPLICATION_KEY_ID or not settings.APPLICATION_KEY:
            raise RuntimeError(
                "Supabase Storage is not configured. Set s3_endpoint, "
                "b2__application_key_id, and b2__application_key in .env."
            )
        self.client = boto3.client(
            service_name="s3",
            endpoint_url=endpoint,
            aws_access_key_id=settings.APPLICATION_KEY_ID,
            aws_secret_access_key=settings.APPLICATION_KEY,
            region_name=settings.REGION,
        )

    def get_object(self, key: str) -> Optional[str]:
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=key)
            return response["Body"].read().decode("utf-8")
        except ClientError as e:
            if e.response.get('Error', {}).get('Code') in {'NoSuchKey', '404', 'NotFound'}:
                return None
            print(f"[ERROR] Supabase Storage error in get_object ({key}): {e}")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected Supabase Storage error fetching {key}: {e}")
            return None

    def put_object(self, key: str, data: str, content_type: str = "text/plain") -> bool:
        try:
            self.client.put_object(Bucket=self.bucket_name, Key=key,
                                   Body=data.encode("utf-8"), ContentType=content_type)
            print(f"  Uploaded to Supabase Storage: {self.bucket_name}/{key}")
            return True
        except ClientError as e:
            print(f"[ERROR] Failed to upload {key} to Supabase Storage: {e}")
            return False

    def delete_object(self, key: str) -> bool:
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            print(f"[ERROR] Failed to delete {key} from Supabase Storage: {e}")
            return False

    def list_objects(self, prefix: str = "") -> List[Dict[str, Any]]:
        paginator = self.client.get_paginator("list_objects_v2")
        return [item for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)
                for item in page.get("Contents", [])]

    def presigned_url(self, key: str, operation: str = "get_object", expires_in: int = 3600) -> str:
        if operation not in {"get_object", "put_object"}:
            raise ValueError("operation must be 'get_object' or 'put_object'")
        return self.client.generate_presigned_url(
            operation, Params={"Bucket": self.bucket_name, "Key": key}, ExpiresIn=expires_in
        )

    def get_json(self, key: str) -> Optional[List[Dict[str, Any]]]:
        data = self.get_object(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                print(f"[WARN] Failed to decode JSON from {key}. Starting fresh.")
                return []
        return []

    def get_articles_json(self, domain: str) -> List[Dict[str, Any]]:
        return self.get_json(f"blogs/{domain}/articles.json") or []

    def save_articles_json(self, domain: str, articles: List[Dict[str, Any]]) -> bool:
        return self.put_object(f"blogs/{domain}/articles.json",
                               json.dumps(articles, indent=2, ensure_ascii=False),
                               content_type="application/json")

    def get_recent_history(self, domain: str, limit: int = 3) -> List[Dict[str, Any]]:
        articles = sorted(self.get_articles_json(domain),
                          key=lambda x: x.get("date", ""), reverse=True)[:limit]
        return [{"title": a.get("title"), "topic": a.get("topic"),
                 "subtopics": a.get("subtopics", "")} for a in articles]

    def get_all_domains_last_updated(self) -> Dict[str, str]:
        latest_dates = {}
        for domain_slug in app_settings.tags.model_dump().keys():
            articles = self.get_articles_json(domain_slug)
            if not articles:
                latest_dates[domain_slug] = "Never"
            else:
                latest_dates[domain_slug] = sorted(
                    articles, key=lambda x: x.get("date", ""), reverse=True
                )[0].get("date", "Unknown")
        return latest_dates


# Kept as a compatibility alias for integrations that imported the old name.
B2StorageService = SupabaseStorageService
