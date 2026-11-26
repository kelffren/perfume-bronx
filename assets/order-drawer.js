function renderCart() {
  try {
    localStorage.setItem("oud-cart-v1", JSON.stringify(items));
  } catch {}
  const n = count();
  selectedBundle =
    n === 2
      ? bundles.find((pair) => pair.every((id) => items[id] === 1)) || null
      : null;
  $("#badge").textContent = n || "";
  if ($("#stickyLabel"))
    $("#stickyLabel").textContent = n
      ? t("Tu selección · ", "Your selection · ") + n + " · " + money(sum())
      : t("Pack 2 × $55", "2 for $55");
  $("#cart").innerHTML =
    catalog
      .filter((p) => items[p.id] > 0)
      .map(
        (p) =>
          '<div class="cartline"><img class="cart-thumb" src="' +
          p.image +
          '" alt="" loading="lazy"><div class="cart-info"><strong>' +
          p.name +
          '</strong><div class="muted">' +
          money(p.price) +
          " × " +
          items[p.id] +
          '</div></div><div><button type="button" data-dec="' +
          p.id +
          '" aria-label="' +
          t("Quitar uno", "Remove one") +
          '">−</button><strong style="padding:0 9px">' +
          items[p.id] +
          '</strong><button type="button" data-add="' +
          p.id +
          '" aria-label="' +
          t("Añadir uno", "Add one") +
          '">+</button></div></div>',
      )
      .join("") ||
    '<div class="cart-empty"><div class="cart-empty-icon" aria-hidden="true">✦</div><h4>' +
      t(
        "Tu carrito está esperando su primer aroma",
        "Your cart is waiting for its first fragrance",
      ) +
      "</h4><p>" +
      t(
        "Elige un perfume para empezar. Los packs de dos tienen delivery gratis en zonas confirmadas.",
        "Choose a fragrance to start. Two-bottle orders qualify for free delivery in confirmed areas.",
      ) +
      '</p><div class="cart-picks">' +
      catalog
        .map(
          (p) =>
            '<button type="button" class="cart-pick" data-add="' +
            p.id +
            '"><img src="' +
            p.image +
            '" alt="" loading="lazy"><span><strong>' +
            p.name.replace("Lattafa ", "") +
            "</strong><small>" +
            money(p.price) +
            '</small></span><b aria-hidden="true">+</b></button>',
        )
        .join("") +
      "</div></div>";
  $("#total").hidden = n === 0;
  $("#deliveryNote").hidden = n === 0;
  $("#complement").hidden = n === 0;
  $("#deliveryDetails").hidden = n === 0;
  $(".order-path").hidden = n === 0;
  $("#sheet").classList.toggle("is-empty", n === 0);
  $("#total").textContent =
    t("Subtotal orientativo: ", "Estimated subtotal: ") +
    money(sum()) +
    (selectedBundle ? t(" · Pack $55 aplicado", " · $55 bundle applied") : "");
  $("#deliveryNote").textContent =
    n >= 2
      ? t(
          "Delivery gratis para 2+ unidades en zonas confirmadas. Sujeto a confirmación.",
          "Free delivery for 2+ bottles in confirmed service areas. Subject to confirmation.",
        )
      : t(
          "Con 1 unidad, el delivery tiene costo por confirmar. Gratis desde 2 unidades.",
          "Single-bottle delivery fee to be confirmed. Free from 2 bottles.",
        );
  $("#submitOrder").disabled = n === 0 && !scent;
  $("#submitOrder").textContent =
    n === 0
      ? t("Elige un perfume para continuar", "Choose a fragrance to continue")
      : t("Enviar pedido por WhatsApp ↗", "Send order via WhatsApp ↗");
  const progress = $("#cartProgress");
  if (progress) {
    progress.hidden = n === 0;
    progress.textContent =
      n >= 2
        ? t(
            "✓ Delivery gratis sujeto a zona confirmada",
            "✓ Free delivery in confirmed areas",
          )
        : t(
            "Añade 1 perfume más para delivery gratis",
            "Add 1 more fragrance for free delivery",
          );
  }
  renderComplement();
}
const background = () =>
  [...document.body.children].filter(
    (el) =>
      !["sheet", "shade"].includes(el.id) &&
      !["SCRIPT", "STYLE"].includes(el.tagName),
  );
function openSheet() {
  if ($("#oudHelp")) $("#oudHelp").hidden = true;
  if ($("#sheet").classList.contains("open")) return;
  lastFocus = document.activeElement;
  if ($("#menu")) {
    setPopover("menu", false);
    setPopover("lang", false);
  }
  lockedScroll = scrollY;
  document.body.style.top = `-${lockedScroll}px`;
  document.body.classList.add("lock");
  $("#sheet").inert = false;
  $("#sheet").setAttribute("aria-hidden", "false");
  $("#sheet").classList.add("open");
  $("#shade").classList.add("open");
  renderCart();
  $("#closeSheet").focus({ preventScroll: true });
  background().forEach((el) => (el.inert = true));
}
function closeSheet() {
  if (!$("#sheet").classList.contains("open")) return;
  $("#sheet").classList.remove("open");
  $("#shade").classList.remove("open");
  background().forEach((el) => (el.inert = false));
  if ($("#menu")) {
    setPopover("menu", false);
    setPopover("lang", false);
  }
  if ($("#sticky"))
    $("#sticky").inert = !$("#sticky").classList.contains("show");
  document.body.classList.remove("lock");
  document.body.style.top = "";
  const root = document.documentElement;
  root.style.scrollBehavior = "auto";
  window.scrollTo(0, lockedScroll);
  root.style.scrollBehavior = "";
  lastFocus?.focus({ preventScroll: true });
  $("#sheet").inert = true;
  $("#sheet").setAttribute("aria-hidden", "true");
  $("#status").textContent = "";
  if (typeof updateHelpVisibility === "function") updateHelpVisibility();
}
function makeMessage(d) {
  const rows = catalog
    .filter((p) => items[p.id] > 0)
    .map(
      (p) =>
        "- " +
        p.name +
        " × " +
        items[p.id] +
        " (" +
        money(p.price) +
        t(" por unidad)", " each)"),
    );
  const details = [
    ["name", t("Nombre", "Name")],
    ["phone", t("Teléfono", "Phone")],
    ["area", t("Zona", "Area")],
    ["address", t("Dirección", "Address")],
    ["zip", "ZIP"],
    ["notes", t("Notas", "Notes")],
  ]
    .filter(([key]) => String(d.get(key) || "").trim())
    .map(([key, label]) => label + ": " + String(d.get(key)).trim());
  return [
    t(
      "Hola, Oud Bronx. Quiero confirmar este pedido:",
      "Hello Oud Bronx. I'd like to confirm this order:",
    ),
    "",
    ...rows,
    ...(selectedBundle
      ? [t("Pack de 2 aplicado: $55", "2-bottle bundle applied: $55")]
      : []),
    t("Subtotal estimado: ", "Estimated subtotal: ") + money(sum()),
    t("Entrega: ", "Delivery: ") +
      (count() >= 2
        ? t("gratis en zona confirmada", "free in confirmed service area")
        : t("tarifa por confirmar", "fee to be confirmed")),
    ...(scent ? [t("Preferencia: ", "Preference: ") + scent] : []),
    "",
    ...details,
    t(
      "Por favor confirma disponibilidad, precio final, pago y entrega.",
      "Please confirm availability, final price, payment and delivery.",
    ),
  ].join("\n");
}
function renderComplement() {
  const root = $("#complement");
  if (!root) return;
  root.replaceChildren();
  if (count() !== 1) return;
  const current = catalog.find((p) => items[p.id] === 1);
  if (!current) return;
  const preferences = {
    yara: ["khamrah", "asad"],
    khamrah: ["yara", "asad"],
    asad: ["yara", "khamrah"],
  };
  const heading = document.createElement("p");
  heading.className = "complement-heading";
  heading.textContent = t(
    "Completa tu pack de 2 por $55",
    "Complete your 2-bottle bundle for $55",
  );
  root.append(heading);
  const explanation = document.createElement("p");
  explanation.className = "notice";
  explanation.textContent = t(
    "Elige otro aroma y compara el ahorro real. Delivery gratis solo en zonas confirmadas.",
    "Choose another scent and see the actual savings. Free delivery only in confirmed areas.",
  );
  root.append(explanation);
  (
    preferences[current.id] ||
    catalog.filter((p) => p.id !== current.id).map((p) => p.id)
  ).forEach((id, index) => {
    const p = catalog.find((x) => x.id === id);
    if (!p) return;
    const normal = current.price + p.price,
      discount = normal - 55;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "complement-option";
    const img = document.createElement("img");
    img.src = p.image;
    img.alt = "";
    img.loading = "lazy";
    img.width = 58;
    img.height = 58;
    const copy = document.createElement("span");
    const name = document.createElement("strong");
    name.textContent = p.name;
    const detail = document.createElement("small");
    detail.textContent =
      (index === 0 ? t("Sugerido · ", "Suggested · ") : "") +
      t("Añadir por ", "Add for ") +
      money(55 - current.price) +
      (discount > 0 ? t(" · Ahorras ", " · Save ") + money(discount) : "");
    copy.append(name, detail);
    const plus = document.createElement("b");
    plus.textContent = "+";
    button.append(img, copy, plus);
    button.addEventListener("click", () => {
      items[p.id] = 1;
      trackFunnel("complement_select");
      trackFunnel("bundle_upgrade");
      renderCart();
    });
    root.append(button);
  });
}

async function openWhatsApp(msg) {
  if (window.OudContact) {
    await window.OudContact.ready;
    if (window.OudContact.isReady())
      CONFIG.whatsapp =
        window.OudContact.url("").match(/wa\.me\/(\d+)/)?.[1] || "";
  }
  if (!/^\d{10,15}$/.test(CONFIG.whatsapp)) {
    trackFunnel("whatsapp_not_configured");
    openSheet();
    const status = $("#status");
    status.className = "status error";
    status.textContent = t(
      "Falta configurar el número comercial. Copia el mensaje para enviarlo manualmente.",
      "Business number not configured. Copy the message to send manually.",
    );
    if (navigator.clipboard?.writeText) {
      navigator.clipboard
        .writeText(msg)
        .then(() => {
          status.textContent = t(
            "Mensaje copiado. Falta conectar WhatsApp comercial.",
            "Message copied. Business WhatsApp needs connecting.",
          );
        })
        .catch(() => fallback(msg));
    } else fallback(msg);
    return;
  }
  trackFunnel("whatsapp_open_attempt");
  const link = document.createElement("a");
  link.href =
    "https://wa.me/" + CONFIG.whatsapp + "?text=" + encodeURIComponent(msg);
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  document.body.append(link);
  link.click();
  link.remove();
  $("#status").className = "status";
  $("#status").textContent = t(
    "Revisa y envía el mensaje en WhatsApp.",
    "Review and send the message in WhatsApp.",
  );
}
function submit(e) {
  e.preventDefault();
  trackFunnel("order_submit_attempt");
  const form = e.currentTarget;
  if (!form.checkValidity()) {
    $("#deliveryDetails").open = true;
    form.reportValidity();
    return;
  }
  if (count() === 0 && !scent) {
    $("#status").textContent = t(
      "Elige un perfume primero.",
      "Choose a perfume first.",
    );
    return;
  }
  const msg = makeMessage(new FormData(form));
  openWhatsApp(msg);
}
function fallback(msg) {
  $("#status").textContent = t(
    "Copia el pedido de la ventana y envíalo manualmente.",
    "Copy the order from the window and send it manually.",
  );
  window.prompt(t("Copia tu pedido", "Copy your order"), msg);
}
$("#quickChat").addEventListener("click", () => {
  const list = catalog
    .filter((p) => items[p.id] > 0)
    .map((p) => p.name + " × " + items[p.id])
    .join(", ");
  openWhatsApp(
    [
      t(
        "Hola Oud Bronx, tengo una pregunta antes de pedir.",
        "Hi Oud Bronx, I have a question before ordering.",
      ),
      list ? t("Me interesa: ", "Interested in: ") + list : "",
      selectedBundle
        ? t("Vi el pack de 2 por $55.", "I saw the 2-for-$55 bundle.")
        : "",
      scent ? t("Prefiero aromas: ", "I prefer scents: ") + scent : "",
    ]
      .filter(Boolean)
      .join("\n"),
  );
});
$("#cart").addEventListener("click", (e) => {
  const a = e.target.closest("[data-add]"),
    d = e.target.closest("[data-dec]");
  if (a || d) selectedBundle = null;
  if (a) items[a.dataset.add] = Math.min(99, (items[a.dataset.add] || 0) + 1);
  if (d) items[d.dataset.dec] = Math.max(0, (items[d.dataset.dec] || 0) - 1);
  renderCart();
});
$("#closeSheet").onclick = closeSheet;
$("#shade").onclick = closeSheet;
$("#orderForm").addEventListener("submit", submit);
document.addEventListener("keydown", (event) => {
  if (!$("#sheet").classList.contains("open")) return;
  if (event.key === "Escape") closeSheet();
  if (event.key !== "Tab") return;
  const controls = [
    ...$("#sheet").querySelectorAll(
      "button:not(:disabled), summary, input, select, textarea, a[href]",
    ),
  ].filter((el) => el.checkVisibility());
  const edge = event.shiftKey ? controls[0] : controls.at(-1);
  if (document.activeElement === edge) {
    event.preventDefault();
    (event.shiftKey ? controls.at(-1) : controls[0]).focus();
  }
});

(() => {
  const sheet = document.getElementById("sheet"),
    header = document.querySelector("header.top");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  let gesture;
  function release() {
    gesture = null;
    sheet.style.transition = "";
    sheet.style.transform = "";
  }
  sheet.addEventListener("pointerdown", (event) => {
    if (
      !event.isPrimary ||
      event.pointerType !== "touch" ||
      event.target.closest("button, input, textarea, select, summary, a")
    )
      return;
    gesture = {
      id: event.pointerId,
      x: event.clientX,
      y: event.clientY,
      time: performance.now(),
    };
  });
  sheet.addEventListener("pointermove", (event) => {
    if (event.pointerId !== gesture?.id) return;
    const x = event.clientX - gesture.x;
    const y = Math.abs(event.clientY - gesture.y);
    if (y > 12 && y > x) return release();
    if (x < 10 || x < y * 1.5 || reduced.matches) return;
    sheet.setPointerCapture(event.pointerId);
    sheet.style.transition = "none";
    sheet.style.transform = `translateX(${x}px)`;
  });
  sheet.addEventListener("pointerup", (event) => {
    if (event.pointerId !== gesture?.id) return;
    const x = event.clientX - gesture.x;
    const y = Math.abs(event.clientY - gesture.y);
    const velocity = x / Math.max(1, performance.now() - gesture.time);
    release();
    if (x > y * 1.5 && (x > 120 || (x > 55 && velocity > 0.5))) closeSheet();
  });
  sheet.addEventListener("pointercancel", release);
  const update = () => header?.classList.toggle("oud-scrolled", scrollY > 12);
  addEventListener("scroll", update, { passive: true });
  update();
})();
