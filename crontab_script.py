#!/usr/bin/python3

import asyncio
import time

from pyboinc import init_rpc_client

IP_BOINC_1 = "192.168.35.239"
#IP_BOINC_1 = "127.0.0.1"
PASSWORD_BOINC = ""


async def main():

    rpc_client_1 = await init_rpc_client(IP_BOINC_1, PASSWORD_BOINC)

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


    try:
        results = await rpc_client_1.project_update("http://www.worldcommunitygrid.org/")
        print ("WCG update: " + str(results))
        results = await rpc_client_1.project_update("http://www.gpugrid.net/")
        print ("GPUGRID update: " + str(results))
        results = await rpc_client_1.project_update("https://boinc.bakerlab.org/rosetta/")
        print ("Rosetta update: " + str(results))
    except:
        print("project_update -> exception occurred")

    try:
        results = await rpc_client_1.get_results()
        gpu_grid_tasks = 0
        wcg_tasks = 0
        for result in results:
            if result["project_url"] == "https://www.gpugrid.net/":
                gpu_grid_tasks = 1 + gpu_grid_tasks
            if result["project_url"] == "https://www.worldcommunitygrid.org/":
                wcg_tasks = 1 + wcg_tasks

        if gpu_grid_tasks > 0:
            print ("number of GPUGRID tasks:" + str(gpu_grid_tasks))
            results = await rpc_client_1.project_suspend("https://einstein.phys.uwm.edu/")
            print ("Einstein suspend: " + str(results))
            if wcg_tasks > 5:
                results = await rpc_client_1.project_suspend("https://www.worldcommunitygrid.org/")
                print ("WCG suspend: " + str(results))
        else:
            results = await rpc_client_1.project_resume("https://einstein.phys.uwm.edu/")
            print ("Einstein resume: " + str(results))
            results = await rpc_client_1.project_resume("https://www.worldcommunitygrid.org/")
            print ("WCG resume: " + str(results))


    except:
        print("project_get -> exception occurred")
            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
