import os
import logging
import asyncio
from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker
from app.utils.retry import retry

logger = logging.getLogger(__name__)

@workflow.defn
class SampleWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return f"Hello, {name}!"

class TemporalService:
    def __init__(self):
        self.client = None
        self.worker = None
        self.host = os.getenv("TEMPORAL_HOST", "temporal")
        self.port = int(os.getenv("TEMPORAL_PORT", 7233))
        self.namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
        self._initialized = False

    @retry(max_retries=5, delay=5)
    async def initialize(self):
        try:
            if self._initialized and self.client is not None:
                logger.info("Temporal client already initialized")
                return
            logger.debug(f"Attempting to connect to Temporal at {self.host}:{self.port}, namespace={self.namespace}")
            self.client = await Client.connect(
                f"{self.host}:{self.port}",
                namespace=self.namespace
            )
            if self.client is None:
                raise RuntimeError("Failed to create Temporal client")
            # Start worker
            self.worker = Worker(
                self.client,
                task_queue="test-queue",
                workflows=[SampleWorkflow]
            )
            logger.debug("Starting Temporal worker for test-queue")
            asyncio.create_task(self.worker.run())
            logger.info(f"Initialized Temporal client and worker to {self.host}:{self.port}, namespace={self.namespace}")
            self._initialized = True
        except Exception as e:
            logger.error(f"Temporal initialization failed: {str(e)}")
            self.client = None
            self.worker = None
            self._initialized = False
            raise

    @retry(max_retries=3, delay=2)
    async def test_workflow(self):
        try:
            if self.client is None or not self._initialized:
                logger.error("Temporal client not initialized, attempting to initialize")
                await self.initialize()
            workflow_id = f"test-workflow-{int(os.times().elapsed)}"
            logger.debug(f"Starting workflow with ID: {workflow_id}")
            handle = await self.client.start_workflow(
                SampleWorkflow.run,
                "TestUser",
                id=workflow_id,
                task_queue="test-queue"
            )
            result = await handle.result()
            logger.info(f"Temporal test workflow succeeded: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to execute Temporal test workflow: {str(e)}")
            raise

    async def disconnect(self):
        try:
            if self.worker is not None:
                logger.debug("Shutting down Temporal worker")
                await self.worker.shutdown()
            if self.client is not None and self._initialized:
                self.client = None
                self.worker = None
                self._initialized = False
                logger.info("Disconnected Temporal client and worker")
        except Exception as e:
            logger.error(f"Failed to disconnect Temporal client/worker: {str(e)}")
            raise