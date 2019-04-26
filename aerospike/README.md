# aerospike-scripts
Scripts for monitoring and manage aerospike clusters
# as_sets_stat.py 
Script for parse 'show stats' output for all version (after it you can send metrics to graphite)

Sample output:
```
ae.<ns>.<set> <objects>
```

Sample output for graphite:
```
graphite_prefix.ae.ns_n1.set_n1 261812
graphite_prefix.ae.ns_n1.set_n2 96481
graphite_prefix.ae.ns_n1.set_n3 26181266

graphite_prefix.ae.ns_n2.set_n11 34261
graphite_prefix.ae.ns_n2.set_n21 261
...
```

Dashboard example

![ns_sets](aerospike/img/ns_sets.png)

***
