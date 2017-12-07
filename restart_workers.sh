#!/bin/bash
pkill -9 -f "server_worker"
pkill -9 -f "run_execution_worker"
pkill -9 -f "runserver"
rm /at_em_imaging_workflow/logs/server.log
rm /at_em_imaging_workflow/logs/execution_worker.log
rm /at_em_imaging_workflow/logs/debug.log
DEBUG_LOG=logs/server.log python -m manage server_worker&
DEBUG_LOG=logs/execution_worker.log python -m manage run_execution_worker&
DEBUG_LOG=logs/debug.log python -m manage runserver 0.0.0.0:8000

