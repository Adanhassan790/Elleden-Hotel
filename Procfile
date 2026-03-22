web: cd backend && gunicorn elleden.wsgi --log-file -
release: cd backend && python manage.py migrate && python manage.py collectstatic --noinput --clear && mkdir -p staticfiles && cp -r static/* staticfiles/
