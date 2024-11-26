import os
import subprocess
from typing import Set, Tuple


class PlantUMLGenerator:
    def __init__(self, plantuml_path: str):
        self.plantuml_path = plantuml_path

    def generate_diagram(self, dependencies: Set[Tuple[str, str]], output_path: str) -> bool:
        plantuml_content = self._create_plantuml_content(dependencies)

        try:
            # Создаем временный файл с диаграммой
            temp_file = "temp.puml"
            with open(temp_file, "w", encoding='utf-8') as f:
                f.write(plantuml_content)

            # Определяем команду запуска PlantUML
            if self.plantuml_path.endswith('.jar'):
                cmd = ['java', '-jar', self.plantuml_path, temp_file]
            else:
                cmd = [self.plantuml_path, temp_file]

            # Создаем директорию для выходного файла, если её нет
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

            # Запускаем PlantUML
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            # Удаляем временный файл
            if os.path.exists(temp_file):
                os.remove(temp_file)

            if result.returncode != 0:
                print(f"PlantUML Error: {result.stderr}")
                return False

            return True

        except Exception as e:
            print(f"Error generating diagram: {str(e)}")
            return False

    def _create_plantuml_content(self, dependencies: Set[Tuple[str, str]]) -> str:
        content = ["@startuml"]
        content.append("skinparam rectangle {")
        content.append("    BackgroundColor<<root>> LightGreen")
        content.append("}")

        # Добавляем уникальные узлы
        nodes = set()
        for source, target in dependencies:
            nodes.add(source)
            nodes.add(target)

        for node in nodes:
            content.append(f'rectangle "{node}" as {node.replace("-", "_")}')

        # Добавляем связи
        for source, target in dependencies:
            content.append(f'{source.replace("-", "_")} --> {target.replace("-", "_")}')

        content.append("@enduml")
        return "\n".join(content)
