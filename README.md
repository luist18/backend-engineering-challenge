# unbabel-backend-challenge<!-- omit in toc -->

![https://img.shields.io/badge/License-MIT-blue](https://img.shields.io/badge/License-MIT-blue)

Unbabel backend challenge part of the recruitment process.

## Table of Contents<!-- omit in toc -->

- [1. Challenge Scenario](#1-challenge-scenario)
- [2. Installation](#2-installation)
- [3. How to Run](#3-how-to-run)
- [4. How to Test](#4-how-to-test)
- [5. Algorithms](#5-algorithms)
  - [5.1. Hash Map Algorithm](#51-hash-map-algorithm)
  - [5.2. Queue Algorithm](#52-queue-algorithm)
  - [5.3. Future Improvements](#53-future-improvements)
- [6. License](#6-license)


## 1. Challenge Scenario

The challenge consists of implementing a moving average algorithm that calculates, for every minute, the average delivery time of translations, considering translations submitted in the last X minutes (being X a configurable parameter).

For a detailed description of the challenge scenario, please refer to the [GitHub repository of the challenge](https://github.com/Unbabel/backend-engineering-challenge).

## 2. Installation

This project is built with [poetry](https://python-poetry.org/). If you don't have poetry installed, please follow the [installation instructions](https://python-poetry.org/docs/#installation).

To install the project dependencies, run the following command:

```bash
poetry install
```

To activate the virtual environment, run the following command:

```bash
poetry shell
```

## 3. How to Run

To run the project, run the `unbabel_cli` module with the following command:

```bash
python -m unbabel_cli <arguments>
```

The arguments are the following:

- `--input_file` **(required)**: Path to the input file.
- `--window_size` **(required)**: Window size. Must be zero or a positive integer.
- `--algorithm` **(optional)**: Algorithm to use. Must be one of `hash_map` or `queue`. Defaults to `hash_map`.

The output is printed to the standard output. To redirect it to a file, use the following command:

```bash
python -m unbabel_cli <arguments> > output_file
```

## 4. How to Test

The project uses [pytest](https://docs.pytest.org/en/stable/) for testing. To run the tests, run the following command:

```bash
pytest
```

or the following command to run the tests with coverage:

```bash
pytest --cov
```

Alternatively, you can run `pytest` with `poetry` with the following command:

```bash
poetry run pytest
```

## 5. Algorithms

This section describes the algorithms used to solve the challenge. The algorithms are implemented in the `unbabel_cli.algorithms` module.

### 5.1. Hash Map Algorithm

The Hash Map algorithm uses a hash map to store the timestamps where the duration of an event is added or removed to the total duration of the window. The hash map is implemented with a Python dictionary.

For instance, consider the following entry. The following minute to the event's minute is the first minute where the duration is going to be considered in the window (if the window is different from 0). So, we can set a value in the hash map with the POSIX timestamp of the date `2016-12-26 18:12` (the following minute) with a value of `[20]` (which is the duration). We also know that the value has to be removed once the window is over. So, we can set the value in the hash map with the POSIX timestamp of the date `2016-12-26 18:12 + window size` with a value of `[-20]` (which is the negative duration).

```json
{
  "timestamp": "2016-12-26 18:11:08.509654",
  "translation_id": "5aa5b2f39f7254a75aa5",
  "source_language": "en",
  "target_language": "fr",
  "client_name": "airliberty",
  "event_name": "translation_delivered",
  "nr_words": 30,
  "duration": 20
}
```

Iterating over every minute between the first and last timestamp of the input file, we can calculate the average duration of the window by summing the values of the hash map for each minute whenever an event occurs in that timestamp.

**Time complexity**: O(T*M+E), where T is the number of minutes between the first and last event, M is the average number of events per minute and E is the number of events.

**Space complexity**: O(E), where E is the number of minutes between the first and last event.

**Pros**: this algorithm does not require the events to be sorted by timestamp, yet it requires to know the first timestamp.


### 5.2. Queue Algorithm

The Queue algorithm uses two queues to store the timestamps and the durations of the events. The queues are implemented with Python lists.

The algorithm iterates over every minute, if in that minute a new event is seen (_i.e._, has a `delta > 0`, where delta is the time difference between the current minute and the event's timestamp) the values are added to the queue.

In every minute the algorithm checks if the elements in the front of the queue are older than the window size. If they are, the values are removed from both queues. The moving average in each minute is calculated by summing the values in the queue and dividing by the number of elements in the queue.

**Time complexity**: O(T*2*M), where T is the number of minutes between the first and last event and M is the average number of events per minute.

**Space complexity**: O(W), where W is the average number of events in the window.

**Cons**: this algorithm requires events to be sorted by timestamp.

### 5.3. Future Improvements

- Add validation to input event objects.
- Verify if the events are sorted by timestamp if the algorithm requires.
- Explore other data structures to improve the time and space complexity of the algorithms.

## 6. License

[MIT](https://opensource.org/licenses/MIT)
