# sync_info #
It has a client and a server writen in python.  
The client will tell server its hostname and ip.  
I use it when my pc's ip changed with time.  

## Usage ##
- Client  
    The client send a post request to server.  
    You can use `crontab` to make it excuted hourly on linux.  
- Server  
    Server use **Flask** framework.  
    It processes client's post request and save info.  
    You can also get info from browser using url `/sync` or `/sync/< hostname >`  

## Requirements ##
- Python 2.x
- flask
    ```
    pip install flask
    ```

## END ##
Just enjoy it! :)

