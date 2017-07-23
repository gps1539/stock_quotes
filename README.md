# stock_quote
python script for getting stock quotes, calculating gains and losses and optionally recording to a time series database (influxdb).

stock_quote]$ ./stock_quote --help

usage: stock_quote [-h] [--add ADD [ADD ...]] [--delete DELETE]
                   [--influx INFLUX [INFLUX ...]] [--offline]
                   [--portfolio PORTFOLIO]
optional arguments:

  -h, --help            show this help message and exit
  --add ADD [ADD ...]   add a symbol, the quantity held and the price paid
  --delete DELETE       delete a symbol
  --influx INFLUX [INFLUX ...]
                        influx server, port, user and password
  --offline             displays last downloaded data
  --portfolio PORTFOLIO
                        choose a portfolio
  --read READ [READ ...]
                        read transactions from a csv file (google finance)

  
When adding the stock symbol, quantity and price are required

Files are created in a .stocks directory in the users home directory

Allows multiple portfolios to be created and used. They are created as directories under .stocks in the user's home directory. Program will create 3 files in the portfolio directory to store portfolio info (cost.npy, last.npy and stocks.npy)

For continuous updates watch (bash) is useful:
watch -n 5 --color stock_quote

When using --influx, influxdb most be running on the target server and you must have a valid user and passwd
Graphs can be created using grafana (and other tools) by using influxdb as a datasource.

Supports exported csv from a google finance portfolio.   
