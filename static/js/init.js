(function($){
  $(function(){


    // Plugin initialization
    $('.collapsible').collapsible({accordion: true});
    $('.carousel.carousel-slider').carousel({fullWidth: true});
    $('.carousel').carousel();
    $('.dropdown-trigger').dropdown({
      alignment: 'right',
      constrainWidth: false,
      coverTrigger: false,
      closeOnClick: false,
      onOpenEnd: function(el) {
        console.log(el.M_Dropdown);
        var tabs = $(this).find('.tabs');
        var dropdownInstance = el.M_Dropdown;
        if (tabs.length) {
          var tabsInstance = M.Tabs.getInstance(tabs);
          tabsInstance.updateTabIndicator();
          tabsInstance.options.onShow = function() {
            setTimeout(function() {
              dropdownInstance.recalculateDimensions();
              tabsInstance.updateTabIndicator();
            }, 0);
          };
        }
      }
    });
    $('.slider').slider();
    $('.parallax').parallax();
    $('.modal').modal();
    $('.scrollspy').scrollSpy();
    $('.sidenav').sidenav({'edge': 'left'});
    $('#sidenav-right').sidenav({'edge': 'right'});
    $('.datepicker').datepicker({
      selectYears: 20,
      i18n: {
                months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"],
                weekdays: ["Domingo","Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
                weekdaysShort: ["Dom","Lun", "Mar", "Mie", "Jue", "Vie", "Sab"],
                weekdaysAbbrev: ["D","L", "M", "M", "J", "V", "S"]
            }
    });
    $('select').not('.disabled').formSelect();
    $('input.autocomplete').autocomplete({
      data: {"Apple": null, "Microsoft": null, "Google": 'http://placehold.it/250x250'},
    });
    $('.tabs').tabs();

    // Chips
    $('.chips').chips();
    $('.chips-initial').chips({
      readOnly: true,
      data: [{
        tag: 'Apple',
      }, {
        tag: 'Microsoft',
      }, {
        tag: 'Google',
      }]
    });
    $('.chips-placeholder').chips({
      placeholder: 'Enter a tag',
      secondaryPlaceholder: '+Tag',
    });
    $('.chips-autocomplete').chips({
      autocompleteOptions: {
        data: {
          'Apple': null,
          'Microsoft': null,
          'Google': null
        }
      },
    });


  }); // end of document ready
})(jQuery); // end of jQuery name space
