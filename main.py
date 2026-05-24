import asyncio
from config import VKU_URL, UDN_URL, UED_URL, DUT_URL, DUE_URL, UFL_URL, UTE_URL, SMP_URL

from pipeline.school_pipeline import (
    run_school_pipeline
)
from normalized.nomalized import (
    normalized
)

async def main():

    await run_school_pipeline(VKU_URL[0])

    if await normalized(VKU_URL[1]
                        
                        ):
        print("Pipeline completed successfully.")
    


asyncio.run(main())