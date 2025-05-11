import logging
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPException
from typing import Optional, Type
from types import TracebackType
from config.ldap_config import LDAPConfig
from core.models import UserRegistration, UserGetion

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

    # def get_user(self, user: UserGetion):
    #     if not self.connection or self.connection.closed:
    #         raise RuntimeError("LDAP connection is not established")
    #     try:
    #         self.connection.search(
    #             search_filter=f'(sAMAccountName={user.sAMAccountName})',
    #             search_base=user.dn,
    #             attributes=['mail, sAMAccountName'],
    #         )
    #
    #         if len(self.connection.entries) != 0:
    #             finded_user = self.connection.entries[0]
    #             logger.info(f"Successfully search user: {user.sAMAccountName}")
    #             return finded_user
    #         else:
    #             logger.info(f"Successfully search user: {user.sAMAccountName}")
    #             return None
    #
    #     except LDAPException as e:
    #         logger.error(f"LDAP error: {e}")
    #         return False


    def get_user(self, user: UserGetion, *attributes):
        """
        Выполняет поиск пользователя по логину (sAMAccountName)
        Возвращает словарь:
            {"login": ..., "attr1": "val1", "attr2": "val2", ..., "attrN": "valN"}
        Если пользователь не найден, возвращает None
        В случае ошибки возвращает False
        """

        if not self.connection or self.connection.closed:
            raise RuntimeError("LDAP connection is not established")
        try:
            self.connection.search(
                search_filter=f'(sAMAccountName={user.sAMAccountName})',
                search_base=user.dn,
                attributes=["mail"]
            )

            if not self.connection.entries:
                logger.info("User not found")
                return None

            finded_user = self.connection.entries[0]
            logger.info("Successfully found user")

            user_data = {
                "login": user.sAMAccountName,
                "mail": finded_user.mail.value if hasattr(finded_user, 'mail') else None
            }
            logger.info(f"Founded user: {user_data}")
            return user_data

        except LDAPException as e:
            logger.error(f"LDAP error: {e}")
            return False

        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")
            return False


    def get_test_user(self):
        if not self.connection or self.connection.closed:
            raise RuntimeError("LDAP connection is not established")
        try:
            self.connection.search(
                search_filter='(sAMAccountName=dyuzhev_mn)',
                search_base='dc=art-t,dc=ru',
                attributes=['mail', 'sAMAccountName']
            )

            if not self.connection.entries:
                logger.info("User not found")
                return None

            finded_user = self.connection.entries[0]
            logger.info("Successfully found user")

            user_data = {
                "login": finded_user.sAMAccountName.value,
                "mail": finded_user.mail.value if hasattr(finded_user, 'mail') else None
            }
            logger.info(f"Founded user: {user_data}")
            return user_data

        except LDAPException as e:
            logger.error(f"LDAP error: {e}")
            return False

        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")
            return False
