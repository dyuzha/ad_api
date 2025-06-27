curl -X POST "http://pgadmin.it4prof.ru:82/get_user_mail" \
     -H "Content-Type: application/json" \
     -d '{
           "login": "dyuzhev_mn",
           "ou": "OU=Пользователи,OU=Проф ИТ,OU=krd",
           "domain": "art-t.ru",
         }'


