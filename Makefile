push:
	git push && git push --tags

bumpversion:
	bumpversion $(bump)

# make release bump=minor  (major,minor,patch)
release: bumpversion push
