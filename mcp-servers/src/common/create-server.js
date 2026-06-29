import express from 'express';

/**
 * Creates an MCP-compatible HTTP tool server.
 * Exposes GET /health, GET /tools, POST /tools/:name, GET /mcp/manifest
 */
export function createMcpServer({ name, description, port, tools }) {
  const app = express();
  app.use(express.json());

  const toolMap = Object.fromEntries(tools.map(t => [t.name, t]));

  app.get('/health', (_req, res) => res.json({ status: 'UP', server: name }));

  app.get('/mcp/manifest', (_req, res) => {
    res.json({
      name,
      description,
      protocol: 'mcp-http-tools/1.0',
      tools: tools.map(({ name: n, description: d, inputSchema }) => ({ name: n, description: d, inputSchema }))
    });
  });

  app.get('/tools', (_req, res) => {
    res.json(tools.map(({ name: n, description: d }) => ({ name: n, description: d })));
  });

  app.post('/tools/:toolName', async (req, res) => {
    const tool = toolMap[req.params.toolName];
    if (!tool) {
      return res.status(404).json({ error: `Tool not found: ${req.params.toolName}` });
    }
    try {
      const result = await tool.handler(req.body ?? {});
      res.json({ content: [{ type: 'text', text: JSON.stringify(result, null, 2) }], data: result });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  app.listen(port, () => {
    console.log(`[${name}] MCP server listening on http://localhost:${port}`);
  });

  return app;
}
