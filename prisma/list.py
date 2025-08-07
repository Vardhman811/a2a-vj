import logging
from google.cloud import storage, bigquery, pubsub_v1, metastore_v1
from google.cloud import artifactregistry_v1
from google.api_core.exceptions import GoogleAPICallError

# Configure logging
logging.basicConfig(level=logging.INFO)

# Required labels to check
LABELS_MAP = {
    'one': 'fruit',
    'yes': '123',
    'no': 'vegetable'
}

# Locations for Artifact Registry and Dataproc Metastore
LOCATIONS = ["us-central1", "us-east1"]


def check_storage_labels(project_id, file):
    file.write("\n=== Buckets ===\n")
    try:
        client = storage.Client(project=project_id)
        buckets = list(client.list_buckets(project=project_id))
        found = False
        for bucket in buckets:
            labels = bucket.labels or {}
            missing = [k for k, v in LABELS_MAP.items() if labels.get(k) != v]
            if missing:
                found = True
                file.write(f"{bucket.name} - Missing labels: {missing}\n")
        if not found:
            file.write("All buckets have required labels.\n")
    except GoogleAPICallError as e:
        file.write(f"[Error] GCS - {e}\n")


def check_bigquery_labels(project_id, file):
    file.write("\n=== BigQuery Datasets ===\n")
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
                file.write(f"{dataset.dataset_id} - Missing labels: {missing}\n")
        if not found:
            file.write("All datasets have required labels.\n")
    except GoogleAPICallError as e:
        file.write(f"[Error] BigQuery - {e}\n")


def check_artifact_labels(project_id, file):
    file.write("\n=== Artifact Registry Repos ===\n")
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
                    file.write(f"{name} - Missing labels: {missing}\n")
        if not found:
            file.write("All repos have required labels.\n")
    except GoogleAPICallError as e:
        file.write(f"[Error] Artifact Registry - {e}\n")


def check_dataproc_metastore_labels(project_id, file):
    file.write("\n=== Dataproc Metastore Services ===\n")
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
                    file.write(f"{name} - Missing labels: {missing}\n")
        if not found:
            file.write("All metastore services have required labels.\n")
    except GoogleAPICallError as e:
        file.write(f"[Error] Metastore - {e}\n")


def check_pubsub_labels(project_id, file):
    file.write("\n=== Pub/Sub Subscriptions ===\n")
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
                file.write(f"{name} - Missing labels: {missing}\n")
        if not found:
            file.write("All subscriptions have required labels.\n")
    except GoogleAPICallError as e:
        file.write(f"[Error] Pub/Sub - {e}\n")


if __name__ == "__main__":
    # ✅ List of GCP projects to scan
    PROJECT_IDS = [
        'adk-short-bot-465311',
        'apps-aa218',
    ]

    # ✅ Output file path
    OUTPUT_FILE = "label_check_output.txt"

    # ✅ Write output to UTF-8 encoded file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for project_id in PROJECT_IDS:
            file.write("\n" + "=" * 60 + "\n")
            file.write(f"Checking project: {project_id}\n")
            file.write("=" * 60 + "\n")

            check_storage_labels(project_id, file)
            check_bigquery_labels(project_id, file)
            check_artifact_labels(project_id, file)
            check_dataproc_metastore_labels(project_id, file)
            check_pubsub_labels(project_id, file)

            file.write(f"\nCompleted check for: {project_id}\n")
