blog:
	python yasbe.py

clean:
	rm -rf www

serve:
	python yasbe.py && cd www && python3 -m http.server 4000
