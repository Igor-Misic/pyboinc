import asyncio

from pyboinc import init_rpc_client, xml_to_dict

IP_BOINC = "127.0.0.1"
PASSWORD_BOINC = "example_password"


async def main():
    rpc_client = await init_rpc_client(IP_BOINC, PASSWORD_BOINC)

    # Get status of current and older tasks
    results = await rpc_client.get_results()
    results_d = [xml_to_dict(result) for result in results]
    print(results_d)
    print(await rpc_client.get_project_status())
    print(await rpc_client.get_old_results())

    # Get last three messages
    c = await rpc_client.get_message_count()
    print(c)
    print(await rpc_client.get_messages(c-3))

    print(await rpc_client.get_notices_public(2))

    # suspend task and resume
    task = (results_d[0]["project_url"], results_d[0]["name"])
    print(await rpc_client.suspend_result(*task))
    print(await rpc_client.resume_result(*task))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
