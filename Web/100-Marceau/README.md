# Marceau - 100pts

# Solution

The `Accept` header must be set to `text/php`:
```
$ curl http://<IP>:<PORT> -H 'Accept: text/php'
```

## Usage
```
$ docker build -t marceau . 
$ docker run -d --name -p 3333:80 marceau marceau
```


## Maintenance

None required, just restart or re-provision the Docker provision
