## Datadog Monitors

### Overview
Easily create [Datadog](http://www.datadoghq.com) monitors to monitor application and service health.

Commits to this repository will trigger a [Jenkins job](http://jenkins-docker.svc.csh/job/Datadog%20Monitors) that automatically deploys monitors via the [Datadog API](http://docs.datadoghq.com/api/#monitor).

### Creating new monitors
The [monitor.yaml](https://github-enterprise.colo.lair/Operations/datadog_monitors/blob/master/monitors.yaml) file located in this repository is the authoritative list of all Datadog monitors. Any monitors added via the web interface that are not present in this file will be deleted by the Jenkins run.
