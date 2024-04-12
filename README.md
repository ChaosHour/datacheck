# datacheck

## What is data-check.py?

data-check.py is a wrappper script for [data-diff](https://github.com/datafold/data-diff) to compare data between two databases and tables.

## Why did I write this script?

I wrote this script to automate the process of comparing data between two databases and tables from multiple servers synchronously. I will come back to this script to add more features and make it more user-friendly. The goal is to be able to do this without using zsh or bash as a wrapper on top.


## Requirements:

- Docker 
- data-diff is included in docker image
- Python 3.10 and above will work


Build the image first

```bash
docker build -t data-diff:latest -f Dockerfile.data-diff .
```

The python script starts the container to run data-diff.

## How to use this script? Usage

```python

This script will read from your ~/.my.cnf to get the user and password. You need configparser.
Check the requirements.txt file.  

I use pipenv and pyenv to manage my python environment. Others use Poetry or pip.


./data-check.py
usage: data-check.py [-h] -s SOURCE_SERVER -d DEST_SERVER -db DEST_DB -t TABLE -k PRIMARY_KEY
data-check.py: error: the following arguments are required: -s/--source_server, -d/--dest_server, -db/--dest_db, -t/--table, -k/--primary_key
```

## Example Usage

```bash
typeset -A servers=(
    ["server1.com"]="db1"
    ["server2.com"]="db2"
    ["server3.com"]="db3"
    ["server4.com"]="db4"
)
table="my-table"
for key val in "${(@kv)servers}"; do
    echo "Source server: ${key}, Database: ${val}, Table: ${table}"
    ./data-check.py -s ${key} -d dest-node.com -db ${val} -t ${table} -k id
    sleep 1
done
Source server: server1.com, Database: db1, Table: my-table
- 39976
Source server: server2.com, Database: db2, Table: my-table
Source server: server3.com, Database: db3, Table: my-table
- 9525
- 9526
- 9527
- 9528
- 9529
- 9530
- 9531
- 9532
- 9533
- 9534
- 9535
- 9536
- 9537
- 9540
- 9541
- 9545
- 9546
- 9547
- 9548
- 9549
- 9550
- 9551
- 9552
- 9553
Source server: server4.com, Database: db4, Table: my-table
 
 
 
To sync your data:
mysqldump --skip-opt --single-transaction -t -n --replace --hex-blob --quick --extended-insert db3 my-table --where="id IN (9525, 9526, 9527, 9528, 9529, 9530, 9531, 9532, 9533, 9534, 9535, 9536, 9537, 9540, 9541, 9545, 9546, 9547, 9548, 9549, 9550, 9551, 9552, 9553)" > $(hostname)-diffs-db3-my-table-$(date +%F).sql
 
mysqldump --skip-opt --single-transaction -t -n --replace --hex-blob --quick --extended-insert db1 my-table --where="id IN (39976)" > $(hostname)-diffs-db1-my-table-$(date +%F).sql
 
 


Sync the data:
for i in $(ls -1 *-2024-01*.sql); do db=$(echo $i | awk -F'-' '{print $(NF-3)}'); echo "Current file is ${i} and database ${db}"; cat ${i} | mysql ${db} ; sleep 1; done


In a second Terminal:
mysqladmin proc -i1 | grep -i insert
```

## How to run data-diff against a single database and table?

```bash
docker run -it data-diff mysql://checkuser:xxxxx@mysql56-docker-primary-1:3306/db1 my-table1 mysql://checkuser:xxxxx@mysql56-docker-replica-1:3306/db2 my-table2

- 3021
- 3031
- 3041
- 3611
```


