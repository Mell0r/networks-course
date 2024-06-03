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
import { checkAuthorization } from './app.user_controller';

let publicProducts: Product[] = [];
let usersProducts = new Map<string, Product[]>();

@Controller('/product')
export class ProductController {
  constructor() {}

  @Post(':token?')
  addProduct(
    @Param('token') token: string | undefined,
    @Body() productData: ProductData,
  ): Product {
    const product = createProduct(productData);
    const maybeUser = checkAuthorization(token);
    if (maybeUser) usersProducts[maybeUser].push(product);
    else publicProducts.push(product);
    return product;
  }

  @Get(':id/:token?')
  getProduct(
    @Param('id') id: number,
    @Param('token') token: string | undefined,
  ): Product {
    const availableProducts = publicProducts.concat(
      token ? usersProducts.get(token) ?? [] : [],
    );
    const product = availableProducts.find((value) => value.id == id);
    if (!product) {
      throw new HttpException(
        'Product with this id is not found',
        HttpStatus.NOT_FOUND,
      );
    }
    return product;
  }

  @Put(':id/:token?')
  updateProduct(
    @Param('id') id: number,
    @Param('token') token: string | undefined,
    @Body() newData: Partial<Product>,
  ): Product {
    let changedProduct: Product | undefined = undefined;

    publicProducts = publicProducts.map((value) => {
      if (value.id == id) {
        changedProduct = { ...value, ...newData };
        return changedProduct;
      } else {
        return value;
      }
    });

    const maybeUser = checkAuthorization(token);
    if (maybeUser) {
      if (!usersProducts.has(maybeUser)) {
        usersProducts.set(maybeUser, []);
      }
      usersProducts.get(maybeUser)!!.map((value) => {
        if (value.id == id) {
          changedProduct = { ...value, ...newData };
          return changedProduct;
        } else {
          return value;
        }
      });
    }

    if (!changedProduct) {
      throw new HttpException(
        'Product with this id is not found',
        HttpStatus.NOT_FOUND,
      );
    }
    return changedProduct;
  }

  @Delete(':id/:token?')
  deleteProduct(
    @Param('id') id: number,
    @Param('token') token: string | undefined,
  ): Product {
    let product: Product | undefined = undefined;

    product = publicProducts.find((value) => value.id == id);
    publicProducts = publicProducts.filter((value) => value.id == id);

    const maybeUser = checkAuthorization(token);
    if (maybeUser && usersProducts.has(maybeUser)) {
      product = usersProducts.get(maybeUser)!!.find((value) => value.id == id);
      usersProducts.set(
        maybeUser,
        usersProducts.get(maybeUser)!!.filter((value) => value.id == id),
      );
    }

    if (!product) {
      throw new HttpException(
        'Product with this id is not found',
        HttpStatus.NOT_FOUND,
      );
    }
    return product;
  }
}

@Controller('/products')
export class ProductListController {
  constructor() {}

  @Get(':token?')
  getList(@Param('token') token: string | undefined): Product[] {
    return publicProducts.concat(token ? usersProducts.get(token) ?? [] : []);
  }
}
