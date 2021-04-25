PYTHON = python3.8 # just should be >= 3.7
TESTS = vm_tests \
	compiler_tests \
	parser_tests \
	rasm_parser_tests

.PHONY: test

# run all tests
test: 
	@for exec in $(TESTS); do \
		echo "Running $$exec"; \
		$(PYTHON) -m tests.$$exec; \
	done \

repl:
	$(PYTHON) -m scripts.repl