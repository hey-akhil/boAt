function updatePreview(field, value) {
  switch (field) {
    case 'badge':
      document.getElementById('previewBadge').innerText = value || 'EXTRA ₹100 OFF';
      break;
    case 'playback':
      document.getElementById('previewPlayback').innerText = value || '50 Hrs Playback';
      break;
    case 'rating':
      document.getElementById('previewRating').innerText = value || '4.7';
      break;
    case 'title':
      document.getElementById('previewTitle').innerText = value || 'boAt Airdopes Prime 701 ANC';
      break;
    case 'price':
      document.getElementById('previewPrice').innerText = value ? '₹' + value : '₹1,999';
      break;
    case 'old_price':
      document.getElementById('previewOldPrice').innerText = value ? '₹' + value : '₹7,990';
      break;
    case 'discount':
      document.getElementById('previewDiscount').innerText = value || '75% off';
      break;
  }
}

// Load image from local file into preview card
function previewLocalImage(input) {
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById('previewImage').src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
}