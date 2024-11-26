import pkg_resources
from typing import Dict, Set, Tuple


class DependencyAnalyzer:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        self.dependencies = {}

    def get_package_dependencies(self, package_name: str, depth: int = 0) -> Set[Tuple[str, str]]:
        if depth >= self.max_depth:
            return set()

        if package_name in self.dependencies:
            return self.dependencies[package_name]

        try:
            # Получаем зависимости напрямую через pkg_resources
            dist = pkg_resources.get_distribution(package_name)
            requires = dist.requires()

            dependencies = set()

            for req in requires:
                dep_name = req.project_name
                dependencies.add((package_name, dep_name))
                sub_deps = self.get_package_dependencies(dep_name, depth + 1)
                dependencies.update(sub_deps)

            self.dependencies[package_name] = dependencies
            return dependencies

        except Exception as e:
            print(f"Error analyzing {package_name}: {str(e)}")
            return set()