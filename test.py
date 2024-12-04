import unittest
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
from Graph import get_commit_history, build_mermaid_graph, save_mermaid_file, display_graph


class TestGraph(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_commit_history(self, mock_subprocess):
        """Тест на извлечение истории коммитов."""
        mock_subprocess.return_value = MagicMock(
            returncode=0,
            stdout=(
                "abc123 Commit 1\nfile1.txt\n\n"
                "def456 Commit 2\nfile2.txt\nfile3.txt\n\n"
                "ghi789 Commit 3\n"
            )
        )

        repo_path = "fake-repo"
        before_date = datetime.strptime("2024-12-01", "%Y-%m-%d")
        result = get_commit_history(repo_path, before_date)

        expected_result = [
            ("abc123", "Commit 1", ["file1.txt"]),
            ("def456", "Commit 2", ["file2.txt", "file3.txt"]),
            ("ghi789", "Commit 3", [])
        ]

        self.assertEqual(result, expected_result)

    def test_build_mermaid_graph(self):
        """Тест на корректность построения графа Mermaid."""
        commits = [
            ("abc123", "Commit 1", ["file1.txt"]),
            ("def456", "Commit 2", ["file2.txt", "file3.txt"]),
            ("ghi789", "Commit 3", [])
        ]

        result = build_mermaid_graph(commits)

        expected_result = (
            "graph TD\n"
            '    abc123["Commit 1<br>"]\n'
            '    def456["Commit 2<br>"]\n'
            "    def456 --> abc123\n"
            '    ghi789["Commit 3<br>"]\n'
            "    ghi789 --> def456\n"
        )

        self.assertEqual(result, expected_result)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_mermaid_file(self, mock_open_func):
        """Тест на сохранение графа в файл."""
        mermaid_graph = "graph TD\nabc123 --> def456\n"
        output_path = "test_graph.mmd"

        save_mermaid_file(mermaid_graph, output_path)

        mock_open_func.assert_called_once_with(output_path, 'w', encoding="utf-8")
        mock_open_func().write.assert_called_once_with(mermaid_graph)

    @patch('subprocess.run')
    @patch('os.startfile')
    def test_display_graph(self, mock_startfile, mock_subprocess):
        """Тест на отображение графа."""
        mock_subprocess.return_value = MagicMock(returncode=0)
        mermaid_path = "graph.mmd"
        mermaid_tool_path = "mmdc"

        display_graph(mermaid_path, mermaid_tool_path)

        mock_subprocess.assert_called_once_with([mermaid_tool_path, "-i", mermaid_path, "-o", "graph.png"])
        mock_startfile.assert_called_once_with("graph.png")

    def test_empty_commit_history(self):
        """Тест на обработку пустой истории коммитов."""
        commits = []
        result = build_mermaid_graph(commits)
        expected_result = "graph TD\n"

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
