// Methods and jQuery UI for Wax search box
function excerptedString(str) {
  str = str || ''; // handle null > string
  if (str.length < 40) {
    return str;
  }
  else {
    return `${str.substring(0, 40)} ...`;
  }
}

function getThumbnail(item, url) {
  if ('thumbnail' in item) {
    return `<img class='sq-thumb-sm' src='${item.thumbnail}'/>`
  }
  else {
    return '';
  }
}

function displayResult(item, fields, url) {
  var pid   = item.iden;
  var label = item.title || 'Untitled';
  var link  = item.permalink;
  var thumb = getThumbnail(item, url);
  var meta  = []

  for (i in fields) {
    fieldLabel = fields[i];
    if (fieldLabel in item ) {
      meta.push(`<b>${fieldLabel}:</b> ${excerptedString(item[fieldLabel])}`);
    }
  }
  return `<div class="result"><a href="${url}${link}">${thumb} <p><span class="title">${item.title}</span></p></a></div>`;
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
  });
}
