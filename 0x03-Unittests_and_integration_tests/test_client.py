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


class TestGithubOrgClient(unittest.TestCase):
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

            self.assertEqual(result, expected_url)


if __name__ == "__main__":
    unittest.main()


