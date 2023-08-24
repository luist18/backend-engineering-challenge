from datetime import datetime, timedelta
from typing import Any, Dict

import unbabel_cli.config.date as date_config
import unbabel_cli.util.date as date_util
from unbabel_cli.model import MovingAverageAlgorithm


class HashMapMovingAverageAlgorithm(MovingAverageAlgorithm):
    """This class implements the hash map moving average algorithm.

    It uses an hash map to store the duration of the events and reduce
    the time complexity of the algorithm. The time complexity of this
    algorithm is O(T*M+E) where T is the number of timestamps, M is the
    average number of events in a minute and E is the number of events.

    The space complexity of this algorithm is O(n) where n is the number
    of entries in the hash map. Which also means that the space complexity
    is O(E) where E is the number of events.
    """

    def __init__(self):
        """Initializes the hash map moving average algorithm. The extra
        memory used is declared in the constructor."""

        # Space complexity of an hash map is O(n) where n is the number of entries.
        self.duration_set = {}

    def __set_or_append(self, key: int, value: int) -> None:
        """Sets or appends a value to the duration set. This operation
        is O(1).

        Args:
            key (int): the key to set or append the value
            value (int): the value to set or append
        """
        if key in self.duration_set:
            self.duration_set[key].append(value)
        else:
            self.duration_set[key] = [value]

    def __add_to_duration_set(self, timestamp: datetime, duration: int, window: int) -> None:
        """Adds a duration to the duration set. This operation is O(1).

        Args:
            timestamp (datetime): the timestamp of the event
            duration (int): the duration of the event
            window (int): the window size
        """
        add_timestamp = date_util.ceil_minute(timestamp)

        remove_timestamp = date_util.ceil_minute(timestamp + timedelta(minutes=window))

        add_timestamp_key = add_timestamp.timestamp()
        remove_timestamp_key = remove_timestamp.timestamp()

        self.__set_or_append(add_timestamp_key, duration)
        self.__set_or_append(remove_timestamp_key, -duration)

    def moving_average(self, events: [Dict[str, Any]], window: int = 10) -> [Dict[str, Any]]:
        """Calculates the moving average of the events every minute for
        a given window size. This operation is O(T*M+E) where T is the
        number of timestamps, M is the average number of events in a
        minute and E is the number of events.

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

        # Reset the duration set and add each event duration to the
        # duration set. O(E), E is the number of events.
        self.duration_set = {}

        for event in events:
            # Get both variables of interest
            timestamp = datetime.strptime(event["timestamp"], date_config.INPUT_DATE_FORMAT)
            duration = int(event["duration"])

            self.__add_to_duration_set(timestamp, duration, window)

        # Define the output list and variables for the average calculation
        output = []

        total = 0
        total_number = 0

        # Get the first and last timestamp. The last timestamp
        # is incremented by one minute from the timestamp of the last
        # event.
        current_timestamp = date_util.floor_minute(
            datetime.strptime(events[0]["timestamp"], date_config.INPUT_DATE_FORMAT)
        )

        last_timestamp = date_util.floor_minute(
            datetime.strptime(events[-1]["timestamp"], date_config.INPUT_DATE_FORMAT) + timedelta(minutes=1)
        )

        # Iterate each timestamp. O(T) where T is the number of timestamps.
        # As we have a for inside this while loop we also have to consider
        # it for the time complexity.
        #
        # The for loop iterates over the number of events in a minute.
        # O(M) where M is the average number of events in a minute.
        #
        # The time complexity of this loop is O(T*M).
        while current_timestamp <= last_timestamp:
            timestamp_key = current_timestamp.timestamp()

            if timestamp_key in self.duration_set:
                for number in self.duration_set[timestamp_key]:
                    total += number

                    # If the number is positive we have to add it to the total number
                    # as it is a new event. If the number is negative we have to
                    # subtract it from the total number as it is an event that
                    # has been passed the window size.
                    total_number = total_number + 1 if number > 0 else total_number - 1

            average = total / total_number if total_number > 0 else 0

            # Append the average to the output list
            output.append(
                {
                    "date": current_timestamp.strftime(date_config.OUTPUT_DATE_FORMAT),
                    "average_delivery_time": average,
                }
            )

            # Increment the current timestamp by one minute
            current_timestamp += timedelta(minutes=1)

        return output
