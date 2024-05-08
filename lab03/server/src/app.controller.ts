import { Controller, Get, HttpException, Param } from '@nestjs/common';
import { AppService } from './app.service';
import { Worker } from 'node:worker_threads';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get(':filename')
  async getContent(@Param('filename') filename: string): Promise<string> {
    console.log(`get file request with name: ${filename}`);

    const resultPromise: Promise<string> = new Promise((resolve, reject) => {
      const worker = new Worker('./src/worker/worker.ts', {
        workerData: { filename: filename },
      });
      worker.on('message', (fileContent) => {
        resolve(fileContent);
      });
      worker.on('error', (err) => reject(err));
    });

    return resultPromise.catch((err) => {
      throw new HttpException('File not found', 404);
    });
  }
}
