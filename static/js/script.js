function add_menu(menujson) {
    const menu = document.querySelector('.menu');
    menujson.map(function(restaurant) {
        var section = document.createElement('section');
        var content = `<h2><a href="${ restaurant['url'] }">${ restaurant['name'] }</a></h2><p>${ restaurant['menu'] }</p><br>`;
        section.innerHTML = content;
        menu.appendChild(section);
    })
}

function get_menu() {
    fetch(new Request('/menu'))
      .then(function(response) {
        return response.json()
      }).then(function(json) {
        add_menu(json)
      }).then(function() {
        document.querySelector('.loading').remove()
      }).catch(function(ex) {
        console.log('parsing failed', ex)
      });
}

get_menu()