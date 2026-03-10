"""Pytest configuration and shared fixtures."""
import os

os.environ.setdefault(
	"SECRET_KEY",
	"test-secret-key-for-pytest-with-at-least-32-bytes",
)
os.environ.setdefault("ALGORITHM", "HS256")
