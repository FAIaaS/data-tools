SBIN_DIR = "/usr/local/sbin"

install: install_wml install_anomalies_monitor install_switch_web-server

dist/eve_adps-0.0.1-py3-none-any.whl:
	python -m build

install_wml: dist/eve_adps-0.0.1-py3-none-any.whl
	pip install dist/eve_adps-0.0.1-py3-none-any.whl

install_anomalies_monitor: bin/anomalies_monitor.sh
	sudo cp bin/anomalies_monitor.sh $(SBIN_DIR)

install_switch_web-server: bin/switch_web-server.sh
	sudo cp bin/switch_web-server.sh $(SBIN_DIR)

