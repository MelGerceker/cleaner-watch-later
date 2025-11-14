export function initDurationSlider(onChange) {
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