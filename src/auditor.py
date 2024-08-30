"""
Demonstrative auditor to mark components as vulnerable by notifying the maintainer.
"""

import asyncio
import sys
import json

from aiohttp import ClientSession
from support.agent import DEFAULT_INTERNAL_HOST
from support.database import OrionDB
from support.utils import log_msg, log_status, prompt_loop


class Auditor:
    """
    Class that holds logic for a sample auditor, marking software as vulnerable.
    Works by querying the orion database and notifying the issuer, i.e., the admin of a
    vulnerability.
    """

    def __init__(
        self,
        db_username="auditor",
        orion_db_url=f"http://{DEFAULT_INTERNAL_HOST}:6001",
    ):
        self.client_session = ClientSession()

        self.db_client = OrionDB(
            orion_db_url=orion_db_url,
            username=db_username,
            client_session=self.client_session,
        )

    def check_vulnerability(self, db_name, components):
        return [
            {
                "vulnerability": {"software": {"shady_stuff": 0.1}},
                "db_name": db_name,
            }
        ]

    async def notify_maintainer(self, db_name, vulnerabilities):
        response = await self.client_session.post(
            url=f"http://{DEFAULT_INTERNAL_HOST}:8002/webhooks/topic/notify_vulnerability/",
            json=vulnerabilities,
        )
        if not response.ok:
            log_status("\n\nERRROR HAPPENED\n\n")
        log_msg(f"Returned with {response.status}")
    
    async def notify_maintainer_batch(self, revocation_batch):
        print(f"revocation_batch")
        response = await self.client_session.post(
            url=f"http://{DEFAULT_INTERNAL_HOST}:8002/webhooks/topic/notify_batch_revocation/",
            json=revocation_batch,
        )
        if not response.ok:
            log_status("\n\nERRROR HAPPENED\n\n")
        log_msg(f"Returned with {response.status}")

    async def process_node(self, node, db_to_check):
        print(f"node to process: {node}")

        if node == "":
            log_msg("Aborting Node onboarding...")
            return
        
        # Initialize database key for this node
        self.db_client.db_keys[db_to_check][node] = {}

        try:
            value = await self.db_client.query_key(db_to_check, node)
            marked_vulnerabilities = self.check_vulnerability(db_to_check, value["components"])
            print(f"marked vulnerabilities: {marked_vulnerabilities}")
            if marked_vulnerabilities is not None:
                await self.notify_maintainer(db_to_check, marked_vulnerabilities)
        except Exception as e:
            log_msg(f"Error processing node {node}: {e}")

    # Add this method to db_client for getting all nodes
    async def get_all_nodes(self, db_name):
        try:
            # retrieving all nodes
            async with self.client_session.get(
                url=f"http://{DEFAULT_INTERNAL_HOST}:8002/webhooks/topic/get_all_nodes/"
            ) as response:
                if not response.ok:
                    log_status("\n\nERRROR HAPPENED\n\n")
                    log_msg(f"Returned with {response.status}")
                    return
                response_read = await response.json()
                response_json = json.loads(response_read)

                node_keys = response_json.get("node_keys", [])
                print(f"reiceved json: {response_json}, node keys: {node_keys}")
                return node_keys

        except Exception as e:
            # Log the exception and re-raise it
            log_msg(f"Exception occurred while getting all nodes: {str(e)}")
            raise

    async def get_all_nodes_and_process_concurrently(self, db_to_check):
        # Get all nodes from the database
        all_nodes = await self.get_all_nodes(db_to_check)
        print(f"{all_nodes}")

        # Process all nodes concurrently
        await asyncio.gather(*(self.process_node(node, db_to_check) for node in all_nodes))



async def main():
    auditor = Auditor()
    # simulated db to be checked
    db_to_check = "db1"
    auditor.db_client.db_keys[db_to_check] = {}
    nodes = auditor.db_client.db_keys[db_to_check]
    async for action in prompt_loop("Enter node names (comma-separated) or type 'all' or 'allCon' to check all nodes: "):
        if action is None or action.lower() == "exit":
            log_msg("Exiting...")
            break  # Exit the loop

        if action.lower() == "all":
            print("Trying to process all nodes")
            # Check all nodes
            all_nodes = await auditor.get_all_nodes(db_to_check)
            for node in all_nodes:
                await auditor.process_node(node, db_to_check)
        elif action.lower() == "allCon":
            print("Trying to process all nodes concurrently")
            # Check all nodes
            all_nodes = await auditor.get_all_nodes_and_process_concurrently(db_to_check)
        
        elif action.lower() == "test":
            db_nodes = auditor.db_client.query_all(db_to_check)
            print(f"{db_nodes}")

        else:
            print("Trying to process multiple nodes")
            # Process multiple nodes
            nodes = [node.strip() for node in action.split(',')]
            nodes_json = json.dumps(nodes)
            revocation = await auditor.notify_maintainer_batch(nodes_json)

    #except Exception:
    await auditor.client_session.close()



if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        sys.exit(1)
