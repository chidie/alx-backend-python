#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1), 
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        expected_key = path[0] if nested_map == {} else path[1]
        self.assertEqual(str(context.exception), repr(expected_key))


class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns expected result using a mocked requests.get"""

        with patch("utils.requests.get") as mock_get:
            # Create a mock response with a .json() method
            mock_response = Mock()
            mock_response.json.return_value = test_payload

            # requests.get() should return this mock response
            mock_get.return_value = mock_response

            # Call the function under test
            result = get_json(test_url)

            # Ensure requests.get was called exactly once with the right argument
            mock_get.assert_called_once_with(test_url)

            # Ensure get_json returned the correct payload
            self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
