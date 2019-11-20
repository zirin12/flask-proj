#!/bin/bash
 celery -A app.workerA.celery_app worker --loglevel=info -Q workerA