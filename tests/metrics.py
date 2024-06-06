import json
import os
import time
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Metric:
    key: str
    value: int
    _time: float
    _id: str
    _implementation: str


@dataclass
class Metrics:
    implementation: str
    metrics: list[Metric] = field(default_factory=list)
    run_id: str = str(uuid4())

    def add(self, key: str, value: int):
        self.metrics.append(
            Metric(
                key=key,
                value=value,
                _time=time.time(),
                _id=self.run_id,
                _implementation=self.implementation,
            )
        )

    def to_jsonl(self, file=__file__):
        _metrics = [m.__dict__ for m in self.metrics]
        _file = os.path.basename(file).replace(".py", "")
        # Get the current POSIX timestamp
        ts = int(time.time())
        # Set hours, minutes, and seconds to zero to get the start of the day timestamp
        ts = ts - (ts % 86400)
        file_path = f"metrics/{ts}_{_file}_metrics.jsonl"
        with open(file_path, "a") as file:
            for _metric in _metrics:
                file.write(json.dumps(_metric) + "\n")
