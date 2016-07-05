/**
 * Created by Alice on 01.07.2016.
 */
var arr = $('input:checkbox.file-selection-id').filter(':checked').map(function () {
    return this.id;
}).get();/**get id`s of checked boxes */