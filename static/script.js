function search(query) {
    // Utiliza la clave de API y el ID de búsqueda personalizado para enviar una solicitud a la API de Google
    var apiKey = 'TU_CLAVE_DE_API';
    var customSearchId = 'TU_ID_DE_BUSQUEDA_PERSONALIZADA';
    var url = 'https://www.googleapis.com/customsearch/v1?q=' + query + '&key=' + apiKey + '&cx=' + customSearchId;

    // Realiza una solicitud GET a la API
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Procesa y muestra los resultados en tu página
            var response = JSON.parse(xhr.responseText);
            console.log(response); // Aquí puedes manipular los resultados como desees
        } else {
            console.error('Error al cargar los resultados de la búsqueda');
        }
    };
    xhr.send();
}
