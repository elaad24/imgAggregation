import Redis from "ioredis";

const redis = new Redis({
  host: process.env.REDIS_HOST || "localhost",
  port: Number(process.env.REDIS_PORT) || 6379,
});

export async function processMessage(data: any) {
  console.log("Processing message:", data);
  // Your processing logic here
}

export async function listenToQueue(
  queueName: string,
  functionToExecute: (data: string[]) => void
) {
  console.log(`Listening to ${queueName} queue...`);

  while (true) {
    const message = await redis.blpop(queueName, 0); // 0 means wait indefinitely
    if (message) {
      const [, data] = message; // message[1] contains the data
      try {
        const parsedData = JSON.parse(data);
        await functionToExecute(parsedData);
      } catch (error) {
        console.error("Error processing message:", error);
      }
    }
  }
}

export async function pushToQueue(queueName: string, message: any) {
  try {
    // Convert message to a JSON string and push it to the specified queue
    await redis.rpush(queueName, JSON.stringify(message));
    console.log(`Message dispatched to ${queueName}:`, message);
  } catch (error) {
    console.error("Error pushing to queue:", error);
  }
}
