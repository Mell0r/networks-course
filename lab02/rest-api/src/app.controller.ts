import {
  Body,
  Controller,
  Delete,
  Get,
  HttpException,
  HttpStatus,
  Param,
  Post,
  Put,
} from '@nestjs/common';
import { Product, ProductData, createProduct } from './product';

let products: Product[] = [];

@Controller('/product')
export class ProductController {
  constructor() {}

  @Post('')
  addProduct(@Body() productData: ProductData): Product {
    const product = createProduct(productData);
    products.push(product);
    return product;
  }

  @Get(':id')
  getProduct(@Param('id') id: number): Product {
    const product = products.find((value) => value.id == id);
    if (!product) {
      throw new HttpException('Product with this id is not found', HttpStatus.NOT_FOUND);
    }
    return product;
  }

  @Put(':id')
  updateProduct(@Param('id') id: number, @Body() newData: Partial<Product>): Product {
    let changedProduct: Product | undefined = undefined;
    products = products.map((value) => {
      if (value.id == id) {
        changedProduct = { ...value, ...newData };
        return changedProduct;
      } else {
        return value;
      }
    });
    if (!changedProduct) {
      throw new HttpException('Product with this id is not found', HttpStatus.NOT_FOUND);
    }
    return changedProduct;
  }

  @Delete(':id')
  deleteProduct(@Param('id') id: number): Product {
    const product = products.find((value) => value.id == id);
    products = products.filter((value) => value.id == id);
    if (!product) {
      throw new HttpException('Product with this id is not found', HttpStatus.NOT_FOUND);
    }
    return product;
  }
}

@Controller('/products')
export class ProductListController {
  constructor() {}

  @Get('')
  getList(): Product[] {
    return products;
  }
}
