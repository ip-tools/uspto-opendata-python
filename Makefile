push:
	git push && git push --tags

bumpversion:
	bumpversion $(bump)

# make release bump=minor  (major,minor,patch)
release: bumpversion push


mkvar:
	mkdir -p var/lib

redis-start: mkvar
	echo 'dir ./var/lib' | redis-server -

celery-start: mkvar
	@# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#starting-the-scheduler
	celery worker --app uspto --beat --schedule-filename var/lib/celerybeat-schedule --loglevel=info
