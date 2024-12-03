from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Table, Column, String, MetaData, select

class SemrushToolInput(BaseModel):
    """Input schema for SemrushTool."""
    client: str = Field(..., description="Name of the client.")

class SemrushTool(BaseTool):
    name: str = "SEMRush Tool"
    description: str = (
        "Use this tool to analyze competitors using SEMRush."
    )
    args_schema: Type[BaseModel] = SemrushToolInput

    def _run(self, client: str) -> str:
        # Implementation goes here
        return f"SEMRush analysis report for {client}."
    

class StoreInDatabaseToolInput(BaseModel):
    """
    Input schema for the StoreInDatabaseTool.
    Defines the input structure for storing data in the database.
    """
    content_type: str = Field(..., description="Type of content to store in the database.")
    data: str = Field(..., description="The data to store in the database.")

class StoreInDatabaseToolInput(BaseModel):
    """
    Input schema for StoreInDatabaseTool.
    """
    content_type: str = Field(..., description="Type of content to store in the database.")
    data: str = Field(..., description="The data to store in the database.")

class StoreInDatabaseTool(BaseTool):
    """
    Custom tool for storing data in a database.
    """
    name: str = "store_in_database"
    description: str = "Use this tool to store data in the database."
    args_schema: Type[BaseModel] = StoreInDatabaseToolInput

    def __init__(self):
        # Database setup
        self.engine = create_engine("sqlite:///content.db")  # Replace with your DB URL
        self.metadata = MetaData()

        # Define the table
        self.content_table = Table(
            "content", self.metadata,
            Column("content_type", String),
            Column("data", String)
        )

       
        self.metadata.create_all(self.engine)

    def _run(self, content_type: str, data: str) -> str:
        """
        Runs the database storage operation.
        Args:
            content_type: Type of content being stored.
            data: The content data to store.
        Returns:
            Confirmation message.
        """
        with self.engine.connect() as conn:
            insert_query = self.content_table.insert().values(content_type=content_type, data=data)
            conn.execute(insert_query)
        return f"Stored '{content_type}' data in the database: {data[:50]}..."

    async def _arun(self, content_type: str, data: str) -> str:
        """
        Async version of the database storage operation.
        Args:
            content_type: Type of content being stored.
            data: The content data to store.
        Returns:
            Confirmation message.
        """
        return self._run(content_type, data)


from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
from sqlalchemy import create_engine, Table, Column, String, MetaData, select

# Define the input schema for the tool
class FetchFromDatabaseToolInput(BaseModel):
    """
    Input schema for the FetchFromDatabaseTool.
    """
    content_type: str = Field(..., description="Type of content to fetch from the database.")

class FetchFromDatabaseTool(BaseTool):
    """
    Custom tool for fetching data from a database.
    """
    name: str = "fetch_from_database"
    description: str = "Use this tool to fetch data from the database by content type."
    args_schema: Type[BaseModel] = FetchFromDatabaseToolInput

    def __init__(self):
        # Database setup
        self.engine = create_engine("sqlite:///content.db")  # Replace with your DB URL
        self.metadata = MetaData()

        # Define the table
        self.content_table = Table(
            "content", self.metadata,
            Column("content_type", String),
            Column("data", String)
        )

       
        self.metadata.create_all(self.engine)

    def _run(self, content_type: str) -> str:
        """
        Fetch data from the database synchronously.
        Args:
            content_type: The type of content to fetch.
        Returns:
            The fetched data as a string.
        """
        with self.engine.connect() as conn:
            query = select(self.content_table.c.data).where(self.content_table.c.content_type == content_type)
            result = conn.execute(query)
            fetched_data = [row["data"] for row in result]
        return (
            f"Fetched data for {content_type}: {fetched_data[:50]}..."
            if fetched_data else f"No data found for {content_type}."
        )

    async def _arun(self, content_type: str) -> str:
        """
        Async version of fetching data from the database.
        Args:
            content_type: The type of content to fetch.
        Returns:
            The fetched data as a string.
        """
        return self._run(content_type)
    
    from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
import requests

class ShopifyPostToolInput(BaseModel):
    """
    Input schema for ShopifyPostTool.
    """
    title: str = Field(..., description="Title of the post.")
    content: str = Field(..., description="Content to publish on Shopify.")
    blog_id: str = Field(..., description="Shopify Blog ID to publish the post.")

class ShopifyPostTool(BaseTool):
    """
    Tool to post content to Shopify.
    """
    name: str = "shopify_post_tool"
    description: str = "Post content to Shopify blog or product."
    args_schema: Type[BaseModel] = ShopifyPostToolInput

    def _run(self, title: str, content: str, blog_id: str) -> str:
        """
        Posts content to Shopify synchronously.
        Args:
            title: Title of the content.
            content: Content to be published.
            blog_id: Shopify Blog ID.
        Returns:
            Confirmation message or error.
        """
        shopify_url = "https://{shop_name}.myshopify.com/admin/api/2023-01/blogs/{blog_id}/articles.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": "your_shopify_access_token"
        }

        payload = {
            "article": {
                "title": title,
                "body_html": content
            }
        }

        try:
            response = requests.post(shopify_url.format(shop_name="your_shop_name", blog_id=blog_id), headers=headers, json=payload)
            if response.status_code == 201:
                return f"Successfully posted content: '{title}' to Shopify."
            else:
                return f"Failed to post content to Shopify: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error occurred while posting to Shopify: {str(e)}"

    async def _arun(self, title: str, content: str, blog_id: str) -> str:
        """
        Async version of posting content to Shopify.
        """
        # Shopify's requests are synchronous; use aiohttp or similar library for async calls if needed
        return self._run(title, content, blog_id)

