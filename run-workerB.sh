#!/bin/bash
celery -A app.workerB.celery_app worker --loglevel=info -Q workerB