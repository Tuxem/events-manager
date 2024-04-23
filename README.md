# events-manager

## Database initialisation

```
# Go inside the app container
docker exec -it events-manager-web-1 /bin/bash

# init database
flask db init
flask db migrate
flask db upgrade
```