PYTHON = python3.8 # just should be >= 3.7
TESTS = vm_tests

.PHONY: test

# run all tests
test: 
	@for exec in $(TESTS); do \
		$(PYTHON) -m tests.$$exec; \
	done \