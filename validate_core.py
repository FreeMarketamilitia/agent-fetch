#!/usr/bin/env python3
"""
Simple validation script for the agent-fetch core functionality.

This script validates that the modular design works correctly without requiring
all external dependencies to be installed.
"""

import sys
import pathlib

# Add the current directory to the path
sys.path.insert(0, str(pathlib.Path(__file__).parent))

def test_config_manager_basic():
    """Test ConfigManager basic functionality."""
    print("Testing ConfigManager...")

    try:
        from agents_collector.config.config_manager import ConfigManager

        # Test with custom config dir to avoid affecting real config
        import tempfile
        temp_dir = pathlib.Path(tempfile.mkdtemp())

        config = ConfigManager(str(temp_dir))

        # Test set/get operations
        config.set("test_key", "test_value")
        value = config.get("test_key")
        assert value == "test_value", f"Expected 'test_value', got {value}"

        print("✓ ConfigManager basic functionality works")

        # Clean up
        temp_dir.joinpath("config.yaml").unlink(missing_ok=True)
        temp_dir.rmdir()

    except Exception as e:
        print(f"✗ ConfigManager test failed: {e}")
        return False

    return True

def test_index_parser_basic():
    """Test IndexParser basic functionality."""
    print("Testing IndexParser...")

    try:
        from agents_collector.parser.index_parser import IndexParser, IndexEntry
        import tempfile
        import yaml

        parser = IndexParser()

        # Create test data
        test_data = {
            "agents": [
                {
                    "name": "Root Guide",
                    "source": "AGENTS.md",
                    "target": "downloads/root.md"
                },
                {
                    "name": "API Guide",
                    "source": "services/api/AGENTS.md",
                    "target": "downloads/api.md"
                }
            ]
        }

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.safe_dump(test_data, f)
            temp_path = pathlib.Path(f.name)

        try:
            # Parse the file
            entries = parser.parse_index_file(temp_path)

            # Validate results
            assert len(entries) == 2, f"Expected 2 entries, got {len(entries)}"
            assert entries[0].name == "Root Guide"
            assert entries[1].name == "API Guide"

            print("✓ IndexParser basic functionality works")

        finally:
            # Clean up
            temp_path.unlink()

    except Exception as e:
        print(f"✗ IndexParser test failed: {e}")
        return False

    return True

def test_github_fetcher_basic():
    """Test GitHubFetcher basic functionality."""
    print("Testing GitHubFetcher...")

    try:
        from agents_collector.fetcher.github_fetcher import GitHubFetcher

        fetcher = GitHubFetcher()

        # Test URL parsing
        owner, repo, branch = fetcher.parse_github_url("https://github.com/octocat/hello-world")
        assert owner == "octocat", f"Expected 'octocat', got {owner}"
        assert repo == "hello-world", f"Expected 'hello-world', got {repo}"

        # Test URL building
        raw_url = fetcher.build_raw_url("https://github.com/octocat/hello-world", "README.md", "main")
        expected_url = "https://raw.githubusercontent.com/octocat/hello-world/main/README.md"
        assert raw_url == expected_url, f"Expected {expected_url}, got {raw_url}"

        print("✓ GitHubFetcher basic functionality works")

    except Exception as e:
        print(f"✗ GitHubFetcher test failed: {e}")
        return False

    return True

def test_modular_imports():
    """Test that all modules can be imported independently."""
    print("Testing modular imports...")

    tests = [
        ("agents_collector.config", "ConfigManager"),
        ("agents_collector.parser", "IndexParser"),
        ("agents_collector.fetcher", "GitHubFetcher"),
    ]

    for module, class_name in tests:
        try:
            module_obj = __import__(module, fromlist=[class_name])
            getattr(module_obj, class_name)
            print(f"✓ Successfully imported {class_name} from {module}")
        except ImportError as e:
            print(f"✗ Failed to import {class_name} from {module}: {e}")
            return False
        except AttributeError as e:
            print(f"✗ {class_name} not found in {module}: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error importing {class_name} from {module}: {e}")
            return False

    return True

def main():
    """Run all validation tests."""
    print("🚀 agent-fetch - Core Validation")
    print("=" * 50)

    tests = [
        test_modular_imports,
        test_config_manager_basic,
        test_github_fetcher_basic,
        test_index_parser_basic,
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        try:
            if test_func():
                passed += 1
            print()
        except Exception as e:
            print(f"✗ Test {test_func.__name__} crashed: {e}")
            print()

    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All core functionality validation passed!")
        print("\nThe agent-fetch modular design is sound and ready for use.")
        print("To get started:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Install package: pip install -e .")
        print("3. Run: agentscli --help")
        return 0
    else:
        print(f"⚠️ {total - passed} test(s) failed. Check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
