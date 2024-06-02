export interface ProductData {
  name: string;
  description: string;
}

export interface Product extends ProductData {
  id: number;
}

export function createProduct(data: ProductData): Product {
  return {
    ...data,
    id: Math.random(),
  };
}
