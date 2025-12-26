@echo off
celery -A sannap_project worker -l info --pool=solo
