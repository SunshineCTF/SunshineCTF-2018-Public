# [Web] Evaluation

## Deployment

$ docker build -t evaluation .
$ docker run -d -p 4202:80 --name evaluation evaluation

## Maintenance

Kill the docker container, start it again, and message me so I can figure out what went wrong.

See [writeup.md](writeup.md) for the solution.
