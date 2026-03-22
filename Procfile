web: cd backend && gunicorn elleden.wsgi --log-file -
release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear || (echo "Migration or collectstatic failed" && exit 1)
