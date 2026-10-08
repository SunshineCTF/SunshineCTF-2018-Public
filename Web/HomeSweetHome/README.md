# [Web] Home Sweet Home

## Deployment

$ docker build -t homesweethome .
$ docker run -d -p 4200:80 --name homesweethome homesweethome

## Maintenance

Kill the docker container, start it again, and message me so I can figure out what went wrong.

See [writeup.md](writeup.md) for the solution.
