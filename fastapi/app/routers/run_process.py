import asyncio
import subprocess

async def run_query(command):
    try:
        result = await asyncio.to_thread(
            subprocess.run,
            command,
            capture_output=True,
            text=True
        )
        return result.stdout
    except:
        return " ".join(command)