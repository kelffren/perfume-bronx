let favorites = [];
try {
  const saved = JSON.parse(localStorage.getItem("oud-favorites-v1") || "[]");
  if (Array.isArray(saved))
    favorites = saved.filter((id) => catalog.some((p) => p.id === id));
} catch {}
let favoritesOnly = false,
  recentlyViewed = [];
try {
  const ids = JSON.parse(localStorage.getItem("oud-recent-v1") || "[]");
  if (Array.isArray(ids))
    recentlyViewed = ids
      .filter((id) => catalog.some((p) => p.id === id))
      .slice(0, 3);
} catch {}
function rememberProduct(id) {
  if (!catalog.some((p) => p.id === id)) return;
  recentlyViewed = [id, ...recentlyViewed.filter((x) => x !== id)].slice(0, 3);
  try {
    localStorage.setItem("oud-recent-v1", JSON.stringify(recentlyViewed));
  } catch {}
  renderRecent();
}
function renderRecent() {
  const root = $("#recentlyViewed");
  if (!root) return;
  root.replaceChildren();
  root.hidden = !recentlyViewed.length;
  if (root.hidden) return;
  const label = document.createElement("strong");
  label.textContent = t("Vistos recientemente: ", "Recently viewed: ");
  root.append(label);
  recentlyViewed.forEach((id) => {
    const p = catalog.find((x) => x.id === id);
    if (!p) return;
    const a = document.createElement("a");
    a.href = lang + "/products/" + p.id + "/";
    a.textContent = p.name.replace("Lattafa ", "");
    a.addEventListener("click", () => rememberProduct(id));
    root.append(a);
  });
}
function updateCollectionFilters() {
  const fav = $("#favoritesFilter"),
    all = $("#allProductsFilter");
  fav.setAttribute("aria-pressed", String(favoritesOnly));
  all.setAttribute("aria-pressed", String(!favoritesOnly));
  fav.textContent =
    t("♡ Mis favoritos", "♡ My favorites") + " (" + favorites.length + ")";
  all.textContent = t("Todos los perfumes", "All fragrances");
  renderRecent();
}
function toggleFavorite(id) {
  if (!catalog.some((p) => p.id === id)) return;
  favorites = favorites.includes(id)
    ? favorites.filter((x) => x !== id)
    : [...favorites, id];
  try {
    localStorage.setItem("oud-favorites-v1", JSON.stringify(favorites));
  } catch {}
  trackFunnel("favorite_toggle");
  renderProducts();
}
function setLang(l) {
  lang = l;
  document
    .querySelectorAll("[data-guide-path]")
    .forEach((a) => (a.href = l + "/" + a.dataset.guidePath));
  document.querySelector("#organicGuideLink").href = l + "/";
  document
    .querySelectorAll("[data-tool-route]")
    .forEach((a) => (a.href = l + "/" + a.dataset.toolRoute + "/"));
  document.querySelector("#academyAllLink").href = l + "/academy/";
  document
    .querySelectorAll("[data-compare-product]")
    .forEach(
      (a) => (a.href = l + "/products/" + a.dataset.compareProduct + "/"),
    );
  document.documentElement.lang = l;
  try {
    localStorage.setItem("oud-lang", l);
  } catch {}
  $$("[data-es][data-en]").forEach((el) => (el.textContent = el.dataset[l]));
  $("#langBtn").textContent = l.toUpperCase() + " ⌄";
  setPopover("lang", false);
  renderProducts();
  renderBundles();
  renderCart();
  renderGuide();
  document.dispatchEvent(new Event("oud-language"));
}
function renderProducts() {
  updateCollectionFilters();
  $("#products").innerHTML = catalog
    .filter((p) => !favoritesOnly || favorites.includes(p.id))
    .map(
      (p, i) =>
        '<article id="perfume-' +
        p.id +
        '" tabindex="-1" class="tile reveal visible"><a class="art product-photo" href="' +
        lang +
        "/products/" +
        p.id +
        '/" aria-label="' +
        p.name +
        '"><img src="' +
        p.image +
        '" alt="' +
        p.name +
        '" loading="lazy" decoding="async" width="512" height="512"><small>' +
        t("Foto de referencia", "Reference photo") +
        '</small></a><div class="content"><div class="eyebrow">OUD BRONX · 0' +
        (i + 1) +
        '</div><h3><a href="' +
        lang +
        "/products/" +
        p.id +
        '/">' +
        p.name +
        '</a></h3><p class="muted">' +
        p[lang] +
        '</p><div class="price">' +
        money(p.price) +
        '</div><a class="photo-source" href="' +
        p.source +
        '" target="_blank" rel="noopener noreferrer">' +
        t("Fuente de imagen ↗", "Image source ↗") +
        '</a><button type="button" class="favorite-btn" data-favorite="' +
        p.id +
        '" aria-pressed="' +
        favorites.includes(p.id) +
        '" aria-label="' +
        (favorites.includes(p.id)
          ? t("Quitar de favoritos: ", "Remove favorite: ")
          : t("Guardar favorito: ", "Save favorite: ")) +
        p.name +
        '">' +
        (favorites.includes(p.id) ? "♥" : "♡") +
        " " +
        t("Favorito", "Favorite") +
        '</button><button class="btn" data-add="' +
        p.id +
        '">' +
        t("Añadir a mi pedido +", "Add to my order +") +
        "</button></div></article>",
    )
    .join("");
}
function renderBundles() {
  $("#packsGrid").innerHTML = bundles
    .map((pair, i) => {
      const a = catalog.find((p) => p.id === pair[0]),
        b = catalog.find((p) => p.id === pair[1]);
      return (
        '<article class="tile pack-tile"><div class="pack-images"><img src="' +
        a.image +
        '" alt="' +
        a.name +
        '" loading="lazy" decoding="async" width="170" height="170"><img src="' +
        b.image +
        '" alt="' +
        b.name +
        '" loading="lazy" decoding="async" width="170" height="170"></div><div class="content"><div class="eyebrow">' +
        t("PACK · DELIVERY GRATIS", "BUNDLE · FREE DELIVERY") +
        "</div><h3>" +
        a.name.replace("Lattafa ", "") +
        " + " +
        b.name.replace("Lattafa ", "") +
        '</h3><div class="price pack-price"><span class="pack-price-current">$55</span><span class="old-price">' +
        money(a.price + b.price) +
        '</span></div><div class="pack-quantity">' +
        t("2 unidades", "2 bottles") +
        '</div><button class="btn" data-pack="' +
        i +
        '">' +
        t("Elegir pack y pedir →", "Choose bundle →") +
        "</button></div></article>"
      );
    })
    .join("");
}
function renderGuide() {
  if (window.oudQuizRender) window.oudQuizRender(lang);
}
function setPopover(kind, open) {
  const menu = kind === "lang" ? $("#langMenu") : $("#menu"),
    button = kind === "lang" ? $("#langBtn") : $("#menuBtn");
  menu.classList.toggle("open", open);
  menu.inert = !open;
  button.setAttribute("aria-expanded", String(open));
}
$("#confidenceHelp").addEventListener("click", () => {
  trackFunnel("trust_questions_click");
  openWhatsApp(
    t(
      "Hola Oud Bronx, quisiera confirmar fotos actuales, autenticidad, entrega y condiciones antes de pedir.",
      "Hi Oud Bronx, I would like to confirm current photos, authenticity, delivery and terms before ordering.",
    ),
  );
});
$("#oudHelp").addEventListener("click", () => {
  trackFunnel("customer_service_click");
  openWhatsApp(
    t(
      "Hola Oud Bronx, necesito ayuda para elegir un perfume.",
      "Hi Oud Bronx, I need help choosing a fragrance.",
    ),
  );
});
$("#packsGrid").addEventListener("click", (e) => {
  const b = e.target.closest("[data-pack]");
  if (!b) return;
  trackFunnel("bundle_select");
  const pair = bundles[Number(b.dataset.pack)];
  if (
    count() > 0 &&
    !confirm(
      t(
        "Este pack sustituye tu selección actual. ¿Continuar?",
        "This bundle replaces your current selection. Continue?",
      ),
    )
  )
    return;
  items = {};
  items[pair[0]] = 1;
  items[pair[1]] = 1;
  selectedBundle = pair;
  renderCart();
  openSheet();
});
$("#favoritesFilter").addEventListener("click", () => {
  favoritesOnly = true;
  trackFunnel("favorites_filter");
  renderProducts();
});
$("#allProductsFilter").addEventListener("click", () => {
  favoritesOnly = false;
  renderProducts();
});
$("#products").addEventListener("click", (e) => {
  const link = e.target.closest('a[href*="/products/"]');
  if (link) {
    const card = link.closest("[id^=perfume-]");
    if (card) rememberProduct(card.id.replace("perfume-", ""));
  }
  const fav = e.target.closest("[data-favorite]");
  if (fav) {
    toggleFavorite(fav.dataset.favorite);
    return;
  }
  const b = e.target.closest("[data-add]");
  if (!b) return;
  trackFunnel("individual_select");
  selectedBundle = null;
  items[b.dataset.add] = Math.min(99, (items[b.dataset.add] || 0) + 1);
  renderCart();
  openSheet();
});
["orderBtn", "stickyOrder", "howOrder", "endOrder"].forEach((id) =>
  $("#" + id).addEventListener("click", openSheet),
);
$("#menuBtn").onclick = () => {
  setPopover("lang", false);
  setPopover("menu", !$("#menu").classList.contains("open"));
};
$$(".menu a").forEach((a) => (a.onclick = () => setPopover("menu", false)));
$("#langBtn").onclick = () => {
  setPopover("menu", false);
  setPopover("lang", !$("#langMenu").classList.contains("open"));
};
$("#langMenu").onclick = (e) => {
  const b = e.target.closest("[data-lang]");
  if (b) setLang(b.dataset.lang);
};
document.addEventListener("click", (e) => {
  if (!e.target.closest("#menu,#menuBtn")) setPopover("menu", false);
  if (!e.target.closest("#langMenu,#langBtn")) setPopover("lang", false);
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeSheet();
    if ($("#menu").classList.contains("open")) $("#menuBtn").focus();
    if ($("#langMenu").classList.contains("open")) $("#langBtn").focus();
    setPopover("menu", false);
    setPopover("lang", false);
  }
});
const motion = matchMedia("(prefers-reduced-motion: reduce)");
const entryParams = new URLSearchParams(location.search);
if (["es", "en"].includes(entryParams.get("lang")))
  lang = entryParams.get("lang");
setLang(lang);
setPopover("menu", false);
setPopover("lang", false);
if ("IntersectionObserver" in window) {
  const obs = new IntersectionObserver(
    (entries) =>
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("visible");
          obs.unobserve(e.target);
        }
      }),
    { threshold: 0, rootMargin: "0px 0px 32px 0px" },
  );
  $$(".reveal").forEach((el) => {
    if (!motion.matches && el.getBoundingClientRect().top > innerHeight) {
      el.classList.remove("visible");
      el.classList.add("motion-pending");
      obs.observe(el);
    }
  });
  motion.addEventListener("change", () => {
    if (motion.matches) {
      $$(".motion-pending").forEach((el) => el.classList.add("visible"));
      obs.disconnect();
    }
  });
  const stickyObs = new IntersectionObserver(
    (entries) => {
      const show = entries[0].boundingClientRect.bottom <= 70;
      $("#sticky").classList.toggle("show", show);
      $("#sticky").inert = !show || $("#sheet").classList.contains("open");
    },
    { rootMargin: "-70px 0px 0px 0px", threshold: 0 },
  );
  stickyObs.observe($("#home"));
}
document
  .querySelector(".hero-primary")
  ?.addEventListener("click", () => trackFunnel("hero_shop_click"));
document
  .querySelector(".hero-secondary")
  ?.addEventListener("click", () => trackFunnel("hero_quiz_click"));
document
  .querySelector(".hero-bundle-link")
  ?.addEventListener("click", () => trackFunnel("hero_bundle_click")); // Reveal WhatsApp only after the second content section (#packs) is passed.
function updateHelpVisibility() {
  const help = document.querySelector("#oudHelp"),
    results = document.querySelector("#scentQuiz .quiz-results");
  if (!help) return;
  const active =
    !!results &&
    results.getBoundingClientRect().top < innerHeight * 0.85 &&
    results.getBoundingClientRect().bottom > 0;
  help.hidden = !active || !!document.querySelector("#sheet.open");
}
window.addEventListener("scroll", updateHelpVisibility, { passive: true });
window.addEventListener("resize", updateHelpVisibility);
new MutationObserver(updateHelpVisibility).observe(
  document.querySelector("#scentQuiz"),
  { childList: true, subtree: false },
);
updateHelpVisibility();

const entryProduct = catalog.find((p) => p.id === entryParams.get("product"));
if (entryParams.get("intent") === "inquiry" && entryProduct) {
  items[entryProduct.id] = Math.max(1, items[entryProduct.id] || 0);
  renderCart();
  openSheet();
  trackFunnel("organic_product_inquiry");
}
$("#year").textContent = new Date().getFullYear();
const landingProduct = new URLSearchParams(location.search).get("product");
if (
  entryParams.get("intent") !== "inquiry" &&
  catalog.some((p) => p.id === landingProduct)
) {
  requestAnimationFrame(() => {
    const el = document.getElementById("perfume-" + landingProduct);
    el.scrollIntoView({ behavior: "instant", block: "start" });
    el.focus({ preventScroll: true });
    trackFunnel("product_landing_" + landingProduct);
  });
}
