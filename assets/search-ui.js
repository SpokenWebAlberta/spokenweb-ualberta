// Methods and jQuery UI for Wax search box


function setObject(type) {
  if (type === "object") {
    return "Audio";
  } else if (type === "default") {
    return "Page";
  } else {
    return type;
  }
}


function displayResult(item, fields, url) {
  let type = setObject(item.layout)

  return `
    <div class="search-result">
      <a href="${url}${item.permalink}">
        <div class="search-inner-results">
          <p class="search-title">${item.title}</p>
          <p class="search-type">${type}</p>
          <p class="search-description">${item.description}</p>
        </div>
      </a>
    </div>`;
}

function startSearchUI(fields, indexFile, url) {
  $.getJSON(indexFile, function(store) {
    var index  = new elasticlunr.Index;

    index.saveDocument(false);
    index.setRef('lunr_id');

    for (i in fields) { index.addField(fields[i]); }
    for (i in store)  { index.addDoc(store[i]); }

    $('input#search').on('input', function() {
      var results_div = $('#results');
      var query       = $(this).val();
      var results     = index.search(query, { boolean: 'AND', expand: true });

      results_div.empty();
      results_div.append(`<p class="results-info">Displaying ${results.length} results</p>`);

      for (var r in results) {
        var ref    = results[r].ref;
        var item   = store[ref];
        var result = displayResult(item, fields, url);

        results_div.append(result);
      }
    });

    const urlParams = new URLSearchParams(window.location.search);
    const myParam = urlParams.get('search');

    if (myParam !== null) {
      let el = document.getElementById('search');
      el.value = myParam;
      el.dispatchEvent(new Event('input', {'bubbles': true}));
    }
  }).fail(function() { console.log("failed to get json")});
}
