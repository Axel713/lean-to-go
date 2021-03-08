$(document).ready(function(){
    $('.sidenav').sidenav({edge: 'right'});
    $('.dropdown-trigger').dropdown();
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 2,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
});