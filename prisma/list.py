import logging
from google.cloud import storage, bigquery, pubsub_v1, metastore_v1
from google.cloud import artifactregistry_v1
from google.api_core.exceptions import GoogleAPICallError

# Configure logging
logging.basicConfig(level=logging.INFO)

# Required labels
LABELS_MAP = {
    'apple': 'fruit',
    'mango': '123',
    'potato': 'vegetable'
}

# Locations for Artifact Registry & Metastore
LOCATIONS = ["us-central1", "us-east1"]


def check_storage_labels(project_id):
    print("\n=== Buckets ===")
    try:
        client = storage.Client(project=project_id)
        buckets = list(client.list_buckets(project=project_id))
        found = False
        for bucket in buckets:
            labels = bucket.labels or {}
            missing = [k for k, v in LABELS_MAP.items() if labels.get(k) != v]
            if missing:
                found = True
                print(f"{bucket.name} - Missing labels: {missing}")
        if not found:
            print("All buckets have required labels.")
    except GoogleAPICallError as e:
        print(f"[Error] GCS - {e}")


def check_bigquery_labels(project_id):
    print("\n=== BigQuery Datasets ===")
    try:
        client = bigquery.Client(project=project_id)
        datasets = list(client.list_datasets())
        found = False
        for dataset_ref in datasets:
            dataset = client.get_dataset(dataset_ref.dataset_id)
            labels = dataset.labels or {}
            missing = [k for k, v in LABELS_MAP.items() if labels.get(k) != v]
            if missing:
                found = True
                print(f"{dataset.dataset_id} - Missing labels: {missing}")
        if not found:
            print("All datasets have required labels.")
    except GoogleAPICallError as e:
        print(f"[Error] BigQuery - {e}")


def check_artifact_labels(project_id):
    print("\n=== Artifact Registry Repos ===")
    client = artifactregistry_v1.ArtifactRegistryClient()
    try:
        found = False
        for location in LOCATIONS:
            parent = f"projects/{project_id}/locations/{location}"
            repos = client.list_repositories(parent=parent)
            for repo in repos:
                labels = repo.labels or {}
                missing = [k for k, v in LABELS_MAP.items() if labels.get(k) != v]
                if missing:
                    found = True
                    name = repo.name.split("/")[-1]
                    print(f"{name} - Missing labels: {missing}")
        if not found:
            print("All repos have required labels.")
    except GoogleAPICallError as e:
        print(f"[Error] Artifact - {e}")


def check_dataproc_metastore_labels(project_id):
    print("\n=== Dataproc Metastore Services ===")
    client = metastore_v1.DataprocMetastoreClient()
    try:
        found = False
        for location in LOCATIONS:
            parent = f"projects/{project_id}/locations/{location}"
            services = client.list_services(parent=parent)
            for service in services:
                labels = service.labels or {}
                missing = [k for k, v in LABELS_MAP.items() if labels.get(k) != v]
                if missing:
                    found = True
                    name = service.name.split("/")[-1]
                    print(f"{name} - Missing labels: {missing}")
        if not found:
            print("All metastore services have required labels.")
    except GoogleAPICallError as e:
        print(f"[Error] Metastore - {e}")


def check_pubsub_labels(project_id):
    print("\n=== Pub/Sub Subscriptions ===")
    client = pubsub_v1.SubscriberClient()
    try:
        project_path = f"projects/{project_id}"
        subs = client.list_subscriptions(request={"project": project_path})
        found = False
        for sub in subs:
            labels = sub.labels or {}
            missing = [k for k, v in LABELS_MAP.items() if labels.get(k) != v]
            if missing:
                found = True
                name = sub.name.split("/")[-1]
                print(f"{name} - Missing labels: {missing}")
        if not found:
            print("All subscriptions have required labels.")
    except GoogleAPICallError as e:
        print(f"[Error] Pub/Sub - {e}")


if __name__ == "__main__":
    # ✅ List of projects to scan
    PROJECT_IDS = [
        'adk-short-bot-465311',
        'apps-aa218',
    ]

    for project_id in PROJECT_IDS:
        print("\n" + "=" * 60)
        print(f"🔍 Checking project: {project_id}")
        print("=" * 60)

        check_storage_labels(project_id)
        check_bigquery_labels(project_id)
        check_artifact_labels(project_id)
        check_dataproc_metastore_labels(project_id)
        check_pubsub_labels(project_id)

        print("\n✅ Completed check for:", project_id)
