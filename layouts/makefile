all: alert_ui.py credits_ui.py quit_ui.py ra_cal_ui.py dec_cal_ui.py obs_ui.py threepio_ui.py

%_ui.py: %.ui
	source ../venv/bin/activate; \
	pyuic5 -o $@ $<

clean:
	rm *_ui.py
