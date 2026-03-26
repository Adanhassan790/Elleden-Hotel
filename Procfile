web: cd backend && gunicorn elleden.wsgi --log-file - --timeout 120 --workers 2 --worker-class sync --access-logfile - --error-logfile -
release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear || (echo "Migration or collectstatic failed" && exit 1)
