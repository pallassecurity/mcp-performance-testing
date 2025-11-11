import asyncio
from contextlib import asynccontextmanager, contextmanager
import subprocess
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from fastmcp import Client
from fastmcp.client import StdioTransport


N = 100


@contextmanager
def timer(results):
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    results.append(end - start)


def build_python_docker(tag: str = "fastmcp-test") -> None:
    subprocess.run(["docker", "build", "-t", tag, "-f", "Dockerfile.fastmcp", "."], check=True)


def build_node_docker(tag: str = "node-test") -> None:
    subprocess.run(["npm", "run", "build"], check=True)
    subprocess.run(["docker", "build", "-t", tag, "-f", "Dockerfile.node", "."], check=True)


@asynccontextmanager
async def fastmcp_client():
    transport = StdioTransport(
        "./.venv/bin/python",
        ["./server.py"],
        keep_alive=False
    )

    async with Client(transport) as client:
        yield client


@asynccontextmanager
async def fastmcp_docker_client(tag: str = "fastmcp-test"):
    transport = StdioTransport(
        "docker",
        [
            "run",
            "-i",
            "--rm",
            tag
        ],
        keep_alive=False
    )

    async with Client(transport) as client:
        yield client


@asynccontextmanager
async def node_client():
    transport = StdioTransport(
        "node",
        ["./build/index.js"],
        keep_alive=False
    )

    async with Client(transport) as client:
        yield client


@asynccontextmanager
async def node_docker_client(tag: str = "node-test"):
    transport = StdioTransport(
        "docker",
        [
            "run",
            "-i",
            "--rm",
            tag
        ],
        keep_alive=False
    )

    async with Client(transport) as client:
        yield client


async def startup_test():
    fastmcp_startup_times = []
    for _ in range(N):
        with timer(fastmcp_startup_times):
            async with fastmcp_client() as _:
                pass

    fastmcp_docker_startup_times = []
    for _ in range(N):
        with timer(fastmcp_docker_startup_times):
            async with fastmcp_docker_client() as _:
                pass

    node_startup_times = []
    for _ in range(N):
        with timer(node_startup_times):
            async with node_client() as _:
                pass

    node_docker_startup_times = []
    for _ in range(N):
        with timer(node_docker_startup_times):
            async with node_docker_client() as _:
                pass

    return pd.DataFrame({
        "fastmcp": fastmcp_startup_times,
        "fastmcp_docker": fastmcp_docker_startup_times,
        "node": node_startup_times,
        "node_docker": node_docker_startup_times
    })


async def tool_list_test():
    fastmcp_list_times = []
    async with fastmcp_client() as client:
        for _ in range(N):
            with timer(fastmcp_list_times):
             _ = await client.list_tools_mcp()

    fastmcp_docker_list_times = []
    async with fastmcp_docker_client() as client:
        for _ in range(N):
            with timer(fastmcp_docker_list_times):
             _ = await client.list_tools_mcp()

    node_list_times = []
    async with node_client() as client:
        for _ in range(N):
            with timer(node_list_times):
             _ = await client.list_tools_mcp()

    node_docker_list_times = []
    async with node_docker_client() as client:
        for _ in range(N):
            with timer(node_docker_list_times):
             _ = await client.list_tools_mcp()

    return pd.DataFrame({
        "fastmcp": fastmcp_list_times,
        "fastmcp_docker": fastmcp_docker_list_times,
        "node": node_list_times,
        "node_docker": node_docker_list_times
    })


async def isolated_tool_call_test():
    fastmcp_call_times = []
    for _ in range(N):
        with timer(fastmcp_call_times):
            async with fastmcp_client() as client:
                _ = await client.call_tool_mcp("say_hello", {"name": "Josh"})

    fastmcp_docker_call_times = []
    for _ in range(N):
        with timer(fastmcp_docker_call_times):
            async with fastmcp_docker_client() as client:
                _ = await client.call_tool_mcp("say_hello", {"name": "Josh"})

    node_call_times = []
    for _ in range(N):
        with timer(node_call_times):
            async with node_client() as client:
                _ = await client.call_tool_mcp("say_hello", {"name": "Josh"})

    node_docker_call_times = []
    for _ in range(N):
        with timer(node_docker_call_times):
            async with node_docker_client() as client:
                _ = await client.call_tool_mcp("say_hello", {"name": "Josh"})

    return pd.DataFrame({
        "fastmcp": fastmcp_call_times,
        "fastmcp_docker": fastmcp_docker_call_times,
        "node": node_call_times,
        "node_docker": node_docker_call_times
    })


async def sequential_tool_call_test():
    fastmcp_call_times = []
    async with fastmcp_client() as client:
        for _ in range(N):
            with timer(fastmcp_call_times):
                _ = await client.call_tool_mcp("say_hello", {"name": "Josh"})

    fastmcp_docker_call_times = []
    async with fastmcp_docker_client() as client:
        for _ in range(N):
            with timer(fastmcp_docker_call_times):
                _ = await client.call_tool_mcp("say_hello", {"name": "Josh"})

    node_call_times = []
    async with node_client() as client:
        for _ in range(N):
            with timer(node_call_times):
                _ = await client.call_tool_mcp("say_hello", {"name": "Josh"})

    node_docker_call_times = []
    async with node_docker_client() as client:
        for _ in range(N):
            with timer(node_docker_call_times):
                _ = await client.call_tool_mcp("say_hello", {"name": "Josh"})

    return pd.DataFrame({
        "fastmcp": fastmcp_call_times,
        "fastmcp_docker": fastmcp_docker_call_times,
        "node": node_call_times,
        "node_docker": node_docker_call_times
    })


async def api_tool_call_test():
    fastmcp_call_times = []
    async with fastmcp_client() as client:
        for _ in range(N):
            with timer(fastmcp_call_times):
                _ = await client.call_tool_mcp("make_api_call", {})

    fastmcp_docker_call_times = []
    async with fastmcp_docker_client() as client:
        for _ in range(N):
            with timer(fastmcp_docker_call_times):
                _ = await client.call_tool_mcp("make_api_call", {})

    node_call_times = []
    async with node_client() as client:
        for _ in range(N):
            with timer(node_call_times):
                _ = await client.call_tool_mcp("make_api_call", {})

    node_docker_call_times = []
    async with node_docker_client() as client:
        for _ in range(N):
            with timer(node_docker_call_times):
                _ = await client.call_tool_mcp("make_api_call", {})

    return pd.DataFrame({
        "fastmcp": fastmcp_call_times,
        "fastmcp_docker": fastmcp_docker_call_times,
        "node": node_call_times,
        "node_docker": node_docker_call_times
    })


async def main():
    # Run startup tests
    print("Running startup tests")
    startup_df = await startup_test()
    startup_df.to_csv("results/startup.csv", index=False)
    cold_startups = startup_df.iloc[0]
    warm_startup_df = startup_df.iloc[1:]

    plt.clf()
    sns.kdeplot(data=warm_startup_df.melt(var_name="server", value_name="time"), x="time", hue="server")
    plt.title("Warm startup times for basic MCP servers")
    plt.xlabel("Time to startup (s)")
    plt.ylabel("Density")
    plt.savefig("results/warm_startup_plot.png")
    plt.close()

    plt.clf()
    sns.barplot(cold_startups)
    plt.title("Cold startup times for basic MCP servers")
    plt.ylabel("Time to startup (s)")
    plt.savefig("results/cold_startup_plot.png")
    plt.close()

    # Run tool list tests
    print("Running tool list tests")
    tool_list_df = await tool_list_test()
    tool_list_df.to_csv("results/tool_list.csv", index=False)

    plt.clf()
    sns.kdeplot(data=tool_list_df.melt(var_name="server", value_name="time"), x="time", hue="server")
    plt.title("Tool list times for basic MCP servers")
    plt.xlabel("Tool list time (s)")
    plt.ylabel("Density")
    plt.savefig("results/tool_list_plot.png")
    plt.close()

    # Run isolated tool call tests
    print("Running isolated tool call tests")
    isolated_tool_call_df = await isolated_tool_call_test()
    isolated_tool_call_df.to_csv("results/isolated_tool_call.csv", index=False)

    plt.clf()
    sns.kdeplot(data=isolated_tool_call_df.iloc[1:].melt(var_name="server", value_name="time"), x="time", hue="server")
    plt.title("Isolated tool call times for basic MCP servers")
    plt.xlabel("Time to startup + call (s)")
    plt.ylabel("Density")
    plt.savefig("results/isolated_tool_call_plot.png")
    plt.close()

    # Run sequential tool call tests
    print("Running sequential tool call tests")
    sequential_tool_call_df = await sequential_tool_call_test()
    sequential_tool_call_df.to_csv("results/sequential_tool_call.csv", index=False)

    plt.clf()
    sns.kdeplot(data=sequential_tool_call_df.melt(var_name="server", value_name="time"), x="time", hue="server")
    plt.title("Sequential tool call times for basic MCP servers")
    plt.xlabel("Time to call (s)")
    plt.ylabel("Density")
    plt.savefig("results/sequential_tool_call_plot.png")
    plt.close()

    # Run individual tool calls with API call
    print("Running API tool call tests")
    api_tool_call_df = await api_tool_call_test()
    api_tool_call_df.to_csv("results/api_tool_call.csv", index=False)

    plt.clf()
    sns.kdeplot(data=api_tool_call_df.melt(var_name="server", value_name="time"), x="time", hue="server")
    plt.title("Sequential tool call times with API call")
    plt.xlabel("Time to call (s)")
    plt.ylabel("Density")
    plt.savefig("results/api_tool_call_plot.png")
    plt.ylim(0, 10)
    plt.close()

    # Print results
    for _ in range(20):
        print()

    print("Results:")
    print()

    print("Cold startup times:")
    print(cold_startups)
    print()

    print("Warm startup times:")
    print(warm_startup_df.describe())
    print()

    print("Tool list times:")
    print(tool_list_df.describe())
    print()

    print("Isolated tool call times:")
    print(isolated_tool_call_df.describe())
    print()

    print("Sequential tool call times:")
    print(sequential_tool_call_df.describe())
    print()

    print("API tool call times:")
    print(api_tool_call_df.describe())
    print()


if __name__ == "__main__":
    asyncio.run(main())
