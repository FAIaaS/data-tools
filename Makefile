SBIN_DIR = "/usr/local/sbin"

install: install_wml install_anomalies_monitor install_switch_web-server

dist/eve_adps-0.0.1-py3-none-any.whl:
	python -m build

install_wml: dist/eve_adps-0.0.1-py3-none-any.whl
	pip install dist/eve_adps-0.0.1-py3-none-any.whl

install_anomalies_monitor: anomalies_monitor.sh
	cp anomalies_monitor.sh $(SBIN_DIR)

install_switch_web-server: switch_web-server.sh
	cp switch_web-server.sh $(SBIN_DIR)

