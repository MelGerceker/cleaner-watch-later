(function () {
  function createVideoTableController({ rowsEl, countEl, btnAll, btnUnwatched, btnWatched }) {
    let all        = [];
    let watchedSet = new Set();
    let mode       = 'all';
    let durationSlider = null;

    function setData(videos, watchedIds) {
      all        = videos || [];
      watchedSet = new Set(watchedIds || []);
    }

    function setDurationSlider(slider) {
      durationSlider = slider;
    }

    function render() {
      let data = all;
      if (mode === 'unwatched') data = all.filter(v => !watchedSet.has(v.id));
      if (mode === 'watched')   data = all.filter(v => watchedSet.has(v.id));

      if (durationSlider) {
        const { min, max } = durationSlider.getFilters();
        if (min !== null || max !== null) {
          data = data.filter(v => {
            const m = v.approxdur;
            if (typeof m !== 'number' || !Number.isFinite(m)) return false;
            if (min !== null && m < min) return false;
            if (max !== null && m > max) return false;
            return true;
          });
        }
      }

      rowsEl.innerHTML = data.map(v => `
        <tr>
          <td class="thumb"><img loading="lazy" src="${v.thumb}" alt=""></td>
          <td>${escapeHtml(v.title)}</td>
          <td>${escapeHtml(v.duration || "")}</td>
          <td>${escapeHtml(v.channel)}</td>
          <td><a href="${v.url}" target="_blank" rel="noopener">Open</a></td>
        </tr>
      `).join('');

      const totals = `(${data.length} shown • ${all.length} total)`;
      if (mode === 'unwatched') {
        countEl.textContent = `Unwatched ${totals}`;
      } else if (mode === 'watched') {
        countEl.textContent = `Watched ${totals}`;
      } else {
        countEl.textContent = `All ${totals}`;
      }

      [btnAll, btnUnwatched, btnWatched].forEach(b => b.classList.remove('active'));
      (mode === 'all' ? btnAll : mode === 'unwatched' ? btnUnwatched : btnWatched)
        .classList.add('active');
    }

    btnAll.addEventListener('click',       () => { mode = 'all';       render(); });
    btnUnwatched.addEventListener('click', () => { mode = 'unwatched'; render(); });
    btnWatched.addEventListener('click',   () => { mode = 'watched';   render(); });

    return {
      setData,
      setDurationSlider,
      render,
    };
  }

  window.createVideoTableController = createVideoTableController;
})();


(function () {
function initDurationSlider(onChange) {
    const rangeMinEl = document.getElementById('rangeMin');
    const rangeMaxEl = document.getElementById('rangeMax');
    const labelMinEl = document.getElementById('labelMin');
    const labelMaxEl = document.getElementById('labelMax');
    const btnDurReset = document.getElementById('btnDurReset');

    let bounds = { min: 0, max: 0 }; // minutes
    let filters = { min: null, max: null };

    function configureFromData(all) {
        const durations = all
            .map(v => v.approxdur)
            .filter(m => typeof m === 'number' && Number.isFinite(m));

        bounds.min = Math.min(...durations);
        bounds.max = Math.max(...durations);

        rangeMinEl.min = bounds.min;
        rangeMinEl.max = bounds.max;
        rangeMaxEl.min = bounds.min;
        rangeMaxEl.max = bounds.max;

        // initially no filter
        rangeMinEl.value = bounds.min;
        rangeMaxEl.value = bounds.max;

        filters = { min: null, max: null };
        labelMinEl.textContent = 'any';
        labelMaxEl.textContent = 'any';
    }

    function syncAndClamp(changedEl) {
        let minVal = Number(rangeMinEl.value);
        let maxVal = Number(rangeMaxEl.value);

        // keep sliders from crossing
        if (minVal > maxVal) {
            if (changedEl === rangeMinEl) {
                maxVal = minVal;
                rangeMaxEl.value = String(maxVal);
            } else {
                minVal = maxVal;
                rangeMinEl.value = String(minVal);
            }
        }

        // extreme = no filter
        filters.min = (minVal <= bounds.min) ? null : minVal;
        filters.max = (maxVal >= bounds.max) ? null : maxVal;

        labelMinEl.textContent = filters.min === null ? 'any' : String(minVal);
        labelMaxEl.textContent = filters.max === null ? 'any' : String(maxVal);

        if (typeof onChange === 'function') onChange();
    }

    rangeMinEl.addEventListener('input', () => syncAndClamp(rangeMinEl));
    rangeMaxEl.addEventListener('input', () => syncAndClamp(rangeMaxEl));

    btnDurReset.addEventListener('click', () => {
        if (!Number.isFinite(bounds.min) || !Number.isFinite(bounds.max)) return;

        rangeMinEl.value = bounds.min;
        rangeMaxEl.value = bounds.max;

        filters = { min: null, max: null };
        labelMinEl.textContent = 'any';
        labelMaxEl.textContent = 'any';

        if (typeof onChange === 'function') onChange();
    });

    function getFilters() {
        return { ...filters };
    }

    return {
      configureFromData,
      getFilters,
    };
  }

  // expose as global for normal <script> usage
  window.initDurationSlider = initDurationSlider;
})();


function escapeHtml(s) {
  return (s || "").replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;',
    '"': '&quot;', "'": '&#39;'
  }[c]));
}

window.escapeHtml = escapeHtml;
