import time
from locust import User, task, between
import capacity_target


class CapacityUser(User):
    """
    Locust user that repeatedly calls compute_capacity_value()
    so we can measure capacity of the prediction.
    """

    # optional small think-time between calls
    wait_time = between(0.1, 0.5)

    @task
    def test_compute_capacity_value(self):
        start = time.time()

        try:
            # This is the function we are capacity-testing
            _ = capacity_target.compute_capacity_value()

            total_ms = (time.time() - start) * 1000.0

            # Log as a successful "request"
            # method="function", name="compute_capacity_value"
            self.environment.runner.stats.log_request(
                "function",               # method
                "compute_capacity_value", # name
                total_ms,                 # response_time (ms)
                0,                        # content_length
            )

        except Exception as e:
            total_ms = (time.time() - start) * 1000.0

            # IMPORTANT: positional args only, NO request_type=
            self.environment.runner.stats.log_error(
                "function",               # method
                "compute_capacity_value", # name
                e,                        # error
            )
