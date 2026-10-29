/* OUD BRONX Commerce: explicit backend selection, no silent loss of orders. */
export const BACKENDS=Object.freeze({LOCAL:"local",CLOUD:"cloud",SQLITE:"sqlite"});
const params=new URLSearchParams(location.search);
const requested=params.get("backend");
const stored=localStorage.getItem("oud-commerce-backend");
export const mode=(Object.values(BACKENDS).includes(requested)?requested:stored)||BACKENDS.LOCAL;
export function setMode(next){if(!Object.values(BACKENDS).includes(next))throw Error("Invalid backend");localStorage.setItem("oud-commerce-backend",next);location.reload();}
export const cloudUrl=mode==="sqlite"?"http://127.0.0.1:8765":(window.OUD_COMMERCE_API_URL||"");
