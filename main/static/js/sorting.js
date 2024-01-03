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
        var tagIndex = currentUrl.indexOf('tag/');
        if (tagIndex !== -1) {
            currentUrl = currentUrl.substring(0, tagIndex);
        } else if (tagIndex === -1 && currentUrl.indexOf('?') !== -1) {
            currentUrl = currentUrl.substring(0, currentUrl.indexOf('?'))
        }

        var url = currentUrl;

        if (tags.length > 0) {
            var tagString = tags.join('@');
            url += 'tag/';
            url += tagString;
            url += '/';
        }

        form.action = url;

        // Меняем параметр page при выборе нового тега
        var pageInput = document.getElementById('pageInput');
        pageInput.value = 1;
    }

    function getSelectedCheckboxValuesTagged() {
        var checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');
        return Array.from(checkboxes).map(function (checkbox) {
            return checkbox.value;
        });
    }
});
