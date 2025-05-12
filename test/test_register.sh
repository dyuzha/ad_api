curl -X POST "http://localhost:82/register" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Андрей",
           "surname": "Андреев",
           "optname": "Андреевич",
           "password": "Change_me_123",
           "mail_domain": "it4prof.ru",
           "domain": "art-t.ru",
           "ou": "OU=Пользователи,OU=Проф ИТ,OU=krd",
           "title": "Title",
           "company": "Проф ИТ",
           "mobile": "+7-981-402-77-88",
           "description": "Descr",
           "department": "Depart"
         }'


