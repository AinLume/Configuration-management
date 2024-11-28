import unittest
from pathlib import Path
import os
from main import GitDependencyGraph

class TestGitDependencyGraph(unittest.TestCase):
    def setUp(self):
        self.config_file = "test_config.csv"
        with open(self.config_file, "w") as file:
            file.write("key,value\n")
            file.write("repository_path,./\n")
            file.write("output_file,./test_output.puml\n")
        self.graph = GitDependencyGraph(self.config_file)

    def tearDown(self):
        os.remove(self.config_file)
        if Path("test_output.puml").exists():
            os.remove("test_output.puml")

    def test_load_config(self):
        self.assertEqual(self.graph.config["repository_path"], "./")
        self.assertEqual(self.graph.config["output_file"], "./test_output.puml")

    def test_check_git_repo(self):
        with self.assertRaises(FileNotFoundError):
            self.graph.repo_path = Path("nonexistent")
            self.graph.check_git_repo()

    def test_get_commit_dependencies(self):
        self.graph.repo_path = Path("./")
        dependencies = self.graph.get_commit_dependencies()
        self.assertIsInstance(dependencies, list)

    def test_generate_plantuml_graph(self):
        dependencies = [("abc123", "def456"), ("def456", "ghi789")]
        graph_code = self.graph.generate_plantuml_graph(dependencies)
        self.assertIn("@startuml", graph_code)
        self.assertIn('"def456" -> "abc123";', graph_code)

    def test_save_graph(self):
        graph_code = "@startuml\ndigraph G {\n}\n@enduml"
        self.graph.save_graph(graph_code)
        with open("test_output.puml", "r") as file:
            content = file.read()
        self.assertEqual(content, graph_code)


if __name__ == "__main__":
    unittest.main()
