set -o errexist

pip install -r requirements.txt

python manage.py collect static --noinput

python manage.py migrate