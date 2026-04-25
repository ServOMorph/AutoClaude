"""Tests pour core.content_loader."""

import pytest
from pathlib import Path
from unittest.mock import patch
from src.core.content_loader import _parse_md, load_tips, load_prompts, load_learnings


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    import core.content_loader  # noqa: F401


class TestParseMd:
    """Tests pour _parse_md."""

    def test_parse_with_frontmatter(self, temp_markdown_file):
        """Parse markdown avec frontmatter YAML."""
        meta, body = _parse_md(temp_markdown_file)
        assert meta["title"] == "Test Document"
        assert meta["category"] == "test"
        assert "Body content here" in body

    def test_parse_without_frontmatter(self, temp_dir):
        """Parse markdown sans frontmatter."""
        md_path = temp_dir / "plain.md"
        md_path.write_text("Just content\nNo frontmatter", encoding="utf-8")
        meta, body = _parse_md(md_path)
        assert meta == {}
        assert "Just content" in body

    def test_parse_empty_file(self, temp_dir):
        """Parse fichier vide."""
        md_path = temp_dir / "empty.md"
        md_path.write_text("", encoding="utf-8")
        meta, body = _parse_md(md_path)
        assert meta == {}
        assert body == ""

    def test_parse_malformed_frontmatter(self, temp_dir):
        """Parse fichier avec frontmatter mal formé."""
        md_path = temp_dir / "bad.md"
        md_path.write_text("---\nmalformed\n---\nContent", encoding="utf-8")
        meta, body = _parse_md(md_path)
        assert body == "Content"


class TestLoadTips:
    """Tests pour load_tips."""

    def test_load_tips_empty_dir(self, temp_dir):
        """load_tips sur dossier vide retourne []."""
        with patch("src.core.content_loader.CONTENT_DIR", temp_dir):
            tips = load_tips()
            assert tips == []

    def test_load_tips_single(self, temp_dir):
        """load_tips charge un seul fichier."""
        tips_dir = temp_dir / "tips"
        tips_dir.mkdir()
        tip_file = tips_dir / "test.md"
        tip_file.write_text("---\ntitle: Test Tip\ncategory: core\n---\nContent here", encoding="utf-8")

        with patch("src.core.content_loader.CONTENT_DIR", temp_dir):
            tips = load_tips()

            assert len(tips) == 1
            assert tips[0]["title"] == "Test Tip"
            assert tips[0]["category"] == "core"
            assert tips[0]["content"] == "Content here"

    def test_load_tips_multiple(self, temp_dir):
        """load_tips charge plusieurs fichiers triés."""
        tips_dir = temp_dir / "tips"
        tips_dir.mkdir()

        for i in ["a", "b", "c"]:
            tip_file = tips_dir / f"{i}.md"
            tip_file.write_text(f"---\ntitle: Tip {i}\n---\nContent {i}", encoding="utf-8")

        with patch("src.core.content_loader.CONTENT_DIR", temp_dir):
            tips = load_tips()

            assert len(tips) == 3
            assert tips[0]["title"] == "Tip a"
            assert tips[1]["title"] == "Tip b"
            assert tips[2]["title"] == "Tip c"


class TestLoadPrompts:
    """Tests pour load_prompts."""

    def test_load_prompts_empty(self, temp_dir):
        """load_prompts sur dossier vide retourne []."""
        with patch("src.core.content_loader.CONTENT_DIR", temp_dir):
            prompts = load_prompts()
            assert prompts == []

    def test_load_prompts_with_tags(self, temp_dir):
        """load_prompts parse tags depuis frontmatter."""
        prompts_dir = temp_dir / "prompts"
        prompts_dir.mkdir()
        prompt_file = prompts_dir / "test.md"
        prompt_file.write_text(
            "---\ntitle: Test Prompt\nia_target: claude_code\ntags: debug, coding\n---\nPrompt content",
            encoding="utf-8"
        )

        with patch("src.core.content_loader.CONTENT_DIR", temp_dir):
            prompts = load_prompts()

            assert len(prompts) == 1
            assert prompts[0]["title"] == "Test Prompt"
            assert prompts[0]["ia_target"] == "claude_code"
            assert prompts[0]["tags"] == ["debug", "coding"]


class TestLoadLearnings:
    """Tests pour load_learnings."""

    def test_load_learnings_empty(self, temp_dir):
        """load_learnings sur dossier vide retourne {}."""
        with patch("src.core.content_loader.CONTENT_DIR", temp_dir):
            learnings = load_learnings()
            assert learnings == {}

    def test_load_learnings_with_subdomains(self, temp_dir):
        """load_learnings organise par sous-domaine."""
        learnings_dir = temp_dir / "learnings"
        learnings_dir.mkdir()

        for domain in ["core", "ui", "security"]:
            domain_dir = learnings_dir / domain
            domain_dir.mkdir()
            learning_file = domain_dir / f"{domain}_1.md"
            learning_file.write_text(
                f"---\ntitle: {domain.upper()} Learning\nseverity: HIGH\n---\nContent",
                encoding="utf-8"
            )

        with patch("src.core.content_loader.CONTENT_DIR", temp_dir):
            learnings = load_learnings()

            assert set(learnings.keys()) == {"core", "ui", "security"}
            for domain in ["core", "ui", "security"]:
                assert len(learnings[domain]) >= 1
                assert learnings[domain][0]["severity"] == "HIGH"

    def test_load_learnings_ignores_non_dirs(self, temp_dir):
        """load_learnings ignore les fichiers non-répertoires."""
        learnings_dir = temp_dir / "learnings"
        learnings_dir.mkdir()

        domain_dir = learnings_dir / "core"
        domain_dir.mkdir()
        learning_file = domain_dir / "test.md"
        learning_file.write_text("---\ntitle: Test\n---\nContent", encoding="utf-8")

        file_in_root = learnings_dir / "readme.txt"
        file_in_root.write_text("ignore me", encoding="utf-8")

        with patch("src.core.content_loader.CONTENT_DIR", temp_dir):
            learnings = load_learnings()

            assert "core" in learnings
            assert len(learnings) == 1
