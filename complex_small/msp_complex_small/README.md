# Description
In this scenario a number of complex small calls via MSP to random SIDs are issued.

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
./scenario core msp_periodic_complex_small/ "" "60" "5" 1
```

5 RPCs are called. The watch-agent waits 60 seconds. Node 1 is active.
