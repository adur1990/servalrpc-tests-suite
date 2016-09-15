# Description
In this scenario a number files is send from one end to all other nodes.

# prepare
Generates files which will be sent on initiate.
### Usage
```
<fileset> <num>
```
Generate `<fileset>` `<num>` times.
There are 4 different filesets available:

* f1 - small - 64K, 256K, 512K - 3 files total
* f2 - medium - 1M, 5M, 10M - 3 files total
* f3 - large - 25M, 50M, 100M - 3 files total
* f4 - all of the above - 9 files total

# initiate
Nothing to be done here.

# watch-agent
Watches for a number of files.

### Usage
```
<fileset> <num>
```
Waits, until `<num>` files of the `<fileset>`  arrived. Remember to calculate correctly, depending on the `fileset` and the multiplier!

# Example
```
./scenario core mass-inject-file/ "f1 5" "f1 5" "" 0
./scenario miniworld mass-inject-file "f4 5" "f4 5" "" 5
```

With the first call, 5 * 3 files of the file set f1 will be generated. The watch-agent waits until all 15 files arrive, while the files will be added on node 0.
With the second call, 5 * 9 files of the file set f4 will be generated. The watch-agent waits until all 95 files arrive, while the files woll be added on node 5.
