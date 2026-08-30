# Distributed Taxi Trip Analytics — Big Data Essentials Assignment

**Author:** UWIMPUHWE Erneste (Student ID: 101414)
**Course:** Bigdata Essentials — AUCA MSc in Big Data Analytics
**Instructor:** Dr. Kundan Kumar

## Overview

This project implements a distributed analytics pipeline for NYC TLC Yellow Taxi
trip data (January–March 2026, \~11 million raw records) using Apache Hadoop,
HDFS, and Python MapReduce via Hadoop Streaming. It includes nine required
analyses (hourly demand, daily demand, pickup location, revenue by location,
payment method, distance-based fare, routes, trip duration, anomaly detection),
a compulsory two-stage MapReduce pipeline (revenue by zone → top 10
highest-revenue zones), and a performance comparison against Python/Pandas.

## Environment

* **OS:** Windows 11
* **Hadoop:** 3.2.4, running natively on Windows (via `winutils.exe`), in
pseudo-distributed (single-node) mode 
* **Python:** 3.13 (Windows native install)
* **Java:** OpenJDK 1.8.0\_202
* **Key Python packages:** pandas, pyarrow (for the local Parquet→CSV cleaning
step only — the mappers/reducers themselves use only the Python standard
library, so no packages need to be installed inside Hadoop's task
environment)

## Prerequisites / Installation Assumptions

1. Hadoop 3.2.4 installed at `C:\\hadoop`, with `HADOOP\_HOME` set to `C:\\hadoop`
in **both** User and System environment variables (Windows allows both to
exist; the User-level value takes precedence, so make sure they match).
2. `winutils.exe` present at `C:\\hadoop\\bin\\winutils.exe`.
3. Java 8 installed, `JAVA\_HOME` set accordingly.
4. Python 3.13 installed and on PATH; `pip install pandas pyarrow psutil`.
5. The following non-default XML configuration is required (defaults ship
empty and will NOT run jobs on YARN):

   * `mapred-site.xml`: `mapreduce.framework.name=yarn`
   * `yarn-site.xml`: `yarn.nodemanager.aux-services=mapreduce\_shuffle`,
the shuffle handler class, disk health-checker thresholds appropriate
to available local disk space, and an `env-whitelist` that includes
`HADOOP\_HOME` (not included by default — without it, task containers
cannot locate Hadoop and every mapper fails with
`HADOOP\_HOME and hadoop.home.dir are unset`).

See `commands.txt` for the exact commands used to set up HDFS and run every
job in this project.

## Project Structure

```
taxi\_project/
├── raw\_parquet/              # original TLC Parquet files (3 months)
├── cleaned/                  # cleaned CSVs + cleaning\_summary.csv
├── output\_local/             # downloaded copies of HDFS job outputs
├── mappers/                  # all 10 mapper scripts
├── reducers/                 # all 10 reducer scripts
├── clean\_and\_convert.py      # Parquet -> cleaned CSV conversion script
├── performance\_comparison.py # Pandas benchmark (Section 12)
├── extract\_top\_bottom\_locations.py  # ranks location-analysis output
├── extract\_top\_routes.py     # ranks route-analysis output by count \& revenue
├── commands.txt              # every HDFS/Hadoop command used, in order
└── README.md                 # this file
```

## How to Reproduce

1. **Clean and convert data:** edit `INPUT\_DIR`/`OUTPUT\_DIR` in
`clean\_and\_convert.py` to your local paths, then run it. Produces 3
cleaned CSVs plus a `cleaning\_summary.csv`.
2. **Start Hadoop:** `start-dfs.cmd` then `start-yarn.cmd`; confirm with
`jps` that NameNode, DataNode, ResourceManager, and NodeManager are all
running.
3. **Create HDFS structure and upload data:** see `commands.txt` Section 1.
4. **Run each MapReduce job:** see `commands.txt` Section 2 — one
`hadoop jar ... -files ... -mapper ... -reducer ...` command per
analysis. Each job's `-input`/`-output` paths and mapper/reducer
filenames are listed there.
5. **Run the multi-stage pipeline:** Job 1 (revenue by zone) must complete
before Job 2 (top 10 by revenue) is submitted, since Job 2's `-input`
is Job 1's HDFS `-output` directory.
6. **View results:** `hdfs dfs -cat /taxi\_project/output/<job>/part-00000`
for each job.
7. **Run the performance comparison:** `python performance\_comparison.py`
(requires `psutil`).

## Notes on Design Decisions

* **Fixed column indices in mappers, not header parsing:** cleaned CSVs are
split into multiple Hadoop InputSplits per file (each \~300–400 MB against
a 128 MB default block size), and only the split starting at byte 0 of a
file contains the header row. Every mapper therefore uses pre-verified,
fixed column positions rather than reading a header per task.
* **Full Python path in `-mapper`/`-reducer` commands:** Hadoop Streaming
task containers on Windows do not reliably inherit the full system PATH,
so `python` alone is not found; commands use the full path via the 8.3
short-path form (e.g. `C:\\Progra\~1\\Python313\\python.exe`) to avoid
quoting issues with the space in `Program Files`.

## Known Limitations

See Section 14 ("Limitations") of the final report for a full discussion —
in summary: single-node cluster (no true multi-node scalability tested),
Windows-specific Hadoop configuration quirks, anomaly thresholds set by
domain judgment rather than statistical derivation, and location IDs not
joined against a human-readable zone-name lookup table.

