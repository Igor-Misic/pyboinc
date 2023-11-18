#!/usr/bin/python3

import asyncio

from pyboinc import init_rpc_client

IP_BOINC_1 = "192.168.35.221"
#IP_BOINC_1 = "127.0.0.1"
PASSWORD_BOINC = ""

DOWNLOAD_STATE = 1
RUNNING_STATE = 2

DISABLE_EINSTEIN =True

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
        results = await rpc_client_1.project_update(
            "http://www.worldcommunitygrid.org/"
        )
        print("WCG update: " + str(results))
        results = await rpc_client_1.project_update("http://www.gpugrid.net/")
        print("GPUGRID update: " + str(results))
        results = await rpc_client_1.project_update(
            "https://boinc.bakerlab.org/rosetta/"
        )
        print("Rosetta update: " + str(results))
    except:
        print("project_update -> exception occurred")

    try:

        gpugrid_suspended_via_gui = False
        wcg_suspended_via_gui = False
        einstein_suspended_via_gui = False
        results = await rpc_client_1.get_project_status()
        for result in results:
            if result["master_url"] == "https://www.gpugrid.net/":
                try:
                    gpugrid_suspended_via_gui = result["suspended_via_gui"]
                except:
                    print ("GPUGRID not suspended")

            if result["master_url"] == "http://www.worldcommunitygrid.org/":
                try:
                    wcg_suspended_via_gui = result["suspended_via_gui"]
                except:
                    print ("WCG not suspended")

            if result["master_url"] == "https://einstein.phys.uwm.edu/":
                try:
                    einstein_suspended_via_gui = result["suspended_via_gui"]
                except:
                    print ("Einstein not suspended")

        results = await rpc_client_1.get_results()
        gpu_grid_tasks = 0
        wcg_tasks = 0
        rosseta_tasks = 0
        univers_tasks = 0
        einstein_tasks = 0

        for result in results:
            if (
                not gpugrid_suspended_via_gui
                and result["project_url"] == "https://www.gpugrid.net/"
                and result["state"] == RUNNING_STATE
            ):
                gpu_grid_tasks = 1 + gpu_grid_tasks
            if result["project_url"] == "http://www.worldcommunitygrid.org/":
                wcg_tasks = 1 + wcg_tasks

            if result["project_url"] == "https://boinc.bakerlab.org/rosetta/":
                rosseta_tasks = 1 + rosseta_tasks

            if result["project_url"] == "https://universeathome.pl/universe/":
                univers_tasks = 1 + univers_tasks

            if result["project_url"] == "https://einstein.phys.uwm.edu/":
                einstein_tasks = 1 + einstein_tasks

        print("number of GPUGRID tasks:" + str(gpu_grid_tasks))
        print("number of WCG tasks:" + str(wcg_tasks))
        print("number of Rosseta tasks:" + str(rosseta_tasks))
        print("number of Univers tasks:" + str(univers_tasks))
        print("number of Einstein tasks:" + str(einstein_tasks))

        if rosseta_tasks < 5 and univers_tasks <= 10:
            print("WCG suspend: " + str(results))
            results = await rpc_client_1.project_allow_more_work(
                "https://universeathome.pl/universe/"
            )

        if univers_tasks > 10:
            results = await rpc_client_1.project_no_more_work(
                "https://universeathome.pl/universe/"
            )


        if gpu_grid_tasks < 2:
            results = await rpc_client_1.project_allow_more_work(
                "https://www.gpugrid.net/"
            )

        if gpu_grid_tasks >= 2:
            results = await rpc_client_1.project_no_more_work(
                "https://www.gpugrid.net/"
            )

        if einstein_tasks < 5 and gpu_grid_tasks == 0:
            results = await rpc_client_1.project_allow_more_work(
                "https://einstein.phys.uwm.edu/"
            )

        if einstein_tasks >= 10:
            results = await rpc_client_1.project_no_more_work(
                "https://einstein.phys.uwm.edu/"
            )

        if gpu_grid_tasks > 0:

            if DISABLE_EINSTEIN and einstein_suspended_via_gui == False:
                results = await rpc_client_1.project_suspend(
                    "https://einstein.phys.uwm.edu/"
                )
                print("Einstein suspend: " + str(results))

            if wcg_suspended_via_gui == False and wcg_tasks > 200:
                results = await rpc_client_1.project_suspend(
                    "https://www.worldcommunitygrid.org/"
                )
                print("WCG suspend: " + str(results))
        else:

            if einstein_suspended_via_gui == True:
                results = await rpc_client_1.project_resume(
                    "https://einstein.phys.uwm.edu/"
                )
                print("Einstein resume: " + str(results))

            if wcg_suspended_via_gui == True:
                results = await rpc_client_1.project_resume(
                    "https://www.worldcommunitygrid.org/"
                )
                print("WCG resume: " + str(results))

    except Exception as e:
        print(e)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
