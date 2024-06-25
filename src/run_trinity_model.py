# ./trinity_ai/run_trinity_model.py

import asyncio
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from trinity_ai import initialize_trinity_model
import tensorflow as tf


async def main():
    model = await initialize_trinity_model()
    # ... (rest of your code that uses the model)

if __name__ == "__main__":
    asyncio.run(main())
