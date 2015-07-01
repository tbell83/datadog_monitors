datadog_monitors
================

Monitor definitions for Datadog

http://docs.datadoghq.com/api/#monitor

Modifying the monitor.yaml file will trigger the jenkins job to update datadog monitors via the API.

Monitor.YAML is the authoritative list of DD monitors, anything added via the web interface that does not exist in the YAML file will be removed at the next jenkins job run.
