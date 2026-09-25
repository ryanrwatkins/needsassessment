// Filter the pre-rendered CSV catalog; full content remains readable without JS.
(() => {
  const catalog = document.querySelector('#resource-catalog');
  if (!catalog) return;
  const rows = [...catalog.querySelectorAll('.resource-row')];
  const search = catalog.querySelector('#catalog-search');
  const sort = catalog.querySelector('#catalog-sort');
  const fields = ['resource_type', 'language', 'year'];
  const selects = fields.map(field => catalog.querySelector(`#filter-${field}`));
  const buttons = [...catalog.querySelectorAll('[data-topic]')];
  const records = rows.map(row => ({
    row,
    title: row.dataset.title,
    date: row.dataset.date,
    topics: JSON.parse(row.dataset.topics),
    resource_type: JSON.parse(row.dataset.resourceType),
    language: JSON.parse(row.dataset.language),
    year: JSON.parse(row.dataset.year),
    text: '',
  }));
  records.forEach(record => {
    record.text = [record.row.textContent, ...record.topics].join(' ').toLocaleLowerCase();
  });
  let topic = '';
  function update() {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    const sorted = [...records].sort((a, b) => {
      if (sort.value !== 'title') {
        if (!a.date && b.date) return 1;
        if (a.date && !b.date) return -1;
        const compared = a.date.localeCompare(b.date);
        if (compared) return sort.value === 'newest' ? -compared : compared;
      }
      return a.title.localeCompare(b.title);
    });
    for (const record of sorted) {
      const matches = (!topic || record.topics.includes(topic)) &&
        terms.every(term => record.text.includes(term)) &&
        fields.every((field, i) => !selects[i].value || record[field].includes(selects[i].value));
      record.row.hidden = !matches;
      if (matches) count += 1;
      catalog.querySelector('tbody').append(record.row);
    }
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.topic === topic)));
    catalog.querySelector('#catalog-count').textContent = `${count} of ${rows.length} resources`;
    catalog.querySelector('#catalog-empty').hidden = count !== 0;
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    topic = button.dataset.topic;
    update();
  }));
  search.addEventListener('input', update);
  [...selects, sort].forEach(select => select.addEventListener('change', update));
  catalog.querySelector('#catalog-reset').addEventListener('click', () => {
    topic = '';
    search.value = '';
    selects.forEach(select => { select.value = ''; });
    sort.value = 'title';
    update();
  });
  const legacyTopics = {
    '#section-books': 'Books',
    '#section-articles': 'Articles and Chapters',
  };
  function applyHash() {
    topic = legacyTopics[location.hash] || '';
    update();
  }
  window.addEventListener('hashchange', applyHash);
  catalog.querySelector('#catalog-controls').hidden = false;
  applyHash();
})();
