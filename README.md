# Virtual-Switch [WIP]
> A Virtual-Switch for connecting various machines over a NAS-Server based network to exchange data.

The data exchange is working with JSON-files: `{"req": "None", "res": "None", "exchange": "None"}`.
An external machine connects to the **VNS** *(virtual network switch)* by appending their address/IP/name to the queue. The switch creates a port that the machine can use by overwriting its JSON-file, which is called by its given queue key. Every time the machine sends a request, the **VNS** reads the `exchange` data. The exchange-data tells the switch which machine it should connect to. For each request, the connected machine issues a response and sends it back to the requestor. If the exchange-data is not correct and no connection-port is found, the switch responds with an error code.
## API
> How to create an API-system.

An API system can be created by not defining exchange data. (`"exchange":"None"`) So the port waits for the request and can respond. Because without exchange data, the requests are not sent to anyone and are basically useless. So you can use it as an API.
## Error Codes
> Types of error codes.

Error codes are written as follows: `E:404`. *404* stands for 'not found' and in this case it's used to tell the requestor that the port-address couldn't be found. *503* says that the responder is currently not responding and that the service is unavailable. 
> System issues.

If the switch stops working for a short time (~150ms), it could be due to a decode error in a JSON-file. When this happens, the entire system is rebooted and the queue is also reset.
## USAGE
> How to use the switch.

As mentioned earlier, you need to access the queue file and append an address for the machine to work with. After that it should exchange data with the assigned address file located in the *ports* directory.
```python
template = {
  "req":"None",    #request-data
  "res":"None",    #response-data
  "exchange":"3E-4F-G4-33-K3-E8"    #exchange-address
}
```
## SUPPORT
Reviews and suggestions for improvement are welcome!
