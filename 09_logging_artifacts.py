import mlflow
from mlflow_utils import get_mflow_experiment

if __name__ == "__main__":
    experiment = get_mflow_experiment(experiment_name="testing_mlflow7")

    print("Name: {}".format(experiment.name))

    with mlflow.start_run(run_name="logging_artifacts", experiment_id=experiment.experiment_id) as run:

        # Machine Learning Code

        # create a text file
        with open("hello_word2.txt", "w") as f:
            f.write("Hello, World!")

        # log the text file
        mlflow.log_artifact(local_path="hello_word2.txt", artifact_path="text_files")

        # Run info
        print("Run_id: {}".format(run.info.run_id))
        print("Experiment_id: {}".format(run.info.experiment_id))
        print("status: {}".format(run.info.status))
        print("start_time: {}".format(run.info.start_time))
        print("end_time: {}".format(run.info.end_time))
        print("life_cycle_stage: {}".format(run.info.lifecycle_stage))
