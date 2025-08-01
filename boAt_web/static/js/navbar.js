  // Mobile search toggle
  const toggleBtn = document.getElementById("mobileSearchToggle");
  const searchBar = document.getElementById("mobileSearchBar");

  toggleBtn.addEventListener("click", () => {
    searchBar.classList.toggle("d-none");
  });

  // Rotating placeholder logic
  const placeholders = [
    'Search "Smartwatch"',
    'Search "Earphone"',
    'Search "Speaker"',
    'Search "Neckband"',
    'Search "Power Bank"',
  ];

  let index = 0;

  function rotatePlaceholder() {
    const desktopInput = document.getElementById("searchInput");
    const mobileInput = document.getElementById("mobileSearchInput");

    if (desktopInput) desktopInput.placeholder = placeholders[index];
    if (mobileInput) mobileInput.placeholder = placeholders[index];

    index = (index + 1) % placeholders.length;
  }

  setInterval(rotatePlaceholder, 1000); // Every 3 seconds
  rotatePlaceholder(); // Initial run