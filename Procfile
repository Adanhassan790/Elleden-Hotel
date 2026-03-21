web: cd backend && gunicorn elleden.wsgi --log-file -
release: cd backend && python manage.py migrate && python manage.py collectstatic --noinput --clear 2>&1 || true; if [ ! -d staticfiles/css ]; then cp -r static/* staticfiles/ 2>/dev/null || true; fi
