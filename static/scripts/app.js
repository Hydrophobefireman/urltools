
(function() {
  'use strict';

  var app = {
    isLoading: true,

  };

    if (app.isLoading) {
      app.spinner.setAttribute('hidden', true);
      app.container.removeAttribute('hidden');
      app.isLoading = false;
    }
  };



  if ('serviceWorker' in navigator) {
    navigator.serviceWorker
             .register('./static/service-worker.js')
             .then(function() { console.log('Service Worker Registered'); });
  }
})();
