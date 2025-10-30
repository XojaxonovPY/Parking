from invoke import task

@task
def mig(c):
    c.run("python manage.py makemigrations")

@task
def upg(c):
    c.run("python manage.py migrate")

@task
def admin(c):
    c.run("python manage.py createsuperuser")

@task
def apps(c):
    c.run("python manage.py startapp auth_user")


@task
def celery(c):
    c.run("celery -A root worker --pool=solo -l info")


@task
def flower(c):
    c.run("celery -A root flower")


@task
def beat(c):
    c.run("celery -A root beat -l info -S django")
