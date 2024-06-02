import { Body, Controller, Get, HttpException } from '@nestjs/common';
import { SessionToken, UserData } from './user';

const tokenLength = 40;

function generateRandomString(length: number): string {
  const characters =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

let passwords = new Map<string, string>();
let tokens = new Map<string, string>();

@Controller('/user')
export class UserController {
  constructor() {}

  @Get('/sign-up')
  signUp(@Body() userData: UserData): SessionToken {
    if (passwords.has(userData.email)) {
      throw new HttpException('User with this email already exisis');
    }
    if (passwords.userData) passwords[userData.email] = userData.password;
    const newToken = {
      token: generateRandomString(tokenLength),
    };
    tokens[userData.email] = newToken;
    return newToken;
  }

  @Get('/sign-in')
  getProduct(@Body() userData: UserData): SessionToken {
    return product;
  }
}
