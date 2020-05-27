$(document).ready(function () {

    let filter = {
        stars: [],
        writtenByMe: false,
        result: []
    };

    $('.checkbox').prop('checked', false);
    $('#iWasPassengerCheckbox').prop('checked', true);
    $('#iWasDriverCheckbox').prop('checked', false);

    $('.sort-review').click(function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            cache: false,
            data: {order: $(this).text(), user: $('#hidden-user-id').text(), select: filter.result.join('|')},
            url: "/en/sort",
            dataType: "json",
            success: function (data) {
                filter.result = [];
                while (document.getElementById('reviews').hasChildNodes()) {
                    document.getElementById('reviews').removeChild(document.getElementById('reviews').childNodes[0])
                }
                for (var i = 0; i < data.length; i++) {
                    add(data[i], document.getElementById('review-search').value);
                    filter.result.push(data[i]['id'])
                }
            }
        })
    });

    $('#review-search').keyup(function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            cache: false,
            data: {
                search: document.getElementById('review-search').value,
                user: $('#hidden-user-id').text(),
                select: filter.result.join('|')
            },
            url: "/en/search",
            dataType: "json",
            success: function (data) {
                filter.result = [];
                while (document.getElementById('reviews').hasChildNodes()) {
                    document.getElementById('reviews').removeChild(document.getElementById('reviews').childNodes[0])
                }
                for (var i = 0; i < data.length; i++) {
                    add(data[i], document.getElementById('review-search').value);
                    filter.result.push(data[i]['id'])
                }
            }
        });
    });

    $('.checkbox').click(function (event) {

        if ($(this).is(':checked')) {
            if ($(this).attr('value') === "me") {
                filter.writtenByMe = true;
            } else {
                filter.stars.push($(this).attr('value'));
            }
        } else {
            if ($(this).attr('value') === "me") {
                filter.writtenByMe = false;
            } else {
                var index = filter.stars.indexOf($(this).attr('value'));
                filter.stars.splice(index, 1);
            }
        }

        filterResults(false)
    });

    function filterResults(publish) {
        $.ajax({
            type: "POST",
            cache: false,
            data: {stars: filter.stars.join(''), user: $('#hidden-user-id').text(), writtenByMe: filter.writtenByMe},
            url: "/en/filterstars",
            dataType: "json",
            success: function (data) {
                filter.result = [];
                while (document.getElementById('reviews').hasChildNodes()) {
                    document.getElementById('reviews').removeChild(document.getElementById('reviews').childNodes[0])
                }
                for (var i = 0; i < data.length; i++) {
                    add(data[i]);
                    filter.result.push(data[i]['id'])
                }
                document.getElementById('num-results').removeChild(document.getElementById('num-results').childNodes[0]);
                var txt;
                if (data.length === 1) {
                    txt = document.createTextNode('(' + data.length + ' result)');
                } else {
                    txt = document.createTextNode('(' + data.length + ' results)');
                }
                document.getElementById('num-results').appendChild(txt);
            }
        })
    }

    function add(review, search = '') {
        let outerDiv = document.createElement('DIV');
        outerDiv.setAttribute('class', 'content-section border-light p-4 mx5 mb-5 display-review');
        let starRow = document.createElement('DIV');
        starRow.setAttribute('class', 'row');
        let displayRate = document.createElement('DIV');
        displayRate.setAttribute('class', 'display_rate col-ms-auto margin-b');
        for (var i = 5; i > 0; i--) {
            var star;
            star = document.createElement('I');
            star.setAttribute('aria-hidden', 'true');
            if (review['amount_of_stars'] <= 5 - i) {
                star.setAttribute('class', 'fa fa-star not-checked');
            } else {
                star.setAttribute('class', 'fa fa-star checked');
            }
            displayRate.appendChild(star)
        }
        starRow.appendChild(displayRate);
        outerDiv.appendChild(starRow);

        let titleRow = document.createElement('DIV');
        titleRow.setAttribute('class', 'row');
        titleRow.setAttribute('style', 'margin-left: 0');
        let displayTitle = document.createElement('DIV');
        displayTitle.setAttribute('class', 'col display-title');
        let boldTitle = document.createElement('B');
        createTextNodeOnSearch(search, review['title'], boldTitle);
        displayTitle.appendChild(boldTitle);
        titleRow.appendChild(displayTitle);
        outerDiv.appendChild(titleRow);

        let creationRow = document.createElement('DIV');
        creationRow.setAttribute('class', 'row');
        let displayNameCol = document.createElement('DIV');
        displayNameCol.setAttribute('class', 'col display-name');
        let boldCreation = document.createElement('B');
        createTextNodeOnSearch(search, review['creation'], boldCreation);
        let byText = document.createTextNode(' by ');
        let boldName = document.createElement('B');
        createTextNodeOnSearch(search, review['user_from_first_name'] + ' ' + review['user_from_last_name'], boldName);
        displayNameCol.appendChild(boldCreation);
        displayNameCol.appendChild(byText);
        displayNameCol.appendChild(boldName);
        creationRow.appendChild(displayNameCol);
        outerDiv.appendChild(creationRow);

        let pictureRow = document.createElement('DIV');
        pictureRow.setAttribute('class', 'content-section border-light p-4 mx-5 mb-5 display-review');
        let img = document.createElement('IMG');
        img.setAttribute('class', 'display-profile-pic-review');
        img.setAttribute('src', '/static/images/temp_profile_pic.png');
        img.setAttribute('alt', 'HTML5 Icon');
        pictureRow.appendChild(img);
        outerDiv.appendChild(pictureRow);

        let textRow = document.createElement('DIV');
        textRow.setAttribute('class', 'row display-review');
        let paraText = document.createElement('P');
        createTextNodeOnSearch(search, review['review_text'], paraText);
        textRow.appendChild(paraText);
        outerDiv.appendChild(textRow);

        document.getElementById('reviews').appendChild(outerDiv);
    }

    function createTextNodeOnSearch(search, text, parent) {
        if (search === '') {
            let textNode = document.createTextNode(text);
            parent.append(textNode);
            return
        }
        search = search.toLowerCase();
        let indexPrev = 0;
        let index = text.toLowerCase().indexOf(search, indexPrev);
        let c = 0;
        while (index !== -1 && c < 25) {
            if (indexPrev < index) {
                let textN = document.createTextNode(text.substr(indexPrev, index - indexPrev));
                parent.append(textN);
            }
            let highlight = document.createElement('B');
            highlight.setAttribute('style', 'color: #009900');
            let highlightText = document.createTextNode(text.substr(index, search.length));
            highlight.appendChild(highlightText);
            parent.append(highlight);
            indexPrev = index + search.length;
            index = text.toLowerCase().indexOf(search, index + 1);
            c += 1
        }
        if (indexPrev < text.length) {
            let textN = document.createTextNode(text.substr(indexPrev, text.length - indexPrev + 1));
            parent.append(textN);
        }
    }

    $('#iWasDriverCheckbox').click(function (e) {
        $(this).prop('checked', true);
        $('#iWasPassengerCheckbox').prop('checked', false);
        $('#role').attr('value', 0)
    });

    $('#iWasPassengerCheckbox').click(function (e) {
        $(this).prop('checked', true);
        $('#iWasDriverCheckbox').prop('checked', false);
        $('#role').attr('value', 1)
    })
});