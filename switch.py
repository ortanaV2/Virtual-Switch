import json
import os
import time

while True:
    try:
        while True:
            time.sleep(0.1) #refresh-rate
            
            #connection-queue-check
            with open("queue.json", "r") as data:
                queue = json.load(data)

            if queue != []:
                for address in queue:
                    template = {
                        "req":"None",
                        "res":"None",
                        "exchange":"None"
                    }
                    #create port for address
                    with open(f"./ports/{address}.json", "w") as port_create:
                        json.dump(template, port_create)
                    
                #clear queue
                queue.remove(address)
            with open("queue.json", "w") as data:
                json.dump(queue, data)
            
            #req-check
            ports_dic = "./ports"
            ports = os.listdir(ports_dic)
            max_port_count = len(ports)
            port_count = 0
            for port in ports:
                port_count+=1
                with open(f"./ports/{port}", "r") as port_data:
                    data = json.load(port_data)
                request = data["req"]
                response = data["res"]
                exchange = data["exchange"]
                print(f"Iterate {port_count}/{max_port_count}\t{port}\t[{request}]")

                if (request != "None") and (exchange != "None"):
                    try:
                        with open(f"./ports/{exchange}.json", "r") as contact:
                            contact_data = json.load(contact)
                        pre_res = contact_data["res"]
                        contact_data["req"] = request
                        with open(f"./ports/{exchange}.json", "w") as contact:
                            json.dump(contact_data, contact)   

                        refresh_count = 0
                        while True:
                            time.sleep(0.1)
                            with open(f"./ports/{exchange}.json", "r") as contact:
                                contact_data = json.load(contact)
                                
                            if contact_data["res"] != pre_res: #check if response has changed since new request
                                data["res"] = contact_data["res"]
                                data["req"] = "None"
                                with open(f"./ports/{port}", "w") as port_data:
                                    json.dump(data, port_data)
                                break
                            else:
                                refresh_count+=1
                                if refresh_count == 5:
                                    data["res"] = "E:503" #Service unavailable 
                                    data["req"] = "None"
                                    with open(f"./ports/{port}", "w") as port_data:
                                        json.dump(data, port_data)
                                    break
                    except Exception:
                        print(f"E:404 ---> decode?\t{port}\t[error_response]")
                        data["res"] = "E:404" #(Port) not found
                        data["req"] = "None"
                        with open(f"./ports/{port}", "w") as port_data:
                            json.dump(data, port_data)
    except Exception:
        print("critical error\tsystem\t[reboot]")
        open("queue.json", "w").write("[]")