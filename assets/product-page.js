(() => {
  const id = document.body.dataset.product;
  lang = document.documentElement.lang;
  try {
    localStorage.setItem("oud-lang", lang);
  } catch {}
  for (const node of $("#sheet").querySelectorAll("[data-es][data-en]")) {
    node.textContent = node.dataset[lang];
  }
  $("#closeSheet").ariaLabel = t("Cerrar pedido", "Close order");
  $("#productOrder").addEventListener("click", openSheet);
  for (const button of $$(".product-add")) {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      addBottle(id);
      trackFunnel("individual_select");
      openSheet();
    });
  }
  const bar = $(".product-bar");
  const primary = $(".product .product-add");
  new IntersectionObserver(
    ([entry]) => {
      bar.hidden = entry.boundingClientRect.bottom > 70;
    },
    { rootMargin: "-70px 0px 0px 0px" },
  ).observe(primary);
  renderCart();
})();
