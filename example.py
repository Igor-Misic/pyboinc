import asyncio
import time

from pyboinc import init_rpc_client

#IP_BOINC_1 = "192.168.35.239"
IP_BOINC_1 = "127.0.0.1"
PASSWORD_BOINC = ""


async def main():

    counter = 39
    rpc_client_1 = await init_rpc_client(IP_BOINC_1, PASSWORD_BOINC)

    while(True):

        # Get status of current and older tasks
        results = await rpc_client_1.get_file_transfers()

        for result in results:

            try:
                if result["project_url"] == "http://www.worldcommunitygrid.org/":
                    task = (result["project_url"], result["name"])
                    print(task)
                    print(await rpc_client_1.retry_file_transfer(*task))
            except:
                print("An exception occurred")

        counter += 1

        if (counter == 40):
            counter = 0
            results = await rpc_client_1.project_update("http://www.worldcommunitygrid.org/")
            print ("WCG update: " + str(results))
            results = await rpc_client_1.project_update("http://www.gpugrid.net/")
            print ("GPUGRID update: " + str(results))
            results = await rpc_client_1.project_update("https://boinc.bakerlab.org/rosetta/")
            print ("Rosetta update: " + str(results))
            


        time.sleep(5)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
