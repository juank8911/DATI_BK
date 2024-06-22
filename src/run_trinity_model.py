# ./trinity_ai/run_trinity_model.py

import asyncio
from trinity_ai import initialize_trinity_model

async def main():
    model = await initialize_trinity_model()
    # ... (rest of your code that uses the model)

if __name__ == "__main__":
    asyncio.run(main())
