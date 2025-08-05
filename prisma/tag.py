from google.cloud import storage, bigquery, pubsub_v1, metastore_v1
from google.cloud import artifactregistry_v1, aiplatform
from google.api_core.exceptions import GoogleAPICallError
from google.protobuf import field_mask_pb2

def check_storage_labels(project_id, label_key):
    """Check and add labels to Cloud Storage buckets"""
    storage_client = storage.Client()
    try:
        buckets = storage_client.list_buckets()
        for bucket in buckets:
            labels = bucket.labels or {}
            if label_key not in labels:
                labels[label_key] = project_id
                bucket.labels = labels
                bucket.patch()
                print(f"[GCS] Added label '{label_key}:{project_id}' to bucket '{bucket.name}'")
    except GoogleAPICallError as e:
        print(f"[GCS] Error: {e}")

def check_bigquery_labels(project_id, label_key):
    """Check and add labels to BigQuery datasets"""
    bq_client = bigquery.Client(project=project_id)
    try:
        datasets = list(bq_client.list_datasets())
        for dataset_ref in datasets:
            dataset = bq_client.get_dataset(dataset_ref.dataset_id)
            labels = dataset.labels or {}
            if label_key not in labels:
                labels[label_key] = project_id
                dataset.labels = labels
                bq_client.update_dataset(dataset, ["labels"])
                print(f"[BigQuery] Added label to dataset '{dataset.dataset_id}'")
    except GoogleAPICallError as e:
        print(f"[BigQuery] Error: {e}")

def check_artifact_labels(project_id, label_key, location="us-central1"):
    """Check and add labels to Artifact Registry repositories"""
    artifact_client = artifactregistry_v1.ArtifactRegistryClient()
    try:
        parent = f"projects/{project_id}/locations/{location}"
        repos = artifact_client.list_repositories(parent=parent)
        for repo in repos:
            labels = repo.labels or {}
            if label_key not in labels:
                labels[label_key] = project_id
                repo.labels = labels
                artifact_client.update_repository(
                    repository=repo,
                    update_mask={"paths": ["labels"]}
                )
                print(f"[Artifact] Added label to repo '{repo.name.split('/')[-1]}'")
    except GoogleAPICallError as e:
        print(f"[Artifact] Error: {e}")

def check_dataproc_metastore_labels(project_id, label_key, location="us-central1"):
    """Check and add labels to Dataproc Metastore services"""
    client = metastore_v1.DataprocMetastoreClient()
    try:
        parent = f"projects/{project_id}/locations/{location}"
        services = client.list_services(parent=parent)
        for service in services:
            labels = service.labels or {}
            if label_key not in labels:
                labels[label_key] = project_id
                service.labels = labels
                update_mask = field_mask_pb2.FieldMask(paths=["labels"])
                client.update_service(service=service, update_mask=update_mask)
                print(f"[Metastore] Added label to service '{service.name.split('/')[-1]}'")
    except GoogleAPICallError as e:
        print(f"[Metastore] Error: {e}")

def check_pubsub_labels(project_id, label_key):
    """Check and add labels to Pub/Sub subscriptions"""
    subscriber = pubsub_v1.SubscriberClient()
    try:
        project_path = f"projects/{project_id}"
        subs = subscriber.list_subscriptions(request={"project": project_path})
        for sub in subs:
            labels = sub.labels or {}
            if label_key not in labels:
                labels[label_key] = project_id
                sub.labels = labels
                update_mask = field_mask_pb2.FieldMask(paths=["labels"])
                subscriber.update_subscription(
                    subscription={"name": sub.name, "labels": labels},
                    update_mask=update_mask
                )
                print(f"[PubSub] Added label to sub '{sub.name.split('/')[-1]}'")
    except GoogleAPICallError as e:
        print(f"[PubSub] Error: {e}")

def check_vertexai_labels(project_id, label_key, location="us-central1"):
    """Check and add labels to Vertex AI resources"""
    aiplatform.init(project=project_id, location=location)
    
    # Datasets (use global location)
    try:
        dataset_client = aiplatform.gapic.DatasetServiceClient()
        parent = f"projects/{project_id}/locations/global"  # Use global for datasets
        datasets = dataset_client.list_datasets(parent=parent)
        for dataset in datasets:
            labels = dataset.labels or {}
            if label_key not in labels:
                labels[label_key] = project_id
                dataset.labels = labels
                dataset_client.update_dataset(dataset=dataset)
                print(f"[VertexAI] Added label to dataset '{dataset.name.split('/')[-1]}'")
    except GoogleAPICallError as e:
        print(f"[VertexAI Dataset] Error: {e}")
    
    # Indexes (use the specified location)
    try:
        index_client = aiplatform.gapic.IndexServiceClient()
        parent = f"projects/{project_id}/locations/{location}"  # Use specified location for indexes
        indexes = index_client.list_indexes(parent=parent)
        for index in indexes:
            labels = index.labels or {}
            if label_key not in labels:
                labels[label_key] = project_id
                index.labels = labels
                index_client.update_index(index=index)
                print(f"[VertexAI] Added label to index '{index.name.split('/')[-1]}'")
    except GoogleAPICallError as e:
        print(f"[VertexAI Index] Error: {e}")
    
    # Index Endpoints (use the specified location)
    try:
        endpoint_client = aiplatform.gapic.IndexEndpointServiceClient()
        parent = f"projects/{project_id}/locations/{location}"  # Use specified location for endpoints
        endpoints = endpoint_client.list_index_endpoints(parent=parent)
        for endpoint in endpoints:
            labels = endpoint.labels or {}
            if label_key not in labels:
                labels[label_key] = project_id
                endpoint.labels = labels
                endpoint_client.update_index_endpoint(index_endpoint=endpoint)
                print(f"[VertexAI] Added label to endpoint '{endpoint.name.split('/')[-1]}'")
    except GoogleAPICallError as e:
        print(f"[VertexAI Endpoint] Error: {e}")

if __name__ == "__main__":
    PROJECT_ID = "adk-short-bot-465311"   # Your project ID
    LABEL_KEY = "project_id"              # Label key to check/add
    LOCATION = "us-central1"              # Default region
    
    print("\n=== Processing Cloud Storage ===")
    check_storage_labels(PROJECT_ID, LABEL_KEY)
    
    print("\n=== Processing BigQuery ===")
    check_bigquery_labels(PROJECT_ID, LABEL_KEY)
    
    print("\n=== Processing Artifact Registry ===")
    check_artifact_labels(PROJECT_ID, LABEL_KEY, LOCATION)
    
    print("\n=== Processing Dataproc Metastore ===")
    check_dataproc_metastore_labels(PROJECT_ID, LABEL_KEY, LOCATION)
    
    print("\n=== Processing Pub/Sub ===")
    check_pubsub_labels(PROJECT_ID, LABEL_KEY)
    
    print("\n=== Processing Vertex AI ===")
    check_vertexai_labels(PROJECT_ID, LABEL_KEY, LOCATION)

    print("\nLabel check complete for all services!")
