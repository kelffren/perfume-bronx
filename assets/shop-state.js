const bundles = [
  ["yara", "khamrah"],
  ["yara", "asad"],
  ["khamrah", "asad"],
];
let selectedBundle = null;
const $ = (s) => document.querySelector(s),
  $$ = (s) => document.querySelectorAll(s);
let lang = "es";
try {
  lang = localStorage.getItem("oud-lang") === "en" ? "en" : "es";
} catch {}
let items = readCart(),
  scent = "",
  lastFocus = null,
  lockedScroll = 0;
const t = (es, en) => (lang === "es" ? es : en);
const money = (n) => "$" + n.toFixed(0);
const count = () => Object.values(items).reduce((a, b) => a + b, 0);
const sum = () =>
  catalog.reduce((a, p) => a + (items[p.id] || 0) * p.price, 0) -
  (selectedBundle
    ? Math.max(
        0,
        catalog
          .filter((p) => selectedBundle.includes(p.id))
          .reduce((a, p) => a + p.price, 0) - 55,
      )
    : 0);

function readCart() {
  try {
    const saved = JSON.parse(localStorage.getItem("oud-cart-v1") || "{}");
    return Object.fromEntries(
      catalog.flatMap(({ id }) => {
        const quantity = Number(saved?.[id]);
        return Number.isInteger(quantity) && quantity > 0
          ? [[id, Math.min(99, quantity)]]
          : [];
      }),
    );
  } catch {
    return {};
  }
}
function addBottle(id) {
  if (catalog.some((product) => product.id === id))
    items[id] = Math.min(99, (items[id] || 0) + 1);
}
function syncCart() {
  items = readCart();
  renderCart();
}
window.addEventListener("pageshow", (event) => {
  if (event.persisted) syncCart();
});
window.addEventListener("storage", (event) => {
  if (event.key === "oud-cart-v1" || event.key === null) syncCart();
});
