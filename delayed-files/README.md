# Description
In this scenario files are added periodically on the active nodes. The time periods between the files are randomly, but every time the same per node.

# prepare
Nothing to do here.

# initiate
Starts the SimpleRhizomeAdder.py script on every active node.

### Usage
```
(t <sec> | f <num>) (f1 | f2 | f3)
```
With the `t` parameter, files will be added for `<sec>` seconds. With `f` only `<num>` files will be added.

With `f1` files with a size 250kB will be added, with `f2` with 5MB and with `f3` with 50MB.

# watch-agent
Watches for a specific time or for a specific number of files.

### Usage
```
(t <sec> | f <num>)
```
With the `t` parameter, finishes watching after `<sec>` seconds. With `f` after receiving `<num>` files.

---

**NOTE:** The `t` parameters has to be set seperately per script and a bit longer on watch-agent, to ensure waiting long enough to get all files.
**NOTE:** <num> have to be the same in both scripts.

# Example
```
./scenario core delayed-files/ "" "t 10" "t 5 f2" 0
```
With this call, the watch-agent will wait 10 seconds, while the initiate script will send files for 5 seconds on node 0 from the test-set 2.

```
./scenario core delayed-files/ "" "f 2" "f 2 f1" -a
```
With this call, the watch-agent will wait until 2 files from every active node arrives, while every active node will send 2 files. Here, every node is active.