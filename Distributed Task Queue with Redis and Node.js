const Redis = require('ioredis');
const { v4: uuidv4 } = require('uuid');

class DistributedTaskQueue {
  constructor(redisConfig = { host: 'localhost', port: 6379 }) {
    this.redis = new Redis(redisConfig);
    this.queueKey = 'distributed_task_queue';
    this.processingQueueKey = 'processing_tasks';
    this.workers = new Set();
  }

  async addTask(taskData, priority = 0) {
    const taskId = uuidv4();
    const task = JSON.stringify({
      id: taskId,
      data: taskData,
      priority,
      timestamp: Date.now()
    });
    
    await this.redis.zadd(this.queueKey, priority, task);
    return taskId;
  }

  async processTasks(workerId, handler, batchSize = 5) {
    this.workers.add(workerId);
    
    while (this.workers.has(workerId)) {
      const tasks = await this.redis.eval(
        `local tasks = redis.call('zrange', KEYS[1], 0, ARGV[1]-1, 'WITHSCORES')
         if #tasks > 0 then
           redis.call('zremrangebyrank', KEYS[1], 0, ARGV[1]-1)
           for i, task in ipairs(tasks) do
             if i % 2 == 1 then
               redis.call('lpush', KEYS[2], task)
             end
           end
         end
         return tasks`,
        2,
        this.queueKey,
        this.processingQueueKey,
        batchSize
      );

      if (tasks && tasks.length > 0) {
        for (let i = 0; i < tasks.length; i += 2) {
          try {
            const task = JSON.parse(tasks[i]);
            await handler(task.data);
            await this.redis.lrem(this.processingQueueKey, 1, tasks[i]);
          } catch (error) {
            console.error(`Task failed: ${error}`);
            // Implement retry logic or dead-letter queue here
          }
        }
      } else {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
  }

  async stopWorker(workerId) {
    this.workers.delete(workerId);
  }
}

// Usage Example:
const queue = new DistributedTaskQueue();

// Producer
queue.addTask({ type: 'image_processing', file: 'photo1.jpg' }, 1);

// Consumer
queue.processTasks('worker1', async (task) => {
  console.log('Processing task:', task);
  // Simulate work
  await new Promise(resolve => setTimeout(resolve, 2000));
});