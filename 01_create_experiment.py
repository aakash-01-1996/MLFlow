import mlflow

from mlflow_utils import create_mlflow_experiment

if __name__ == "__main__":
    
    # create a new mlflow experiment
    experiment_id = mlflow.create_experiment(
        name="testing_mlflow7",
        artifact_location="testing_mlflow1_artifacts",
        tags={"env": "dev", "version": "1.0.0"},
    )

    print(experiment_id)