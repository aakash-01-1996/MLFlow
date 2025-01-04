import mlflow
from mlflow_utils import get_mflow_experiment

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

if __name__ == "__main__":

    experiment = get_mflow_experiment(experiment_name="testing_mlflow7")
    print("Name: {}".format(experiment.name))

    with mlflow.start_run(
        run_name="logging_models", experiment_id=experiment.experiment_id
    ) as run:

        X, y = make_classification(
            n_samples=1000,
            n_features=10,
            n_informative=5,
            n_redundant=5,
            random_state=42,
        )
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=43
        )

        # log model parameters
        mlflow.autolog()

        rfc = RandomForestClassifier(n_estimators=100, random_state=42)
        rfc.fit(X_train, y_train)
        y_pred = rfc.predict(X_test)

        # Run info
        print("Run_id: {}".format(run.info.run_id))
        print("Experiment_id: {}".format(run.info.experiment_id))
        print("status: {}".format(run.info.status))
        print("start_time: {}".format(run.info.start_time))
        print("end_time: {}".format(run.info.end_time))
        print("life_cycle_stage: {}".format(run.info.lifecycle_stage))
