import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

# Actual imports as required
from local_builder.tool_agent import model_manager, safe_path, context_limit
from local_builder import desktop

class TestToolAgentSafety(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        # Resolve symlink for macOS /var before comparing paths
        self.root = Path(self.temp_dir.name).resolve()
        
        # Use module function directly as per requirements
        self.host = SimpleNamespace(
            path_in=lambda r, n: desktop.path_in(r, n),
            STATE={},
            gate=lambda: None,
            save=lambda: None
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_safe_path_allowed_and_restricted_paths(self):
        """Test safe_path allows valid src/main.py and rejects restricted paths."""
        # Create a dummy file to ensure path resolution works for allowed case
        (self.root / 'src').mkdir(parents=True, exist_ok=True)
        (self.root / 'src' / 'main.py').touch()

        with self.subTest('allowed_src_main_py'):
            result = safe_path(self.host, self.root, 'src/main.py')
            # Ensure resolved path matches expected
            self.assertEqual(result.resolve(), (self.root / 'src' / 'main.py').resolve())

        restricted_paths = [
            '.hidden',
            'project.py',  # Corrected from managed/file.txt per instructions
            '/absolute/path',
            '../traversal',
            'secret.key'
        ]
        for path in restricted_paths:
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    safe_path(self.host, self.root, path)

    def test_context_limit_model_validation(self):
        """Test context_limit validates model capabilities and existence."""
        mock_catalog = [
            {
                'key': 'valid-model',
                'loaded_instances': [{'id': 'inst-1', 'config': {'context_length': 8192}}],
                'capabilities': {'trained_for_tool_use': True}
            },
            {
                'key': 'unsupported-model',
                'loaded_instances': [{'id': 'inst-2'}],
                'capabilities': {'trained_for_tool_use': False}
            }
        ]

        with patch.object(model_manager, 'catalog', return_value=mock_catalog):
            # Test valid model returns context length
            limit = context_limit('valid-model')
            self.assertEqual(limit, 8192)

            # Test unsupported model raises ValueError
            with self.assertRaises(ValueError) as ctx:
                context_limit('unsupported-model')
            self.assertIn('tool-capable', str(ctx.exception))

            # Test absent model raises ValueError
            with self.assertRaises(ValueError) as ctx:
                context_limit('absent-model')
            self.assertIn('Load the selected model', str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
