First build the image:
```
docker build -t bentham/posgres:latest .
```

Then run the image with host portmapping

```
docker run --net=host bentham/postgres
```

include ```-d``` option if you wish to run as a daemon
