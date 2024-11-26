document.addEventListener('DOMContentLoaded', function () {
    fetch('/account')
        .then(response => response.json())
        .then(data => {
            // Display user information
            document.getElementById('user-name').textContent = data.user.firstname;
            document.getElementById('user-phone').textContent = data.user.phonenumber;

            // Display product information
            const productList = document.getElementById('product-list');
            data.products.forEach(product => {
                const productCard = document.createElement('div');
                productCard.className = 'col-md-4 mb-4';

                // Check if picture exists
                let productImage = "";
                if (product.picture) {
                    productImage = product.picture;  // base64 image
                } else {
                    productImage = 'path/to/default/image.jpg';  // fallback image
                }

                productCard.innerHTML = `
                    <div class="card h-100">
                        <img src="${productImage}" class="card-img-top" alt="${product.name}">
                        <div class="card-body">
                            <h5 class="card-title">${product.name}</h5>
                            <p class="card-text">Classification: ${product.classification}</p>
                            <p class="card-text">Price: $${product.price}</p>
                        </div>
                    </div>
                `;
                productList.appendChild(productCard);
            });
        })
        .catch(error => {
            console.error('Error fetching account data:', error);
            alert('An error occurred while loading data.');
        });
});