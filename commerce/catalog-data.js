/* Shared catalogue source for prototype UI. No live stock or sales claims. */
export async function loadBaseCatalog(){const response=await fetch(new URL("./catalog.json",import.meta.url),{cache:"no-store"});if(!response.ok)throw Error("Catálogo no disponible");const data=await response.json();if(!Array.isArray(data.products))throw Error("Catálogo inválido");return data.products}
