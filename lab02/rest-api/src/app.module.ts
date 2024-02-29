import { Module } from '@nestjs/common';
import { ProductListController, ProductController } from './app.controller';

@Module({
  imports: [],
  controllers: [ProductController, ProductListController],
  providers: [],
})
export class AppModule {}
