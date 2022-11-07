# Import data from HPC to Clowder

TODO: 
* Use Docker image `clowder/uploader` for bulk upload (Warning: files uploaded this way are managed by user, not Clowder aka can't be deleted by GUI.)

* Use `kubectl apply -f job.yaml` to launch.

```bash
# job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      # todo: this seems like the wrong container, use clowder/uploader.
      - name: pi
        image: perl:5.34.0
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
```

```bash
# usage
kubectl apply -f https://kubernetes.io/examples/controllers/job.yaml

# view results
pods=$(kubectl get pods --selector=job-name=pi --output=jsonpath='{.items[*].metadata.name}')
echo $pods
kubectl logs $pods
```

## Unknowns

* 2FA auth on HPC end.
* Progress monitoring.
* Error handling with minimal user interaction.