import mlflow

from mlflow_utils import create_mlflow_experiment

if __name__ == "__main__":
    # create experiment
    # mlflow.create_experiment(
    #     name="testing_mlflow1",
    #     artifact_location="testing_mlflow1_artifacts",
    #     tags={"env": "dev", "version": "1.0.0"},
    # )

    experiment_id = create_mlflow_experiment(experiment_name="testing_mlflow2", artifact_location="testing_mlflow2_artifacts", tags={"env": "dev", "version": "1.0.0"})
    print(f"Experiment ID: {experiment_id}")