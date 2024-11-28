import subprocess
import csv
from pathlib import Path
import argparse


class GitDependencyGraph:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.repo_path = Path(self.config.get("repository_path", "."))
        self.output_file = Path(self.config.get("output_file", "graph.puml"))
        self.check_git_repo()

    def load_config(self, config_file):
        with open(config_file, "r") as file:
            reader = csv.DictReader(file)
            self.config = {row["key"]: row["value"] for row in reader}

    def check_git_repo(self):
        if not self.repo_path.exists() or not (self.repo_path / ".git").exists():
            raise FileNotFoundError(f"{self.repo_path} не является git-репозиторием.")

    def get_commit_dependencies(self):
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_path), "log", "--pretty=format:%H %P"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode != 0:
                raise RuntimeError(f"Ошибка git: {result.stderr.strip()}")
        except FileNotFoundError:
            raise RuntimeError("Git не установлен или недоступен.")

        dependencies = []
        for line in result.stdout.strip().split("\n"):
            parts = line.split()
            commit_hash = parts[0]
            parent_hashes = parts[1:]
            for parent in parent_hashes:
                dependencies.append((commit_hash, parent))
        return dependencies

    def generate_plantuml_graph(self, dependencies):
        lines = ["@startuml", "digraph G {"]
        for child, parent in dependencies:
            lines.append(f'  "{parent}" -> "{child}";')
        lines.append("}")
        lines.append("@enduml")
        return "\n".join(lines)

    def save_graph(self, graph_code):
        with open(self.output_file, "w") as file:
            file.write(graph_code)

    def run(self):
        dependencies = self.get_commit_dependencies()
        graph_code = self.generate_plantuml_graph(dependencies)
        print(graph_code)
        self.save_graph(graph_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Git Dependency Graph Visualizer")
    parser.add_argument(
        "config_file", type=str, help="Path to the configuration CSV file"
    )
    args = parser.parse_args()

    try:
        visualizer = GitDependencyGraph(args.config_file)
        visualizer.run()
    except Exception as e:
        print(f"Ошибка: {e}")
