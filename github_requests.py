"""
Make a script that given one or more GitHub's organizations, lists all public projects,
with their respective columns and cards, for each repository.

Use asyncio and aiohttp. Optionally implement a pool of consumers to limit the concurrent http requests.

Format the output in some way that lets the user to identifiy projects, columns, and cards, for each repository, at a glance.ß
"""
import aiohttp
import asyncio
import ssl
import certifi
import json
from fnutils import show_data


TOKEN = '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'
URL = 'https://api.github.com/users/carlosacg/projects'


async def make_get_request(url: str) -> dict:
    """
    This is a generic function to make a get request using aiohttp
    """
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)

    session = aiohttp.ClientSession(connector=conn)
    headers = {'Authorization': 'token %s' % TOKEN}
    result = await session.get(url, headers=headers)
    content = await result.text()

    return json.loads(content)


async def get_projects_data() -> None:
    """
    This function get the entire data from GitHubs projects
    including columns and cards
    """
    projects_list = await make_get_request(URL)
    for project in projects_list:
        columns_list = await make_get_request(project.get('columns_url'))
        project['columns_list'] = columns_list
        for column in columns_list:
            column['cards_list'] = await make_get_request(column.get('cards_url'))
    await show_data(projects_list)


async def main() -> None:
    await get_projects_data()


if __name__ == "__main__":
    asyncio.run(main())
