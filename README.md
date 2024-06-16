# Django-CBV-DRF-Blog
 A blog app created by using Django CBVs which also includes APIs created by DRF

## Configurations
 - Customized user and profile
 - Up and running Celery & Redis Services
 - Customized logging
 - Customized caching based on Redis
 - smtp4dev development mailing service

### Project Setup
 create a .env file containing SECRET_KEY and DEBUG variables beside docker-compose file
 then run below commands:
 ```
 docker compose up
 docker compose exec backend sh -c "python manage.py makemigrations"
 docker compose exec backend sh -c "python manage.py migrate"
 ```
 This will set you up for using this project.

### Creating a super-user
```
docker compose exec backend sh -c "python manage.py createsuperuser"
```
By creating super-user you can login with the super-user credentials and also access the admin-panel.

### For running tests
```
docker compose exec backend sh -c "pytest ."
```
You test the functionality and performance of the project by using created tests and also adding your tests as well.
