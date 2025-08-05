document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.tab-button');
  const products = document.querySelectorAll('.product-item');
  const countDisplay = document.getElementById('productCount');

  function filterProducts(category) {
    let count = 0;
    products.forEach(item => {
      const title = item.getAttribute('data-title');
      if (category === 'All' || title.includes(`- ${category}`)) {
        item.style.display = '';
        count++;
      } else {
        item.style.display = 'none';
      }
    });
    countDisplay.textContent = count;
  }

  buttons.forEach(btn => {
    btn.addEventListener('click', function () {
      // Remove active from all
      buttons.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const category = this.getAttribute('data-category');
      filterProducts(category);
    });
  });

  // Initial count
  filterProducts('All');
});