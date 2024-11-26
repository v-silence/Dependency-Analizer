import argparse
import sys
from config import load_config
from dependency_analyzer import DependencyAnalyzer
from plantuml_generator import PlantUMLGenerator


def main():
    parser = argparse.ArgumentParser(description="Python package dependency visualizer")
    parser.add_argument("--config", default="config.toml", help="Path to config file")
    args = parser.parse_args()

    try:
        config = load_config(args.config)

        analyzer = DependencyAnalyzer(config.max_depth)
        dependencies = analyzer.get_package_dependencies(config.package_name)

        generator = PlantUMLGenerator(config.plantuml_path)
        success = generator.generate_diagram(dependencies, config.output_path)

        if success:
            print(f"Dependencies graph has been generated successfully: {config.output_path}")
            sys.exit(0)
        else:
            print("Failed to generate dependencies graph")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
