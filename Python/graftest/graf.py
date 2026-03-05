import asyncio
import random
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

# Number of nodes
NODES = 5

# Create a simple undirected graph
#G = nx.cycle_graph(NODES)  # ring for simplicity
G = nx.watts_strogatz_graph(n=20, k=4, p=0.15)
matplotlib.use('TkAgg') 

nx.draw(G, with_labels=True)
plt.show()

# Message queues for each node
mailboxes = {node: asyncio.Queue() for node in G.nodes}


async def agent(node_id):
    while True:
        token = await mailboxes[node_id].get()
        print(f"Node {node_id} received token: {token}")

        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate processing time

        neighbors = list(G.neighbors(node_id))
        next_node = random.choice(neighbors)
        print(f"Node {node_id} sends token {token[0]} to {next_node}")
        await mailboxes[next_node].put((token[0], token[1]+1))


async def main():
    # Start all agents
    tasks = [asyncio.create_task(agent(n)) for n in G.nodes]

    # Start the first token at node 0
    await mailboxes[0].put((0,0))
    await asyncio.sleep(1)
    await mailboxes[1].put((1,0))


    # Let it run for a while
    await asyncio.sleep(10)

    # Cancel all tasks
    for t in tasks:
        t.cancel()

    print("Simulation ended.")

asyncio.run(main())