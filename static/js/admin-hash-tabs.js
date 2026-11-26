/**
 * Fix for Jazzmin/AdminLTE tabs not switching when URL hash changes.
 * This script listens for hash changes and clicks the corresponding tab.
 */
(function ($) {
    'use strict';

    $(document).ready(function () {
        /**
         * Function to activate tab based on URL hash
         */
        function activateTabFromHash() {
            var hash = window.location.hash;
            if (hash) {
                // Find tab link that matches the hash
                var $tabLink = $('.nav-tabs a[href="' + hash + '"]');
                if ($tabLink.length > 0) {
                    $tabLink.tab('show');
                } else {
                    // Fallback for ID matching without the tab suffix if necessary
                    var $tabById = $('.nav-tabs a[href="' + hash + '-tab"]');
                    if ($tabById.length > 0) {
                        $tabById.tab('show');
                    }
                }
            }
        }

        // 1. Check on page load
        activateTabFromHash();

        // 2. Listen for hash changes (e.g. when user clicks a link to another tab on the same page)
        $(window).on('hashchange', function () {
            activateTabFromHash();
        });

        // 3. Update hash When a tab is clicked manually (optional, but good for UX)
        $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
            var hash = $(e.target).attr('href');
            if (hash && hash.startsWith('#')) {
                // Use replaceState to avoid triggering hashchange event recursively
                // or just let it be if we want the back button to work
                history.pushState(null, null, hash);
            }
        });
    });
})(window.jQuery || window.django.jQuery);
