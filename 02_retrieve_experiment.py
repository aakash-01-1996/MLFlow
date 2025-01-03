import mlflow
from mlflow_utils import get_mflow_experiment

if __name__ == "__main__":

    # retrieve experiment
    experiment = get_mflow_experiment(experiment_id="795624509464015525")

    print("Name: {}".format(experiment.name))
    print("Experiment_id: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Tags: {}".format(experiment.tags))
    print("Lifecycle_Stage: {}".format(experiment.lifecycle_stage))
    print("creation timestamp: {}".format(experiment.creation_time))