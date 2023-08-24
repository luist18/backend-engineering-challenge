from datetime import datetime, timedelta
from typing import Any, Dict

import unbabel_cli.config.date as date_config
import unbabel_cli.util.date as date_util
from unbabel_cli.model import MovingAverageAlgorithm


class QueueMovingAverageAlgorithm(MovingAverageAlgorithm):
    """ """

    def __init__(self):
        """Initializes the queue moving average algorithm. The extra
        memory used is declared in the constructor."""

        self.queue_events = []  # O(W) where W is the average number of events in a time window

    def moving_average(self, events: [Dict[str, Any]], window: int = 10) -> [Dict[str, Any]]:
        """Calculates the moving average of the events every minute for
        a given window size. This operation is O(T*(M + M)) = O(2*T*M) where T is the
        number of timestamps, M is the average number of events in a
        minute.

        Args:
            events ([Dict[str, Any]]): a list with objects containing the events
            window (int, optional): the window size. Defaults to 10

        Returns:
            [Dict[str, Any]]: a list of objects with every minute and the
                average delivery time
        """
        # If there are no events immediately return an empty array
        if len(events) == 0:
            return []

        # Reset queue
        self.queue_events = []

        # Define the output list and variables for the average calculation
        output = []

        total = 0
        total_number = 0

        # Get the first timestamp
        current_timestamp = date_util.floor_minute(
            datetime.strptime(events[0]["timestamp"], date_config.INPUT_DATE_FORMAT)
        )

        # While there are events in the stream
        while len(events) > 0:
            # Get the first event in the stream
            event = events[0]

            # Get both variables of interest
            timestamp = datetime.strptime(event["timestamp"], date_config.INPUT_DATE_FORMAT)
            duration = int(event["duration"])

            # We need to remove events that might be out of the window
            if len(self.queue_events) > 0:
                first_timestamp = datetime.strptime(self.queue_events[0]["timestamp"], date_config.INPUT_DATE_FORMAT)

                to_first_delta_minutes = (current_timestamp - first_timestamp).total_seconds() / 60

                # While the delta to the first element in the queue is greater than the
                # window then it has to be removed

                if to_first_delta_minutes > window:
                    remove_duration = int(self.queue_events.pop(0)["duration"])

                    total -= remove_duration
                    total_number -= 1

                    # If this happens, then ensure to run this again if there are multiple cases
                    continue

            # Calculate the delta between the current timestamp and the event timestamp
            event_delta_minutes = (current_timestamp - timestamp).total_seconds() / 60

            # If the delta is positive then we need to add it to the queues of the window
            if event_delta_minutes >= 0:
                # Remove the first element from the queue which is O(1)
                events.pop(0)

                if event_delta_minutes > 0 and event_delta_minutes <= window:
                    self.queue_events.append(event)

                    total += duration
                    total_number += 1

                # We need to check if the next element is in the same minute.
                # If it is then skip the next steps (average and append) and
                # handle the event.
                if len(events) > 0:
                    next_event = events[0]
                    next_timestamp = datetime.strptime(
                        next_event["timestamp"],
                        date_config.INPUT_DATE_FORMAT,
                    )

                    if (
                        timestamp.replace(second=0, microsecond=0) - next_timestamp.replace(second=0, microsecond=0)
                    ).total_seconds() == 0:
                        continue

            average = total / total_number if total_number > 0 else 0

            output.append(
                {
                    "date": current_timestamp.strftime(date_config.OUTPUT_DATE_FORMAT),
                    "average_delivery_time": average,
                }
            )

            current_timestamp += timedelta(minutes=1)

        return output
