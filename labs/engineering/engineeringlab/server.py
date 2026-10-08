"""Run with python -m engineeringlab.server; stdout is reserved for MCP."""
import importlib,os
import httpx
from mcp.server import MCPServer

def main():
    implementation=importlib.import_module(os.environ.get('COURSE_SUBMISSION','submission'))
    server=MCPServer('Course tickets')
    with httpx.Client(base_url=os.environ['COURSE_API_URL'],headers={'X-API-Key':os.environ['COURSE_API_KEY']},timeout=5) as client:
        implementation.register_tools(server,client)
        server.run(transport='stdio')
if __name__=='__main__':main()
