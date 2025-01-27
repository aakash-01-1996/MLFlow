from mlflow_utils import create_mlflow_experiment
from mlflow import MlflowClient

from mlflow.types.schema import Schema
from mlflow.types.schema import ColSpec

if __name__ == "__main__":

    experiment_id = create_mlflow_experiment(
        experiment_name="model_registry",
        artifact_location="model_registry_artifacts",
        tags={"purpose": "learning"},
    )

    print(experiment_id)

    client = MlflowClient()
    model_name = "registered_model_1"

    # adding description to registired model.
    client.update_registered_model(name=model_name, description="This is a test model")

    # adding tags to registired model.
    client.set_registered_model_tag(name=model_name, key="tag1", value="value1")

    # adding description to model version.
    client.update_model_version(
        name=model_name, version=1, description="This is a test model version"
    )

    # adding tags to model version.
    client.set_model_version_tag(name=model_name, version=1, key="tag1", value="value1")
