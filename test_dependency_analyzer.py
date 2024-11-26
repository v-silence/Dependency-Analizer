import unittest
from dependency_analyzer import DependencyAnalyzer

class TestDependencyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = DependencyAnalyzer(max_depth=2)

    def test_get_package_dependencies(self):
        deps = self.analyzer.get_package_dependencies("requests")
        self.assertIsInstance(deps, set)
        self.assertTrue(len(deps) > 0)

    def test_max_depth_limit(self):
        analyzer = DependencyAnalyzer(max_depth=0)
        deps = analyzer.get_package_dependencies("requests")
        self.assertEqual(len(deps), 0)

    def test_invalid_package(self):
        deps = self.analyzer.get_package_dependencies("invalid-package-name")
        self.assertEqual(len(deps), 0)
