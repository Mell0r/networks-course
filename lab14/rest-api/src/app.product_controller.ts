import {
  Body,
  Controller,
  Delete,
  Get,
  HttpException,
  HttpStatus,
  Ip,
  Param,
  Post,
  Put,
} from '@nestjs/common';
import { Product, ProductData, createProduct } from './product';
import { checkAuthorization, emailByIp } from './app.user_controller';
import { sendGreetings } from './mail';

let publicProducts: Product[] = [];
let usersProducts = new Map<string, Product[]>();
function mapUsersProducts(user: string, func: (prod: Product) => Product) {
  usersProducts.set(user, (usersProducts.get(user) ?? []).map(func));
}
function pushUsersProducts(user: string, product: Product) {
  usersProducts.set(user, usersProducts.get(user) ?? []);
  usersProducts.get(user)!!.push(product);
}

let timeouts = new Map<string, NodeJS.Timeout>();
function setEmailTimeout(token: string | undefined, ip: string | undefined) {
  if (!token && ip) {
    const email = emailByIp.get(ip);
    console.log(`Saved email: ${email}`);
    if (email) {
      if (timeouts.has(email)) {
        clearTimeout(timeouts.get(email)!!);
      }
      timeouts.set(
        email,
        setTimeout(() => {
          sendGreetings(email);
          timeouts.delete(email);
        }, 60000),
      );
    }
  }
}

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

    if (maybeUser) pushUsersProducts(maybeUser, product);
    else publicProducts.push(product);
    return product;
  }

  @Get(':id/:token?')
  getProduct(
    @Param('id') id: number,
    @Param('token') token: string | undefined,
    @Ip() ip: string | undefined,
  ): Product {
    setEmailTimeout(token, ip);

    const maybeUser = checkAuthorization(token);
    const availableProducts = publicProducts.concat(
      maybeUser ? usersProducts.get(maybeUser) ?? [] : [],
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
    const modifyProducts = (value: Product) => {
      if (value.id == id) {
        changedProduct = { ...value, ...newData };
        return changedProduct;
      } else {
        return value;
      }
    };

    publicProducts = publicProducts.map(modifyProducts);

    const maybeUser = checkAuthorization(token);
    if (maybeUser) {
      mapUsersProducts(maybeUser, modifyProducts);
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
    publicProducts = publicProducts.filter((value) => value.id != id);

    const maybeUser = checkAuthorization(token);
    if (maybeUser && usersProducts.has(maybeUser)) {
      product = usersProducts.get(maybeUser)!!.find((value) => value.id == id);
      usersProducts.get(maybeUser)!!.filter((value) => value.id != id);
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
  getList(
    @Param('token') token: string | undefined,
    @Ip() ip: string | undefined,
  ): Product[] {
    setEmailTimeout(token, ip);
    return publicProducts.concat(token ? usersProducts.get(token) ?? [] : []);
  }
}
