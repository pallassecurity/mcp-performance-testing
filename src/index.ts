import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
    name: "JS performance test",
    version: "1.0.0"
});

server.registerTool(
    "say_hello",
    {
        description: "Says hello",
        inputSchema: { name: z.string() },
        outputSchema: { result: z.string() }
    },
    async ({ name }) => {
        const output = { result: `Hello ${name}!` };
        return {
            content: [{ type: "text", text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
);

server.registerTool(
    "make_api_call",
    {
        description: "Says hello",
        outputSchema: { result: z.string() }
    },
    async () => {
        const something = await fetch("YOUR API GOES HERE");
        const output = { result: something.status };
        return {
            content: [{ type: "text", text: JSON.stringify(output) }],
            structuredContent: output
        };
    }
)

async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
}

main().catch((error) => {
    process.exit(1);
});
