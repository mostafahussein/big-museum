var task_status_poller = function(url) {
    var jitems = jQuery('#items'),
        jfulness = jQuery('#fulness');

    var interval_id = setInterval(function() {
        jQuery.ajax({url: url, method: 'GET'}).done(function(data) {
            if (data.status) {
                jitems.find('span').text(data.current);

                if (data.fulness !== undefined) {
                    jfulness.removeClass('hidden').find('span').text(data.fulness);
                    jQuery('#success_msg').removeClass('hidden');
                    clearInterval(interval_id);
                }
            } else {
                jQuery('#error_msg').removeClass('hidden').text(data.message);
                jitems.addClass('hidden');
                jfulness.addClass('hidden');

                clearInterval(interval_id);
            }
        });
    }, 1000);
};