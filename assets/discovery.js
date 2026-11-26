(function () {
  const stage = document.getElementById("discoveryStage");
  if (!stage) return;
  const sets = {
    hot: ["khamrah", "yara", "asad"],
    gems: ["asad", "khamrah", "yara"],
  };
  const cards = document.getElementById("discoveryCards"),
    ambient = document.getElementById("discoveryAmbient"),
    caption = document.getElementById("discoveryCaption"),
    counter = document.getElementById("discoveryCount"),
    buy = document.getElementById("discoveryBuy"),
    reveal = document.getElementById("discoveryReveal"),
    revealText = document.getElementById("discoveryRevealText"),
    order = document.getElementById("discoveryOrder");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  // Only verified, product-matched, licensed MP4 URLs belong here. Empty entries safely use the photo.
  const productVideos = { khamrah: "", yara: "", asad: "" };
  let mode = "hot",
    index = 0,
    timer = 0,
    visible = false,
    dragX = null,
    expanded = false,
    occasion = "",
    activeVideo = null;
  function stopVideo() {
    if (activeVideo) {
      activeVideo.pause();
      activeVideo.removeAttribute("src");
      activeVideo.load();
      activeVideo = null;
    }
    cards
      .querySelectorAll(".discovery-card.is-playing")
      .forEach((n) => n.classList.remove("is-playing"));
  }
  function startProductVideo() {
    if (!visible || document.hidden || reduced.matches || expanded) return;
    const item = sets[mode][index],
      url = productVideos[item];
    if (!url) {
      step(1);
      return;
    }
    const card = cards.children[index],
      video = card?.querySelector("video");
    if (!video) {
      step(1);
      return;
    }
    stopVideo();
    activeVideo = video;
    video.src = url;
    video.onended = () => {
      stopVideo();
      step(1);
    };
    video.onerror = () => {
      stopVideo();
      step(1);
    };
    video
      .play()
      .then(() => card.classList.add("is-playing"))
      .catch(() => {
        stopVideo();
        step(1);
      });
  }

  function trackDiscovery(action) {
    try {
      window.dataLayer?.push({
        event: "oud_discovery",
        action,
        collection: mode,
        perfume: sets[mode][index],
      });
    } catch (e) {}
  }
  function build() {
    document.getElementById("discoveryIntro").textContent =
      mode === "hot"
        ? t(
            "Explora los perfumes de la colección.",
            "Explore the fragrances in the collection.",
          )
        : t(
            "Compara los perfiles de cada perfume.",
            "Compare the profiles of each fragrance.",
          );
    cards.replaceChildren(
      ...sets[mode].map((v) => {
        const p = catalog.find((x) => x.id === v);
        const article = document.createElement("article");
        article.className = "discovery-card";
        article.innerHTML =
          '<div class="discovery-image"><img loading="lazy" decoding="async" alt=""><video class="discovery-product-video" muted playsinline preload="none" aria-hidden="true"></video><div class="discovery-image-shine"></div></div><div class="details"><span class="discovery-card-kicker">OUD BRONX / THE EDIT</span><h3></h3><p></p><span class="discovery-price"></span></div>';
        article.querySelector("img").alt = p.name;
        article.querySelector("img").src = p.image;
        article.querySelector("h3").textContent = p.name;
        article.querySelector(".details p").textContent = p[lang];
        article.querySelector(".discovery-price").textContent = "$" + p.price;
        return article;
      }),
    );
    render();
  }
  function render() {
    const arr = sets[mode],
      nodes = [...cards.children];
    nodes.forEach((node, i) => {
      const delta = (i - index + arr.length) % arr.length;
      const pos = delta === 0 ? 0 : delta === 1 ? 1 : -1;
      node.dataset.pos = String(pos);
      node.setAttribute("aria-hidden", String(pos !== 0));
      node.inert = pos !== 0;
      node.style.setProperty("--depth", String(pos));
    });
    const current = catalog.find((p) => p.id === arr[index]);
    caption.textContent = current[lang];
    counter.textContent =
      String(index + 1).padStart(2, "0") +
      " / " +
      String(arr.length).padStart(2, "0");
    reveal.hidden = !expanded;
    document
      .getElementById("discoveryDetails")
      .setAttribute("aria-expanded", String(expanded));
    revealText.replaceChildren();
    const details = document.createElement("a");
    details.href = lang + "/products/" + current.id + "/";
    details.textContent = t("Explorar ", "Explore ") + current.name + " →";
    details.style.color = "inherit";
    revealText.append(details);
    const p = catalog.find((x) => x.id === arr[index]);
    const pair = choosePair(p.id, occasion),
      partner = catalog.find((x) => x.id === pair);
    document.getElementById("discoveryPairImage").src = partner.image;
    document.getElementById("discoveryPairImage").alt = partner.name;
    document.getElementById("discoveryPairName").textContent =
      p.name.replace("Lattafa ", "") +
      " + " +
      partner.name.replace("Lattafa ", "");
    document.getElementById("discoveryMatch").textContent = occasion
      ? matchCopy(p.id, occasion)
      : t(
          "Elige una ocasión para afinar tu recomendación.",
          "Choose an occasion for a recommendation.",
        );
    document
      .querySelectorAll("#discoveryOccasions button")
      .forEach((b) =>
        b.setAttribute("aria-pressed", String(b.dataset.occasion === occasion)),
      );
    buy.textContent =
      lang === "en"
        ? "Choose " + p.name + " · $" + p.price
        : "Elegir " + p.name + " · $" + p.price;
    order.textContent =
      lang === "en"
        ? "Prepare " + p.name + " order ↗"
        : "Preparar pedido de " + p.name + " ↗";
  }
  function choosePair(id, use) {
    const preferences = {
      daily: ["yara", "asad", "khamrah"],
      date: ["yara", "khamrah", "asad"],
      night: ["khamrah", "asad", "yara"],
    };
    return (preferences[use] || ["yara", "khamrah", "asad"]).find(
      (x) => x !== id,
    );
  }
  function matchCopy(id, use) {
    const partner = catalog.find((p) => p.id === choosePair(id, use));
    return (
      t("Para esta ocasión: ", "For this occasion: ") +
      partner.name +
      " · " +
      partner[lang]
    );
  }
  function addPack() {
    const id = sets[mode][index],
      other = choosePair(id, occasion);
    const pair = bundles.find((x) => x.includes(id) && x.includes(other));
    if (!pair) return;
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
    items[id] = 1;
    items[other] = 1;
    selectedBundle = pair;
    renderCart();
    trackDiscovery("bundle_selected");
    openSheet();
  }
  document.getElementById("discoveryPack").addEventListener("click", addPack);
  document
    .getElementById("discoveryOccasions")
    .addEventListener("click", (e) => {
      const b = e.target.closest("button[data-occasion]");
      if (!b) return;
      occasion = b.dataset.occasion;
      trackDiscovery("occasion_selected");
      render();
    });
  function addCurrent() {
    const p = sets[mode][index];
    addBottle(p);
    selectedBundle = null;
    renderCart();
    trackDiscovery("add_to_order");
    openSheet();
  }
  function schedule() {
    clearTimeout(timer);
    if (
      visible &&
      !expanded &&
      !reduced.matches &&
      !document.hidden &&
      !stage.matches(":hover") &&
      !stage.contains(document.activeElement)
    )
      timer = setTimeout(startProductVideo, 23000);
  }
  function step(n) {
    stopVideo();
    index = (index + n + sets[mode].length) % sets[mode].length;
    expanded = false;
    occasion = "";
    trackDiscovery("swipe");
    render();
    schedule();
  }
  function setMode(m) {
    if (mode === m) return;
    stopVideo();
    mode = m;
    index = 0;
    expanded = false;
    occasion = "";
    trackDiscovery("switch_collection");
    document
      .getElementById("tabHot")
      .setAttribute("aria-selected", String(m === "hot"));
    document
      .getElementById("tabGems")
      .setAttribute("aria-selected", String(m === "gems"));
    document.getElementById("discoveryTitle").textContent =
      m === "hot" ? "HOT RIGHT NOW" : "HIDDEN GEMS";
    build();
    schedule();
  }
  document
    .getElementById("tabHot")
    .addEventListener("click", () => setMode("hot"));
  document
    .getElementById("tabGems")
    .addEventListener("click", () => setMode("gems"));
  document
    .getElementById("discoveryPrev")
    .addEventListener("click", () => step(-1));
  document
    .getElementById("discoveryNext")
    .addEventListener("click", () => step(1));
  document.getElementById("discoveryDetails").addEventListener("click", () => {
    expanded = !expanded;
    stopVideo();
    render();
    schedule();
  });
  buy.addEventListener("click", addCurrent);
  order.addEventListener("click", addCurrent);
  stage.addEventListener(
    "pointerdown",
    (e) => {
      if (e.pointerType === "mouse") return;
      dragX = e.clientX;
    },
    { passive: true },
  );
  stage.addEventListener(
    "pointerup",
    (e) => {
      if (dragX === null) return;
      const delta = e.clientX - dragX;
      dragX = null;
      if (Math.abs(delta) > 42) step(delta < 0 ? 1 : -1);
    },
    { passive: true },
  );
  stage.addEventListener("pointercancel", () => {
    dragX = null;
  });
  stage.addEventListener("mouseenter", () => clearTimeout(timer));
  stage.addEventListener("mouseleave", schedule);
  stage.addEventListener("focusin", () => clearTimeout(timer));
  stage.addEventListener("focusout", () => requestAnimationFrame(schedule));
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      ambient.pause();
      stopVideo();
    } else if (visible && !navigator.connection?.saveData && !reduced.matches)
      ambient.play().catch(() => {});
    schedule();
  });
  reduced.addEventListener?.("change", () => {
    if (reduced.matches) stopVideo();
    schedule();
  });
  new IntersectionObserver(
    (entries) => {
      visible = entries[0].isIntersecting;
      if (!visible) stopVideo();
      if (visible && !navigator.connection?.saveData && !reduced.matches) {
        if (!ambient.src) {
          ambient.src = ambient.dataset.src;
          ambient.load();
        }
        ambient.play().catch(() => {});
      } else ambient.pause();
      schedule();
    },
    { threshold: 0.2 },
  ).observe(stage);
  document.addEventListener("oud-language", build);
  build();
})();
