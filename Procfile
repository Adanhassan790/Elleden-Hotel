web: cd backend && gunicorn elleden.wsgi --log-file -
release: cd backend && python manage.py migrate && python elleden/collectstatic_fallback.py
