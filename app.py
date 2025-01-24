import os
import sys
from dotenv import load_dotenv
import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use.browser.browser import BrowserConfig, Browser

# Load environment variables from .env file
load_dotenv()

# Check if API key exists
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Basic configuration
browser = Browser(
    config = BrowserConfig(
    disable_security=True,
    headless=False,  # Set to True for headless mode
    chrome_instance_path=os.path.join(
            os.environ.get("PROGRAMFILES", "C:\\Program Files"),
            "Google\\Chrome\\Application\\chrome.exe"), # locates chrome path for windows users
    extra_chromium_args=['--remote-debugging-port=9222']
    )
)

llm = ChatOpenAI(model='gpt-4o')
agent = Agent(
	task="""1.Go to amazon.com
  2. go to the FREE Shipping to Philippines page 
  3. browse down and look for the Electronics category
  4. sort category by best seller
  5. browse down multiple times until you reach the bottom of the page
  6. give me a list of top 10 items from Electronics category""",
	llm=llm,
    browser=browser, 
    use_vision=True,
)


async def main():
	await agent.run(max_steps=50)
	input('Press Enter to continue...')


asyncio.run(main())