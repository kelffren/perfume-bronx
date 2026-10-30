import {loadBaseCatalog} from "./catalog-data.js";
const KEY="oud-commerce-catalog-v1";
let base=[];
export async function initCatalog(){base=await loadBaseCatalog();return getCatalog()}
export function getCatalog(){let overrides={};try{const saved=JSON.parse(localStorage.getItem(KEY)||"{}");overrides=Array.isArray(saved)?Object.fromEntries(saved.map(p=>[p.sku,p])):saved}catch{}return base.map(p=>({...p,...(overrides[p.sku]||{})}))}
export function updateProduct(sku,changes){const p=getCatalog().find(x=>x.sku===sku);if(!p)throw Error("Producto desconocido");if(!Number.isInteger(changes.stock)||changes.stock<0||changes.stock>100000)throw Error("Stock inválido");if(!Number.isFinite(changes.price)||changes.price<0||changes.price>100000)throw Error("Precio inválido");const list=getCatalog();const product=list.find(x=>x.sku===sku);product.stock=changes.stock;product.price=Math.round(changes.price*100)/100;localStorage.setItem(KEY,JSON.stringify(list));return product}
