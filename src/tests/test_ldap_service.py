import pytest
from unittest.mock import patch, MagicMock
from ad_api.services.ldap_service import LDAPService
from ldap3.core.exceptions import LDAPException


class DummyConfig:
    LDAP_SERVER_URL = "ldap://test"

    def get_admin_login(self):
        return "cn=admin,dc=example,dc=com"

    def get_admin_password(self):
        return "password"


class DummyUser:
    sAMAccountName = "jdoe"
    dn = "dc=example,dc=com"


@pytest.fixture
def ldap_config():
    return DummyConfig()


def test_successful_connection(ldap_config):
    with patch("ad_api.services.ldap_service.Server") as mock_server, \
         patch("ad_api.services.ldap_service.Connection") as mock_conn:
        instance = mock_conn.return_value
        service = LDAPService(ldap_config)

        with service as s:
            assert s.connection is instance
            mock_conn.assert_called_once_with(
                mock_server.return_value,
                user=ldap_config.get_admin_login(),
                password=ldap_config.get_admin_password(),
                auto_bind=True
            )


def test_connection_error(ldap_config):
    with patch("ad_api.services.ldap_service.Connection", side_effect=LDAPException("fail")):
        service = LDAPService(ldap_config)
        with pytest.raises(LDAPException):
            with service:
                pass


def test_get_user_info_success(ldap_config):
    user = DummyUser()

    fake_entry = MagicMock()
    fake_entry.mail.value = "jdoe@example.com"
    fake_entry.displayName.value = "John Doe"

    conn = MagicMock()
    conn.closed = False
    conn.entries = [fake_entry]

    with patch("ad_api.services.ldap_service.Connection") as mock_conn, \
         patch("ad_api.services.ldap_service.Server"):
        mock_conn.return_value = conn

        with LDAPService(ldap_config) as service:
            service.connection = conn
            result = service.get_user_info(user, "mail", "displayName")

            assert result == {
                "mail": "jdoe@example.com",
                "displayName": "John Doe",
                "login": "jdoe"
            }


def test_get_user_info_not_found(ldap_config):
    user = DummyUser()

    conn = MagicMock()
    conn.closed = False
    conn.entries = []

    with patch("ad_api.services.ldap_service.Connection") as mock_conn, \
         patch("ad_api.services.ldap_service.Server"):
        mock_conn.return_value = conn

        with LDAPService(ldap_config) as service:
            service.connection = conn
            result = service.get_user_info(user, "mail")
            assert result is None


def test_get_user_info_ldap_error(ldap_config):
    user = DummyUser()

    conn = MagicMock()
    conn.closed = False
    conn.search.side_effect = LDAPException("Some error")

    with patch("ad_api.services.ldap_service.Connection") as mock_conn, \
         patch("ad_api.services.ldap_service.Server"):
        mock_conn.return_value = conn

        with LDAPService(ldap_config) as service:
            service.connection = conn
            result = service.get_user_info(user, "mail")
            assert result is False


def test_exit_unbinds_connection(ldap_config):
    conn = MagicMock()
    conn.closed = False

    with patch("ad_api.services.ldap_service.Connection") as mock_conn, \
         patch("ad_api.services.ldap_service.Server"):
        mock_conn.return_value = conn

        service = LDAPService(ldap_config)
        with service:
            pass

        conn.unbind.assert_called_once()
