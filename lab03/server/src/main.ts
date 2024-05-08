import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap(port: number) {
  const app = await NestFactory.create(AppModule);
  await app.listen(port);
}

if (process.argv.length === 2) {
  console.error('Expected at least one argument!');
  process.exit(1);
}

console.log(__dirname);

bootstrap(parseInt(process.argv[2]));
