document.addEventListener('DOMContentLoaded', function () {
      const buttons = document.querySelectorAll('.tab-button');
      const products = document.querySelectorAll('.product-item');

      function filterProducts(category) {
        const filter = category.toLowerCase();

        products.forEach(product => {
          const title = product.getAttribute('data-title');
          if (filter === 'all' || title.includes(filter)) {
            product.style.display = '';
          } else {
            product.style.display = 'none';
          }
        });
      }

      buttons.forEach(button => {
        button.addEventListener('click', function () {
          buttons.forEach(btn => btn.classList.remove('active'));
          this.classList.add('active');

          const category = this.getAttribute('data-category');
          filterProducts(category);
        });
      });

      filterProducts('all'); // default on load
    });