import logging
from typing import Optional
from transliterate import translit
from pydantic import BaseModel, EncodedStr, computed_field, Field

logger = logging.getLogger(__name__)


class UserRegistration(BaseModel):
    """Форма для регистрации нового пользователя"""
    givenName:str = Field(alias="name", description="Имя (RU)")
    sn: str = Field(alias="surname", description="Фамилия (RU)")
    optname: str = Field(exclude=True, description="Отчество (RU)")

    password: str = Field(alias="password", exclude=True, description="Пароль")
    ou: str = Field(exclude=True, description="OU из Active Directory (например: ou=krd,ou=Проф ИТ,ou=Пользователи)")
    domain: str = Field(exclude=True, description="Домен Active Directory (например: art-t.ru)")
    mobile: str = Field(description="Мобильный телефон (например: +7-123-456-7890)")

    mail_domain: str = Field(exclude=True, description="Почтовый домен (например: art-t.ru)")

    company: Optional[str] = Field(default=None, description="Компания")
    title: Optional[str] = Field(default=None, description="Должность")
    description: Optional[str] = Field(default=None, description="Описание в AD, зачастую это должность")
    department: Optional[str] = Field(default=None, description="Отдел")

    @computed_field(alias="login")
    def sAMAccountName(self) -> str:
        try:
            name_trans = translit(self.givenName, "ru", reversed=True)
            surname_trans = translit(self.sn, "ru", reversed=True)
            optname_trans = translit(self.optname, "ru", reversed=True)
            return f"{surname_trans.lower()}_{name_trans[:1].lower()}{optname_trans[:1].lower()}"
        except Exception as e:
            logger.error(f"Transliteration error: {e}")
            raise

    @computed_field
    def displayName(self) -> str:
        return f"{self.sn} {self.givenName} {self.optname}"

    @computed_field
    def userPrincipalName(self) -> str:
        return f"{self.sAMAccountName}@{self.domain}"

    @computed_field
    def mail(self) -> str:
        return f"{self.sAMAccountName}@{self.mail_domain}"

    @property
    def cn(self):
        return f"CN={self.displayName}"

    @property
    def dc(self):
        parts = [part for part in self.domain.split('.') if part]
        return "".join(f",dc={part.lower()}" for part in parts)[1:]

    @property
    def dn(self):
        return f"{self.cn},{self.ou},{self.dc}"

    @property
    def unicodePwd(self):
        # Пароль должен быть заключен в ковычки, также в кодировке utf-16-le,
        # Также должно быть активно TLS/SSL соединение
        logger.info(f"\"{self.password}\"".encode('utf-16-le'))
        return f"\"{self.password}\"".encode('utf-16-le')


class UserEditor(BaseModel):
    """Форма для редактирования пользователя """
    sAMAccountName: str = Field(alias="login", description="Логин (например: login_ad)")


class UserToTrash(BaseModel):
    pass

class UserGetion(BaseModel):
    pass
