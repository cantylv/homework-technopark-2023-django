document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('sortingForm');
    var checkboxInputs = form.querySelectorAll('input[type=checkbox]');

    checkboxInputs.forEach(function (checkbox) {
        checkbox.addEventListener('change', updateFormAction);
    });

    function updateFormAction() {
        var tags = getSelectedCheckboxValuesTagged();
        var currentUrl = window.location.href;

        // Remove existing tag portion from the URL
        var tagIndex = currentUrl.indexOf('/tag/');
        if (tagIndex !== -1) {
            currentUrl = currentUrl.substring(0, tagIndex);
        } else if (tagIndex === -1 && currentUrl.indexOf('?') !== -1){
            currentUrl = currentUrl.substring(0, currentUrl.indexOf('?'))
        }

        var url = currentUrl;

        if (tags.length > 0) {
            var tagString = tags.join('@');
            if (tagIndex === -1) {
                url += 'tag/';
            } else {
                url += '/tag/';
            }
            url += tagString;
        }

        form.action = url;
    }

    function getSelectedCheckboxValuesTagged() {
        var checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');
        return Array.from(checkboxes).map(function (checkbox) {
            return checkbox.value;
        });
    }
});
