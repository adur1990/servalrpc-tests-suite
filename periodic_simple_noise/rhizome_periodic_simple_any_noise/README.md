# Description
In this scenario a number of simple noise calls via Rhizome to any are issued.

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
./scenario core Rhizome_periodic_simple_any_noise/ "" "60" "5" 1
```

5 RPCs are called. The watch-agent waits 60 seconds. Node 1 is active.
