import { Module } from '@nestjs/common';
import {
  ProductListController,
  ProductController,
} from './app.product_controller';
import { UserController } from './app.user_controller';

@Module({
  imports: [],
  controllers: [ProductController, ProductListController, UserController],
  providers: [],
})
export class AppModule {}
