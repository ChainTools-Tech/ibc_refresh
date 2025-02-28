import json
import os

class FailureTracker:
    def __init__(self, config):
        log_directory = config.get("log_directory", ".logs/")
        failure_tracker_file = config.get("failure_tracker_log_file", "failure_tracker.json")
        self.failure_tracker_path = os.path.join(log_directory, failure_tracker_file)

        # Ensure log directory exists
        os.makedirs(log_directory, exist_ok=True)

        self.failure_data = self.load_failures()

    def load_failures(self):
        if os.path.exists(self.failure_tracker_path):
            with open(self.failure_tracker_path, "r") as file:
                return json.load(file)
        return {}

    def save_failures(self):
        with open(self.failure_tracker_path, "w") as file:
            json.dump(self.failure_data, file, indent=4)

    def increment_failure(self, task_key):
        self.failure_data[task_key] = self.failure_data.get(task_key, 0) + 1
        self.save_failures()
        return self.failure_data[task_key]

    def reset_failure(self, task_key):
        if task_key in self.failure_data:
            del self.failure_data[task_key]
            self.save_failures()
