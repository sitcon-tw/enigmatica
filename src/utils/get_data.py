import json
import asyncfile


data = None
story = None

def init():
    """Initialize the story data."""
    global data
    global story
    try:
        with open('src/data/story.json', 'r', encoding='utf-8') as f:
            story = f.read()    
        with open('src/data/data.json', 'r', encoding='utf-8') as f:
            data = f.read()
        story = json.loads(story)
        data = json.loads(data)
    except FileNotFoundError as e:
        print("Data file not found." + e)
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON from story data file.")
        return {}
    
async def read_file(file_path: str) -> str:
    """Read a file asynchronously."""
    try:
        async with asyncfile.open(file_path, 'r', encoding='utf-8') as f:
            return await f.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return ""
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

async def get_story(story_number: str):
    global story
    file_path = None
    try:
        file_path = story[story_number]["file"]
        story_content = await read_file(f'src/data/story/{file_path}')
        if not story_content:
            return "Story content is empty or file not found."
        return story_content
    except KeyError:
        print(f"Story number {story_number} not found in data.")
        return "Story not found."