clear:
	docker images | grep -E 'grafana|tempo' | awk '{print $3}' | xargs docker rmi -f
