from fastmcp import FastMCP
import httpx

server = FastMCP("FastMCP performance test", version="1.0.0")


@server.tool
async def say_hello(name: str) -> str:
    """Says hello"""
    
    return f"Hello {name}!"


@server.tool
async def make_api_call() -> str:
    """Make an API call"""

    async with httpx.AsyncClient() as client:
        result = await client.get("YOUR API GOES HERE")
    
    return str(result.status_code)


if __name__ == "__main__":
    server.run()
