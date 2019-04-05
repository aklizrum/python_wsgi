document.addEventListener("DOMContentLoaded", function (event) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_regions');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            var region_select = document.getElementById('region');
            var city_select = document.getElementById('city');
            region_select.innerHTML = "<option value=''>Выберете регион</option>";
            city_select.innerHTML = "<option value=''>Выберете город</option>";
            data.forEach(function (row) {
                region_select.innerHTML += "<option value='" + row['id'] + "'>" + row['name'] + "</option>";
            });
        } else {
            alert('Request failed.  Returned status of ' + xhr.status);
        }
    };
    xhr.send();
});

function getCities() {
    var region_select = document.getElementById('region');
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get_cities');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            var city_select = document.getElementById('city');
            data.forEach(function (row) {
                city_select.innerHTML += "<option value='" + row['id'] + "'>" + row['name'] + "</option>";
            });
        } else {
            alert('Request failed.  Returned status of ' + xhr.status);
        }
    };
    xhr.send(encodeURI('region_id=' + region_select.value));
}