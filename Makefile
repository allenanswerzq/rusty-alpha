all:
	python main.py -c third_party/rb-tree/rb.cpp -I third_party/rb-tree -o b.rs


test:
	pytest tests/test_slicer.py -s