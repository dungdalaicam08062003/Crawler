import asyncio

from pipeline.school_pipeline import (
    run_school_pipeline
)


async def main():

    await run_school_pipeline()


    


asyncio.run(main())