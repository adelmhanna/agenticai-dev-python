import os
import logging
import paho.mqtt.client as mqtt
import time
import asyncio
from app.utils.retry import retry

logger = logging.getLogger(__name__)

class MosquittoService:
    def __init__(self):
        self.host = os.getenv("MOSQUITTO_HOST", "mosquitto")
        self.port = int(os.getenv("MOSQUITTO_PORT", 1883))
        self.client = mqtt.Client(client_id="mosquitto-service-test")
        self.received_message = None
        self.connected = False
        self._initialized = False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to Mosquitto broker at {self.host}:{self.port}")
            self.connected = True
        else:
            logger.error(f"Connection failed with code {rc}")
            self.connected = False

    def on_message(self, client, userdata, msg):
        self.received_message = msg.payload.decode()
        logger.info(f"Received message: {self.received_message} on topic {msg.topic}")

    @retry(max_retries=5, delay=5)
    async def initialize(self):
        if self._initialized:
            logger.info("Mosquitto client already initialized")
            return
        try:
            logger.info(f"Attempting to connect to Mosquitto at {self.host}:{self.port}")
            self.client.on_connect = self.on_connect
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: self.client.connect(self.host, self.port, keepalive=60))
            self.client.loop_start()
            timeout = 10  # Increased timeout
            start = time.time()
            while not self.connected and time.time() - start < timeout:
                await asyncio.sleep(0.1)
            if not self.connected:
                raise Exception("Failed to connect to Mosquitto broker")
            self._initialized = True
            logger.info("Initialized Mosquitto client")
        except Exception as e:
            logger.error(f"Mosquitto initialization failed: {str(e)}")
            raise

    @retry(max_retries=3, delay=2)
    async def test_pub_sub(self):
        try:
            if not self.connected:
                await self.initialize()
            self.received_message = None
            self.client.on_message = self.on_message
            self.client.subscribe("test/topic", qos=1)
            logger.info("Subscribed to test/topic")
            await asyncio.sleep(0.5)
            self.client.publish("test/topic", "Test message", qos=1)
            logger.info("Published Test message to test/topic")
            timeout = 10
            start = time.time()
            while self.received_message is None and time.time() - start < timeout:
                await asyncio.sleep(0.1)
            if self.received_message:
                logger.info(f"Test successful. Received: {self.received_message}")
                return self.received_message
            raise Exception("No message received within timeout")
        except Exception as e:
            logger.error(f"Failed to perform Mosquitto test pub/sub: {str(e)}")
            raise

    async def disconnect(self):
        try:
            if self.connected:
                self.client.loop_stop()
                self.client.disconnect()
                self.connected = False
                self._initialized = False
                logger.info("Disconnected from Mosquitto broker")
        except Exception as e:
            logger.error(f"Failed to disconnect Mosquitto client: {str(e)}")
            raise

    def __del__(self):
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()