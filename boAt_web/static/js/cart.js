function updateQuantity(itemId, action) {
  fetch(`/cart/${action}/${itemId}/`)
    .then(response => response.json())
    .then(data => {
      if (data.removed) {
        // Remove the whole cart item block
        const cartItem = document.querySelector(`#cart-item-${data.removed_item_id}`);
        if (cartItem) {
          cartItem.closest('.cart-item').remove();
        }
      } else {
        // Update quantity input
        document.querySelector(`#qty-${itemId}`).value = data.quantity;

        // Update item total
        const itemTotal = document.querySelector(`#item-total-${itemId}`);
        if (itemTotal) {
          itemTotal.textContent = `₹${data.item_total}`;
        }
      }

      // Update order summary values
      document.querySelector('#subtotal').textContent = `₹${data.subtotal}`;
      document.querySelector('#tax').textContent = `₹${data.tax}`;
      document.querySelector('#shipping').textContent = `₹${data.shipping}`;
      document.querySelector('#total').textContent = `₹${data.total}`;
    })
    .catch(error => {
      console.error('Error updating cart:', error);
    });
}
