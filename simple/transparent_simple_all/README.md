# Description
In this scenario a number of simple calls transparently to all are issued.

# prepare
Nothing to be done here.

# initiate
Call `<num>` procedures over a time period.

# watch-agent
Watches `<time>` seconds.

### Usage
```
<time>
```

# Example
```
./scenario core transparent_periodic_simple_all/ "" "60" "5" 1
```

5 RPCs are called. The watch-agent waits 60 seconds. Node 1 is active.
