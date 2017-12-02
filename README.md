# Bitshares ElasticSearch Wrapper

Wrapper for final user applications to interact with account data from the bitshares blockchain stored by  `bitshares-core` with `elasticsearch-plugin` running. 

## Install

- Install python elasticsearch low level lib:

`pip install elasticsearch`

- Install python elasticsearch high level lib to easy query:

`pip install elasticsearch-dsl`

- Clone and run it by flask:

```
git clone https://github.com/oxarbitrage/bitshares-es-wrapper.git
export FLASK_APP=wrapper.py
flask run --host=0.0.0.0
```
 
 ## Available Calls
 
 ### get_account history
 
Get all operations in history with pager, similar to bitshares node call.
 
 #### Samples:
 
 get history of account sort by date:

[View Online Sample](http://209.188.21.157:5000/get_account_history?account_id=1.2.282&from=100&size=10&sort_by=block_data.block_time)

sort by operation_time

[View Online Sample](http://209.188.21.157:5000/get_account_history?account_id=1.2.282&from=100&size=10&sort_by=operation_type)

reverse order:

[View Online Sample](http://209.188.21.157:5000/get_account_history?account_id=1.2.282&from=100&size=10&sort_by=-operation_type)