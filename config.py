import tomli
from dataclasses import dataclass


@dataclass
class Config:
    plantuml_path: str
    package_name: str
    output_path: str
    max_depth: int
    repository_url: str


def load_config(config_path: str) -> Config:
    with open(config_path, "rb") as f:
        config_data = tomli.load(f)

    return Config(
        plantuml_path=config_data["visualizer"]["plantuml_path"],
        package_name=config_data["visualizer"]["package_name"],
        output_path=config_data["visualizer"]["output_path"],
        max_depth=config_data["visualizer"]["max_depth"],
        repository_url=config_data["visualizer"]["repository_url"]
    )
