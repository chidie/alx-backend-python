#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch("client.get_json")   # patch where it is imported, not where defined
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""

        expected_payload = {"org": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

class TestGithubOrgClient1(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct value"""

        expected_url = "http://example.com/repos"

        # Patch GithubOrgClient.org as a *property* using PropertyMock
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value={"repos_url": expected_url}
        ):
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            print("Result: ", result)
            print("Expected URL: ", expected_url)
            # self.assertEqual(result, expected_url)
            self.assertAlmostEqual(result, expected_url)

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        expected = {"payload": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected)

    def test_public_repos_url(self):
        """Test the _public_repos_url property"""
        expected_url = "http://example.com/repos"

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value={"repos_url": expected_url}
        ):
            client = GithubOrgClient("testorg")
            result = client._public_repos_url

        self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = payload

        fake_url = "http://example.com/repos"

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value=fake_url
        ) as mock_repos_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()

        expected = ["repo1", "repo2", "repo3"]

        self.assertEqual(result, expected)
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(fake_url)



if __name__ == "__main__":
    unittest.main()


