FROM registry.gitlab.com/kimvanwyk/python2-poetry-container

# /app is the workdir. Copy files to execute to /app/
COPY app /app

WORKDIR /app/lions_md
CMD ["0.0.0.0:9000"]
ENTRYPOINT ["python", "-u", "manage.py", "runserver"]
