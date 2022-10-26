import json
import os
import random
from abc import ABC
from abc import abstractmethod
from io import TextIOWrapper
from typing import Dict
from typing import Optional
from typing import Type
from typing import Union

from ..logs import Logger
from ..simulator import Simulator


class Runner(ABC):
    def __init__(
        self,
        settings: Union[Dict, TextIOWrapper, os.PathLike, str],
        prng: Optional[random.Random] = None,
        logger: Optional[Logger] = None,
        simulator_class: Type[Simulator] = Simulator,
    ):
        self.settings: Dict
        if isinstance(settings, Dict):
            self.settings = settings
        elif isinstance(settings, TextIOWrapper):
            self.settings = json.load(fp=settings)
        else:
            self.settings = json.load(fp=open(settings, mode="r"))
        self._prng: random.Random = prng if prng is not None else random.Random()
        self.logger = logger
        self.simulator: Simulator = simulator_class(
            prng=random.Random(self._prng.randint(0, 2**31))
        )

    def main(self) -> None:
        self._setup()
        self._run()

    @abstractmethod
    def _setup(self) -> None:
        pass

    @abstractmethod
    def _run(self) -> None:
        pass
