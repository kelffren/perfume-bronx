/* Prototype catalogue for the Commerce Lab; not the public storefront source of truth. */
const KEY="oud-commerce-catalog-v1";
const DEFAULT=[{sku:"yara",name:"Lattafa Yara",price:25,stock:0},{sku:"khamrah",name:"Lattafa Khamrah",price:35,stock:0},{sku:"asad",name:"Lattafa Asad",price:35,stock:0}];
export function getCatalog(){try{const saved=JSON.parse(localStorage.getItem(KEY)||"null");return Array.isArray(saved)?saved:structuredClone(DEFAULT)}catch{return structuredClone(DEFAULT)}}
export function updateProduct(sku,changes){const list=getCatalog(),p=list.find(x=>x.sku===sku);if(!p)throw Error("Producto desconocido");if(!Number.isInteger(changes.stock)||changes.stock<0||changes.stock>100000)throw Error("Stock inválido");if(!Number.isFinite(changes.price)||changes.price<0||changes.price>100000)throw Error("Precio inválido");p.stock=changes.stock;p.price=Math.round(changes.price*100)/100;localStorage.setItem(KEY,JSON.stringify(list));return p}
