import { Module } from '@nestjs/common';
import {
  ProductListController,
  ProductController,
} from './app.product_controller';

@Module({
  imports: [],
  controllers: [ProductController, ProductListController],
  providers: [],
})
export class AppModule {}
