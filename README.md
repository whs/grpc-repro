```
INFO:ServerThread:Building server
INFO:ServerThread:Server start
INFO:root:Sending first call
INFO:PingServicerImpl:Received Ping call
INFO:root:Ping response: 
INFO:root:Restarting server
INFO:ServerThread:Stopping server
INFO:ServerThread:Server stopped
INFO:ServerThread:Building server
INFO:ServerThread:Server start
INFO:root:Sending second call
Traceback (most recent call last):
  File "main.py", line 76, in <module>
    logging.info('Ping response: %s', client.Ping(PingRequest()))
  File "/home/whs/apps/grpc-repro/.direnv/python-3.7.3/lib/python3.7/site-packages/grpc/_channel.py", line 549, in __call__
    return _end_unary_response_blocking(state, call, False, None)
  File "/home/whs/apps/grpc-repro/.direnv/python-3.7.3/lib/python3.7/site-packages/grpc/_channel.py", line 466, in _end_unary_response_blocking
    raise _Rendezvous(state, None, None, deadline)
grpc._channel._Rendezvous: <_Rendezvous of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "Socket closed"
	debug_error_string = "{"created":"@1555352933.800544790","description":"Error received from peer","file":"src/core/lib/surface/call.cc","file_line":1039,"grpc_message":"Socket closed","grpc_status":14}"
>
INFO:root:Sending third call
INFO:PingServicerImpl:Received Ping call
INFO:root:Ping response: 
INFO:ServerThread:Stopping server
INFO:ServerThread:Server stopped
```
