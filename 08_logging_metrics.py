import mlflow
from mlflow_utils import get_mflow_experiment

if __name__ == "__main":

    experiment = get_mflow_experiment(experiment_name="testing_mlflow4")
    print("Name: {}".format(experiment.name))

    with mlflow.start_run(
        run_name="logging_metrics", experiment_id=experiment.experiment_id
    ) as run:

        # Machine Learning code
        mlflow.log_metric("mse", 0.01)

        metrics = {"mse": 0.01, "mae": 0.01, "rmse": 0.01, "r2": 0.01}

        mlflow.log_metrics(metrics)

        # Run run info
        print("run_id: {}".format(run.info.run_id))
        print("experiment_id: {}".format(run.info.experiment_id))
        print("status: {}".format(run.info.status))
        print("start_time: {}".format(run.info.start_time))
        print("end_time: {}".format(run.info.end_time))
        print("life_cycle_stage: {}".format(run.info.lifecycle_stage))
