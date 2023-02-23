from diagrams import Cluster, Edge, Diagram
from diagrams.onprem.client import User, Users
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.aws.storage import SimpleStorageServiceS3 as S3
from diagrams.onprem.database import Mssql as MSSQL 
from diagrams.oci.monitoring import Telemetry

with Diagram("Deployment Architecture diagram", show=False):
    # Define Nodes
    ingress = Users("User")
    with Cluster("Compute Instance"):
        with Cluster("Applications"):
            userfacing = Docker("Streamlit")
            backend = Docker("FastAPI")
            userfacing - Edge(label = "API calls", color="red", style="dashed") - backend
        
        with Cluster("Database"):
            db = MSSQL ("SQLite")

        with Cluster("Batch Process"):
            airflow = Airflow("Streamlit")
            GE = Telemetry("Data Quality Check")
            hosting = S3("Reports")

    backend << Edge(label="Verify Login") << db
    devlopers = User("Developers")
    dataset = S3("Open Dataset")

    GE << Edge(label="CSV of metadata") << db
    GE >> Edge(label="Host the static html report") >> hosting
    airflow >> Edge(label="Run Great Expectation") >> GE

    airflow << Edge(label="metadata collection") << dataset
    airflow >> Edge(label="Update AWS bucket metadata") >> db

    ingress >> Edge(label = "Login to Dashboard",color="darkgreen") << userfacing
    devlopers << Edge(label = "View Reports",color="darkgreen") << hosting
    devlopers << Edge(label = "View Dashboard",color="darkgreen") << airflow