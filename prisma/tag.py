import os
import logging
from google.cloud import storage, bigquery, pubsub_v1, metastore_v1
from google.cloud import artifactregistry_v1
from google.api_core.exceptions import GoogleAPICallError
from google.protobuf import field_mask_pb2

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the labels map to check
LABELS_MAP = {
    'app': 'gcp',
    'id': '123',
    'user': 'abc',
    'project_id': 'adk-short-bot-465311'
}

def check_storage_labels():
    """Check and add all required labels to Cloud Storage buckets"""
    storage_client = storage.Client()
    try:
        buckets = storage_client.list_buckets()
        for bucket in buckets:
            labels = bucket.labels or {}
            modified = False
            
            for key, value in LABELS_MAP.items():
                if labels.get(key) != value:
                    labels[key] = value
                    modified = True
            
            if modified:
                bucket.labels = labels
                bucket.patch()
                logging.info(f"[GCS] Added labels to bucket '{bucket.name}': {labels}")
    except GoogleAPICallError as e:
        logging.error(f"[GCS] Error: {e}")

def check_bigquery_labels():
    """Check and add all required labels to BigQuery datasets"""
    bq_client = bigquery.Client(project=LABELS_MAP['project_id'])
    try:
        datasets = list(bq_client.list_datasets())
        for dataset_ref in datasets:
            dataset = bq_client.get_dataset(dataset_ref.dataset_id)
            labels = dataset.labels or {}
            modified = False
            
            for key, value in LABELS_MAP.items():
                if labels.get(key) != value:
                    labels[key] = value
                    modified = True
            
            if modified:
                dataset.labels = labels
                bq_client.update_dataset(dataset, ["labels"])
                logging.info(f"[BigQuery] Added labels to dataset '{dataset.dataset_id}': {labels}")
    except GoogleAPICallError as e:
        logging.error(f"[BigQuery] Error: {e}")

def check_artifact_labels(location="us-central1"):
    """Check and add all required labels to Artifact Registry repositories"""
    artifact_client = artifactregistry_v1.ArtifactRegistryClient()
    try:
        parent = f"projects/{LABELS_MAP['project_id']}/locations/{location}"
        repos = artifact_client.list_repositories(parent=parent)
        for repo in repos:
            labels = repo.labels or {}
            modified = False
            
            for key, value in LABELS_MAP.items():
                if labels.get(key) != value:
                    labels[key] = value
                    modified = True
            
            if modified:
                repo.labels = labels
                artifact_client.update_repository(
                    repository=repo,
                    update_mask={"paths": ["labels"]}
                )
                logging.info(f"[Artifact] Added labels to repo '{repo.name.split('/')[-1]}': {labels}")
    except GoogleAPICallError as e:
        logging.error(f"[Artifact] Error: {e}")

def check_dataproc_metastore_labels(location="us-central1"):
    """Check and add all required labels to Dataproc Metastore services"""
    client = metastore_v1.DataprocMetastoreClient()
    try:
        parent = f"projects/{LABELS_MAP['project_id']}/locations/{location}"
        services = client.list_services(parent=parent)
        for service in services:
            labels = service.labels or {}
            modified = False
            
            for key, value in LABELS_MAP.items():
                if labels.get(key) != value:
                    labels[key] = value
                    modified = True
            
            if modified:
                service.labels = labels
                update_mask = field_mask_pb2.FieldMask(paths=["labels"])
                client.update_service(service=service, update_mask=update_mask)
                logging.info(f"[Metastore] Added labels to service '{service.name.split('/')[-1]}': {labels}")
    except GoogleAPICallError as e:
        logging.error(f"[Metastore] Error: {e}")

def check_pubsub_labels():
    """Check and add all required labels to Pub/Sub subscriptions"""
    subscriber = pubsub_v1.SubscriberClient()
    try:
        project_path = f"projects/{LABELS_MAP['project_id']}"
        subs = subscriber.list_subscriptions(request={"project": project_path})
        for sub in subs:
            labels = sub.labels or {}
            modified = False
            
            for key, value in LABELS_MAP.items():
                if labels.get(key) != value:
                    labels[key] = value
                    modified = True
            
            if modified:
                sub.labels = labels
                update_mask = field_mask_pb2.FieldMask(paths=["labels"])
                subscriber.update_subscription(
                    subscription={"name": sub.name, "labels": labels},
                    update_mask=update_mask
                )
                logging.info(f"[PubSub] Added labels to sub '{sub.name.split('/')[-1]}': {labels}")
    except GoogleAPICallError as e:
        logging.error(f"[PubSub] Error: {e}")

if __name__ == "__main__":
    LOCATION = os.getenv("LOCATION", "us-central1")  # Default region
    
    logging.info("\n=== Processing Cloud Storage ===")
    check_storage_labels()
    
    logging.info("\n=== Processing BigQuery ===")
    check_bigquery_labels()
    
    logging.info("\n=== Processing Artifact Registry ===")
    check_artifact_labels(LOCATION)
    
    logging.info("\n=== Processing Dataproc Metastore ===")
    check_dataproc_metastore_labels(LOCATION)
    
    logging.info("\n=== Processing Pub/Sub ===")
    check_pubsub_labels()
    
    logging.info("\nLabel check complete for all services!")
