import logging
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPException
from typing import Optional, Type
from types import TracebackType
from config.ldap_config import LDAPConfig
from core.models import UserRegistration, UserEditor, UserGetion

logger = logging.getLogger(__name__)


class LDAPService:
    def __init__(self, config: LDAPConfig):
        self.config = config
        self.connection: Optional[Connection] = None

    def __enter__(self):
        try:
            server = Server(self.config.LDAP_SERVER_URL, get_info=ALL)

            self.connection = Connection(
                server,
                user=self.config.get_admin_login(),
                password=self.config.get_admin_password(),
                auto_bind=True
            )
            return self
        except LDAPException as e:
            logger.error(f"Connection error: {e}")
            raise

    def __exit__(self,
                 exception_type: Optional[Type[BaseException]],
                 exception_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        if self.connection:
            if not self.connection.closed:
                self.connection.unbind()

        return exception_type is None

    def get_user_dn(self, login, cn):
        """Возвращает user_dn по логину, если пользователь не найден, возвращает False"""
        if not self.connection or self.connection.closed:
            raise RuntimeError("LDAP connection is not established")
        try:
            self.connection.search(
                search_filter=login,
                search_base=cn,
                attributes=['*'],
            )
            user_dn = self.connection.entries[0].entry_dn
            if len(self.connection.entries) != 0:
                logger.info(f"Successfully search user: {user_dn}")
                return user_dn
            else:
                return False

        except LDAPException as e:
            logger.error(f"LDAP error: {e}")
            return False

    def reg_user(self, user:UserRegistration):
        """Создает пользователя LDAP"""
        if not self.connection or self.connection.closed:
            raise RuntimeError("LDAP connection is not established")

        try:
            attributes = user.model_dump()
            self.connection.add(
                dn=user.dn,
                object_class=["top", "person", "organizationalPerson", "user"],
                attributes=attributes
            )
            logger.info(f"Successfully create user: {user.sAMAccountName}")
            return True

        except LDAPException as e:
            logger.error(f"LDAP error: {e}")
            return False

    def change_mode(self, user):
        """Изменяет пользователя LDAP"""
        if not self.connection or self.connection.closed:
            raise RuntimeError("LDAP connection is not established")

        try:
            self.connection.modify(user.dn, {'userAccountControl': [(MODIFY_REPLACE, [66048])]})
            logger.info(f"Successfully change mode for user {user.sAMAccountName}")
            return True

        except LDAPException as e:
            logger.error(f"LDAP error: {e}")
            return False

    def update_user(self, UserEditor):
        pass


    def password_update(self, user):
        """Обновляет пароль пользователя"""
        if not self.connection or self.connection.closed:
            raise RuntimeError("LDAP connection is not established")

        try:
            self.connection.modify(user.dn, {'unicodePwd': [(MODIFY_REPLACE, [user.unicodePwd])]})
            logger.info(f"Successfully password update for user {user.sAMAccountName}")
            return True

        except LDAPException as e:
            logger.error(f"LDAP error: {e}")
            return False

    def move(self, user):
        """Перемещает пользователя"""
        pass

    def get_user(self, user: UserGetion):
        """Возвращает объект user по логину, если пользователь не найден, возвращает False"""
        if not self.connection or self.connection.closed:
            raise RuntimeError("LDAP connection is not established")
        try:
            self.connection.search(
                search_filter=f'(sAMAccountName = {user.sAMAccountName})',
                search_base=user.dn,
                attributes=['*'],
            )
            user = self.connection.entries[0]
            if len(self.connection.entries) != 0:
                logger.info(f"Successfully search user: {user}")
                return user
            else:
                return False

        except LDAPException as e:
            logger.error(f"LDAP error: {e}")
            return False
