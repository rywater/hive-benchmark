#!/bin/bash
set -e

GEN_BASE_DATA=true
GEN_DELTA_DATA=true
ROWS=45000000
COLUMNS=12
COLUMN_DELTA=1
COLUMN_SIZE=8
UPDATE_DELTA=.2
PARTITIONS=10
# UPDATE ROWS = ROWS * DELTA
UPDATE_ROWS=$(awk "BEGIN { pc=${ROWS} * ${UPDATE_DELTA}; i=int(pc); print (pc - i < 0.5)?i:i+1}")

BASE_DATA=base_data
UPDATE_DATA=update_data

BASE_TABLE=obs
UPDATE_TABLE=obs_update
MERGE_TABLE=merge_result
MERGE_TABLE_TYPE=ORC
MERGE_TABLE_CLUSTER_COLUMN=rowid
MERGE_BUCKETS=50
MERGE_BUCKET_STEP=50

OVERWRITE_TABLE=overwrite_result
OVERWRITE_TABLE_TYPE=ORC

BASE_SETUP=base_setup.hql
UPDATE_SETUP=update_setup.hql
MERGE_TEST_SCRIPT=merge.hql
IO_TEST_SCRIPT=io.hql


create_data() {
  if [ "$GEN_BASE_DATA" = true ];
  then
    echo "Generating base table: $ROWS rows, $COLUMNS columns"
    python gen_random_csv.py $ROWS $COLUMNS $COLUMN_SIZE $PARTITIONS $BASE_DATA
  fi

  if [ "$GEN_DELTA_DATA" = true ];
  then
    echo "Generating update table: $UPDATE_ROWS rows, $COLUMNS columns"
    python gen_random_csv.py $UPDATE_ROWS $COLUMNS $COLUMN_SIZE $PARTITIONS $UPDATE_DATA
  fi
}

setup_tests() {
  echo 'Creating setup scripts for Hive'
  data_path="$(pwd)/$BASE_DATA"
  python gen_setup_script.py $BASE_TABLE $COLUMNS $data_path $BASE_SETUP

  data_path="$(pwd)/$UPDATE_DATA"
  python gen_setup_script.py $UPDATE_TABLE $COLUMNS $data_path $UPDATE_SETUP

  cat $BASE_SETUP $UPDATE_SETUP > setup.hql

  echo 'Loading tables'
  if [ "$GEN_BASE_DATA" = true ] || [ "$GEN_UPDATE_DATA" = true ];
  then
    hive -f setup.hql -v
  fi
}

create_test_scripts() {
  echo 'Generating merge script'
  args=($COLUMNS $COLUMN_DELTA $BASE_TABLE $UPDATE_TABLE $MERGE_TABLE \
  $MERGE_TABLE_CLUSTER_COLUMN $MERGE_BUCKETS $MERGE_TEST_SCRIPT)
  python gen_merge_script.py "${args[@]}"

  echo 'Generating insert overwrite script'
  args=($COLUMNS $BASE_TABLE $UPDATE_TABLE $OVERWRITE_TABLE $IO_TEST_SCRIPT)
  python gen_io_script.py "${args[@]}"
}

run_test() {
  echo 'Updating test scripts'
  create_test_scripts

  echo "Running Benchmark with Rows: $ROWS, Columns: $COLUMNS, Partitions: $PARTITIONS, Buckets: $MERGE_BUCKETS"
  echo 'Starting merge script'
  timer start
  hive -f $MERGE_TEST_SCRIPT -v 
  timer stop

  echo 'Starting insert overwrite script'
  timer start
  hive -f $IO_TEST_SCRIPT -v
  timer stop
}

run_benchmark() {
  create_data
  setup_tests
  run_test
}

timer() {
  cmd=$1
  case $cmd in 
    start) startsecs=$(date +%s)
      ;;
    stop) stopsecs=$(date +%s)
      diff=$(($stopsecs - $startsecs))
      echo "Runtime $diff"
      ;;
    *) echo 'invalid cmd'
      ;;
  esac
}

run_benchmark
