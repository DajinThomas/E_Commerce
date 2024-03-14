// Function to open the popup and display product details
function openPopup(productId) {
    // AJAX request to fetch product details
    fetch(`/get_product_details/${productId}/`)
        .then(response => response.json())
        .then(data => {
            // Update popup content with product details
            document.getElementById('product-name').innerText = data.name;
            document.querySelector('.product-description').innerText = `Description: ${data.description}`;
            document.querySelector('.product-price').innerText = `Price: ${data.price}`;
            document.querySelector('.product-category').innerText = `Category: ${data.category}`;

            // Display the popup
            document.getElementById("popup").style.display = "block";
        })
        .catch(error => console.error('Error fetching product details:', error));
}

// Function to close the popup
function closePopup() {
    document.getElementById("popup").style.display = "none";
}
