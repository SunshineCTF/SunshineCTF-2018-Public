# [Web 50] Home Sweet Home

## Solution

Just set X-Fowarded-For to 127.0.0.1

## Deployment

$ docker build -t homesweethome .
$ docker run -d -p 4200:80 --name homesweethome homesweethome

## Maintenance

Kill the docker container, start it again, and message me so I can figure out what went wrong.