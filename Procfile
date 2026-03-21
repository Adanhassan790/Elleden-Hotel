web: cd backend && gunicorn elleden.wsgi --log-file -
release: cd backend && mkdir -p staticfiles && python manage.py migrate && python manage.py collectstatic --noinput --clear --verbosity 2
