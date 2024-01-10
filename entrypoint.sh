# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

python manage.py makemigrations main --noinput
python manage.py migrate main --noinput
python manage.py collectstatic --noinput
python manage.py test
gunicorn config.wsgi:application --bind 0.0.0.0:8000