.PHONY: clean
clean: clean-py clean-dist

.PHONY: clean-dist
clean-dist:
	rm -rf build dist webclip.egg-info

.PHONY: clean-py
clean-py:
	find -name __pycache__ | xargs rm -rf
