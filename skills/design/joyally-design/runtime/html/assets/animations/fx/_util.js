/* pakco.html fx :: shared helpers */
(function(){
  window.HPX = window.HPX || {};
  const U = window.HPX._u = {};

  U.css = (el, name, fb) => {
    const v = getComputedStyle(el).getPropertyValue(name).trim();
    return v || fb;
  };

  U.accent = (el, fb) => U.css(el, '--accent', fb || '#275a34');
  U.accent2 = (el, fb) => U.css(el, '--accent-2', fb || '#397a46');
  U.text = (el, fb) => U.css(el, '--text-1', fb || '#253c2d');
  U.alpha = (el, token, opacity) => {
    const hex = U.css(el, token, '#f7f5f0').replace('#', '');
    if (!/^[0-9a-f]{6}$/i.test(hex)) return `rgba(247,245,240,${opacity})`;
    const values = [0, 2, 4].map((index) => parseInt(hex.slice(index, index + 2), 16));
    return `rgba(${values.join(',')},${opacity})`;
  };

  U.palette = (el) => [
    U.accent(el),
    U.accent2(el),
    U.css(el, '--good', '#356439'),
    U.css(el, '--warn', '#96620f'),
    U.css(el, '--bad', '#a7472d'),
  ];

  U.canvas = (el) => {
    if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
    const c = document.createElement('canvas');
    c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;pointer-events:none;display:block;';
    el.appendChild(c);
    const ctx = c.getContext('2d');
    let w = 0, h = 0, dpr = Math.max(1, Math.min(2, window.devicePixelRatio||1));
    const fit = () => {
      const r = el.getBoundingClientRect();
      w = Math.max(1, r.width|0);
      h = Math.max(1, r.height|0);
      c.width = (w*dpr)|0;
      c.height = (h*dpr)|0;
      ctx.setTransform(dpr,0,0,dpr,0,0);
    };
    fit();
    const ro = new ResizeObserver(fit);
    ro.observe(el);
    return {
      c, ctx,
      get w(){return w;}, get h(){return h;}, get dpr(){return dpr;},
      destroy(){
        try{ro.disconnect();}catch(e){}
        if (c.parentNode) c.parentNode.removeChild(c);
      }
    };
  };

  U.loop = (fn) => {
    let raf = 0, stopped = false, t0 = performance.now();
    const tick = (t) => {
      if (stopped) return;
      fn((t - t0)/1000);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => { stopped = true; cancelAnimationFrame(raf); };
  };

  U.rand = (a,b) => a + Math.random()*(b-a);
})();
