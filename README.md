<div align="center">

# Session 11

</div>

In this session, we build a docker image that contains a FastAPI backend to run a prediction via the CLIP model against a string (which is a list of classes) and an image. This image is deployed to ECS using AWS Copilot (not to be confused with Github Copilot) using 5 tasks (behind a load balancer). Functional testing is done via the FastAPI docs and stress testing is done via Locust. A simple frontend in Next.js runs a prediction against the deployed service.



## Local Demo
To run locally, execute
```
uvicorn hw:app --host=0.0.0.0 --port=8080 
```

We can package this into a docker image via

```
docker build -t emlo:s11 .
```
Note that to reduce initial start time, the CLIP model and preprocessor is cached inside the Docker image.

Then run via

```
docker run -it --rm -p 80:80  emlo:s11
```


## Stress Testing

To run a stress test, we use locaust via:

```
locust -f locust_test.py
```

Open `http://127.0.0.1:8089/`.


## Pushing to ECR
The image is then pushed to ECR

## ECS and Copilot

Copilot can create all necessary resources like custom VPC, IAM roles, etc. for deploying an applicaiton to ECS.  
To launch the cluster, we can follow these steps. Make sure that copilot CLI is installed.

```bash
copilot init --app emlo-s11 --name emlo-s11-svc --image {INSERT_IMAGE_URI_HERE} --port 80  --type  "Load Balanced Web Service" --port 80 
```

Inside the `../emlo-s11-svc/manifests.yaml` file (created by the above command), make changes to the CPU/Memory and healthcheck path.

Then run

```bash
copilot env init --name staging --default-config --profile {LOCAL_AWS_PROFILE}
copilot env deploy --name staging
copilot svc deploy --name emlo-s11-svc --env staging
```

To see the status, run

```bash
copilot svc show --name emlo-s11-svc
```

In order to change the cluster's properties, simply edit the yaml file mentioned above and re-run the `copilot svc deploy` command.
