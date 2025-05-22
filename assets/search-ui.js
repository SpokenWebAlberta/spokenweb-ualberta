// Methods and jQuery UI for Wax search box


function setObject(type) {
    console.log(type);
    if (type === "object") {
        return "Audio";
    } else if (type === "default") {
        return "Page";
    } else {
        return type;
    }
}


function setDescription(desc) {
  if (desc !== null) {
    return `<p class=\"search-description\">${desc}</p>`;
  } else {
    return "";
  }
}


function displayResult(item, fields, url) {
    console.log(item);

    let type = setObject(item.layout)

  let inner_html = `
    <div class="search-result">
      <a href="${url}${item.permalink}">
        <div class="search-inner-results">
          <p class="search-title">${item.title}</p>
          <p class="search-type">${type}</p>
          ${setDescription(item.description)}
        </div>
      </a>
    </div>`;

  let wrapper = document.createElement('div');
  wrapper.innerHTML = inner_html;

  return wrapper.firstElementChild;
}

function startSearchUI(indexfile, fields, url) {
    fetch(url + indexfile)
        .then((response) => {
            return response.json();
        })
        .then(store => {

            var index = elasticlunr(function () {
                for (let field in fields) {
                    this.addField(fields[field]);
                }
                this.addField("body");
                this.setRef('lunr_id');
            });

            for (let row in store) {
                index.addDoc(store[row]);
            }

            document.querySelector('input#search').addEventListener('input', function() {

                let results_div = document.querySelector('#results');
                let query       = this.value;
                let results     = index.search(query, { boolean: 'AND', expand: true });

                console.log(query);
                console.log(results);


                while (results_div.firstChild) {
                  results_div.removeChild(results_div.firstChild)
                }

                let new_child = document.createElement("p")
                new_child.classList.add("results-info")
                new_child.textContent = `Displaying ${results.length} results`

                results_div.appendChild(new_child);

                for (let r in results) {
                    let ref    = results[r].ref;
                    let item   = store[ref];
                    let result = displayResult(item, fields, url);

                    console.log(result);

                    results_div.appendChild(result);
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
         // .fail(function() { console.log("failed to get json")});
}
