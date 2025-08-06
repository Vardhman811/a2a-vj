import os
import logging
from google.cloud import storage, bigquery, pubsub_v1, metastore_v1
from google.cloud import artifactregistry_v1
from google.api_core.exceptions import GoogleAPICallError
from google.protobuf import field_mask_pb2

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the labels map to check (excluding project_id)
LABELS_MAP = {
    'abc': 'fruit',
    'def': '123',
    'ghi': 'vegetable'
}

# Define the list of locations to check
LOCATIONS = ["us-central1", "us-east1", "us-west1"]  # Add more locations as needed

def check_storage_labels(project_id):
    """Check and add all required labels to Cloud Storage buckets"""
    storage_client = storage.Client(project=project_id)
    try:
        buckets = storage_client.list_buckets()
        for bucket in buckets:
            labels = bucket.labels or {}
            modified = False

            for key, value in LABELS_MAP.items():
                if labels.get(key) != value:
                    labels[key] = value
                    modified = True

            labels['project_id'] = project_id

            if modified:
                bucket.labels = labels
                bucket.patch()
                logging.info(f"[GCS] Added labels to bucket '{bucket.name}': {labels}")
    except GoogleAPICallError as e:
        logging.error(f"[GCS] Error: {e}")

def check_bigquery_labels(project_id):
    """Check and add all required labels to BigQuery datasets"""
    bq_client = bigquery.Client(project=project_id)
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

            labels['project_id'] = project_id

            if modified:
                dataset.labels = labels
                bq_client.update_dataset(dataset, ["labels"])
                logging.info(f"[BigQuery] Added labels to dataset '{dataset.dataset_id}': {labels}")
    except GoogleAPICallError as e:
        logging.error(f"[BigQuery] Error: {e}")

def check_artifact_labels(project_id):
    """Check and add all required labels to Artifact Registry repositories"""
    artifact_client = artifactregistry_v1.ArtifactRegistryClient()
    try:
        for location in LOCATIONS:
            parent = f"projects/{project_id}/locations/{location}"
            repos = artifact_client.list_repositories(parent=parent)
            for repo in repos:
                labels = repo.labels or {}
                modified = False

                for key, value in LABELS_MAP.items():
                    if labels.get(key) != value:
                        labels[key] = value
                        modified = True

                labels['project_id'] = project_id

                if modified:
                    repo.labels = labels
                    artifact_client.update_repository(
                        repository=repo,
                        update_mask={"paths": ["labels"]}
                    )
                    logging.info(f"[Artifact] Added labels to repo '{repo.name.split('/')[-1]}': {labels}")
    except GoogleAPICallError as e:
        logging.error(f"[Artifact] Error: {e}")

def check_dataproc_metastore_labels(project_id):
    """Check and add all required labels to Dataproc Metastore services"""
    client = metastore_v1.DataprocMetastoreClient()
    try:
        for location in LOCATIONS:
            parent = f"projects/{project_id}/locations/{location}"
            services = client.list_services(parent=parent)
            for service in services:
                labels = service.labels or {}
                modified = False

                for key, value in LABELS_MAP.items():
                    if labels.get(key) != value:
                        labels[key] = value
                        modified = True

                labels['project_id'] = project_id

                if modified:
                    service.labels = labels
                    update_mask = field_mask_pb2.FieldMask(paths=["labels"])
                    client.update_service(service=service, update_mask=update_mask)
                    logging.info(f"[Metastore] Added labels to service '{service.name.split('/')[-1]}': {labels}")
    except GoogleAPICallError as e:
        logging.error(f"[Metastore] Error: {e}")

def check_pubsub_labels(project_id):
    """Check and add all required labels to Pub/Sub subscriptions"""
    subscriber = pubsub_v1.SubscriberClient()
    try:
        project_path = f"projects/{project_id}"
        subs = subscriber.list_subscriptions(request={"project": project_path})
        for sub in subs:
            labels = sub.labels or {}
            modified = False

            for key, value in LABELS_MAP.items():
                if labels.get(key) != value:
                    labels[key] = value
                    modified = True

            labels['project_id'] = project_id

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
    # ✅ List of project IDs to process
    project_ids = [
        'apps-aa218',
        'adk-short-bot-465311',
    ]

    for project_id in project_ids:
        try:
            logging.info(f"\n🔧 Starting label checks for project: {project_id}")

            logging.info("\n=== Processing Cloud Storage ===")
            check_storage_labels(project_id)

            logging.info("\n=== Processing BigQuery ===")
            check_bigquery_labels(project_id)

            logging.info("\n=== Processing Artifact Registry ===")
            check_artifact_labels(project_id)

            logging.info("\n=== Processing Dataproc Metastore ===")
            check_dataproc_metastore_labels(project_id)

            logging.info("\n=== Processing Pub/Sub ===")
            check_pubsub_labels(project_id)

            logging.info(f"\n✅ Label check complete for project: {project_id}\n{'=' * 50}")
        except Exception as e:
            logging.error(f"❌ Error processing project {project_id}: {e}")
