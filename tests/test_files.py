from src.file_operations import write_file
import pytest


@pytest.fixture
def temp_file(tmp_path):
    # Create a temporary file for testing
    filepath = tmp_path / "test_file.txt"
    return filepath

def test_write_file(temp_file):
    # Test data
    data = "Hello, world!"

    # Call the function
    write_file(temp_file, data)

    # Read the content from the file
    with open(temp_file, "r") as f:
        content = f.read()

    # Check if the content matches the expected data
    assert content == data

# You can add more test cases as needed
