curl -X POST "http://localhost:82/get_user/mail" \
     -H "Content-Type: application/json" \
     -d '{
           "sAMAccountName": "dyuzhev_mn",
           "ou": "OU=krd",
           "domain": "art-t.ru"
         }'
