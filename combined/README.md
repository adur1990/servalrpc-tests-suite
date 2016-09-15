# Description
Runs all scenarios at once.

# prepare
Nothing to do here.

# initiate
Initiates all scenarios. For more information see the README of the respective scenario.

### Usage
```
<timeout> (f1 | f2 | f3 | f4)
```

# watch-agent
Waits, unitl all scenarios are finished. For the sake of convenience, this script wait's only for a timeout.

### Usage
```
<timeout>
```

---

**NOTE:** The `<timeout>` for the watch-agent should be a lot higher than the timeout in initiate, since the delayed files and mass injects can be very long.
