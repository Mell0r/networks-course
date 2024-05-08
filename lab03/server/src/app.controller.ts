import { Controller, Get, HttpException, Param, Res } from '@nestjs/common';
import { AppService } from './app.service';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get(':filename')
  async getContent(@Param('filename') filename: string): Promise<string> {
    console.log(`get file request on path: ${resolve('')}`);
    return readFile(`./resources/${filename}`, { encoding: 'utf8' }).catch(
      (err) => {
        console.error(err.toString());
        throw new HttpException('File not found', 404);
      },
    );
  }
}
