import {
  Body,
  Controller,
  Post,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
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
export let tokens = new Map<string, string>();

export function checkAuthorization(
  token: string | undefined,
): string | undefined {
  if (!token) return undefined;
  const user = Array.from(tokens).find(([tk, _]) => tk === token);
  return user ? user[1] : undefined;
}

@Controller('user')
export class UserController {
  constructor() {}

  @Post('sign-up')
  signUp(@Body() userData: UserData): SessionToken {
    if (passwords.has(userData.email)) {
      throw new HttpException(
        'User with this email already exisis',
        HttpStatus.BAD_REQUEST,
      );
    }
    passwords.set(userData.email, userData.password);

    const newToken = generateRandomString(tokenLength);
    tokens.set(userData.email, newToken);
    return {
      token: newToken,
    };
  }

  @Post('sign-in')
  getProduct(@Body() userData: UserData): SessionToken {
    if (
      !passwords.has(userData.email) ||
      passwords.get(userData.email) !== userData.password
    ) {
      throw new HttpException(
        'Account with this credentials does not exists',
        HttpStatus.UNAUTHORIZED,
      );
    }

    const newToken = generateRandomString(tokenLength);
    tokens.set(userData.email, newToken);
    return {
      token: newToken,
    };
  }
}
