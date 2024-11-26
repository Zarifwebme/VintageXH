// Show specific section
function showSection(sectionId) {
    $('#dashboard, #products, #users').hide();
    $('#' + sectionId).show();
}
// Function to get the total number of products and display it on the site
async function displayProductCount() {
    try {
        const response = await fetch('/get_product_count');
        const data = await response.json();
        document.getElementById('totalProducts').innerText = data.count;
    } catch (error) {
        console.error("Error fetching product count:", error);
    }
}

// Call the function to display the product count
displayProductCount();
// Load product data and render products table
async function loadProducts() {
    // Load products
    const productData = await fetch('/get_products');
    const products = await productData.json();
    $('#productTable').empty();
    products.forEach(product => {
        $('#productTable').append(`
            <tr>
                <td>${product.name}</td>
                <td>${product.price}</td>
                <td>${product.classification}</td>
                <td><img src="${product.picture}" class="img-thumbnail" width="50"></td>
                <td>
                    <button class="btn btn-info" onclick="editProduct(${product.id})">Edit</button>
                    <button class="btn btn-danger" onclick="deleteProduct(${product.id})">Delete</button>
                </td>
            </tr>
        `);
    });
}
loadProducts

// Delete product function
async function deleteProduct(productId) {
    try {
        const response = await fetch(`/delete_product/${productId}`, { method: 'DELETE' });
        const result = await response.json();
        alert(result.message);
        loadProducts(); // Reload products after deletion
    } catch (error) {
        console.error("Error deleting product:", error);
    }
}

// Load users data and render users table (uncomment if needed)
// async function loadUsers() {
//     try {
//         const userData = await fetch('/get_users');
//         const users = await userData.json();
//         $('#userTable').empty();
//         users.forEach(user => {
//             $('#userTable').append(`
//                 <tr>
//                     <td>${user.firstname}</td>
//                     <td>${user.phonenumber}</td>
//                     <td><button class="btn btn-danger" onclick="deleteUser(${user.id})">Delete</button></td>
//                 </tr>
//             `);
//         });
//     } catch (error) {
//         console.error("Error loading users:", error);
//     }
// }

// Handle adding product through the form
document.getElementById('addProductForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    try {
        const response = await fetch('/add_product', { method: 'POST', body: formData });
        const data = await response.json();
        alert(data.message || data.error);
        loadProducts(); // Reload products after adding
    } catch (error) {
        console.error("Error adding product:", error);
    }
});

// Function to open the update modal and populate it with product data
function editProduct(productId) {
    // Fetch product details and populate the form fields
    fetch(`/get_product/${productId}`)
        .then(response => response.json())
        .then(data => {
            $('#updateProductId').val(data.id);
            $('#updateProductName').val(data.name);
            $('#updateProductPrice').val(data.price);
            $('#updateProductClassification').val(data.classification);
            $('#updateProductModal').modal('show'); // Show modal
        })
        .catch(error => console.error('Error fetching product:', error));
}

// Event listener for updating product
document.getElementById('updateProductForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const productId = $('#updateProductId').val();
    const formData = new FormData(this); // Create FormData from the form

    fetch(`/update_product/${productId}`, {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Display success message
        $('#updateProductModal').modal('hide'); // Hide the modal
        loadProducts(); // Refresh the product table
    })
    .catch(error => console.error('Error updating product:', error));
});

document.getElementById('searchButton').addEventListener('click', function() {
    const query = document.getElementById('searchQuery').value;
    fetch(`/search_products?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('searchResults');
            resultsContainer.innerHTML = ''; // Clear previous results
            if (data.length > 0) {
                data.forEach(product => {
                    const productElement = document.createElement('div');
                    productElement.classList.add('product');
                    productElement.innerHTML = `
                        <h5>${product.name}</h5>
                        <p>Price: $${product.price}</p>
                        <p>Classification: ${product.classification}</p>
                        <img src="${product.picture}" alt="${product.name}" class="img-thumbnail" style="max-width: 150px;">
                    `;
                    resultsContainer.appendChild(productElement);
                });
            } else {
                resultsContainer.innerHTML = '<p>No products found.</p>';
            }
        })
        .catch(error => console.error('Error:', error));
});

document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/register', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            this.reset();
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            this.reset();
        }
    })
    .catch(error => console.error('Error:', error));
});
// Function to delete a user
async function deleteUser(userId) {
    try {
        const response = await fetch(`/delete_user/${userId}`, { method: 'DELETE' });
        const result = await response.json();
        alert(result.message);
        loadUsers(); // Reload users after deletion
    } catch (error) {
        console.error("Error deleting user:", error);
    }
}
function loadUsers() {
    fetch('/get_users')
        .then(response => response.json())
        .then(data => {
            const userTable = document.getElementById('userTable');
            userTable.innerHTML = ''; // Clear previous data
            data.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.firstname}</td>
                    <td>${user.phonenumber}</td>
                    <td>
                        <button class="btn btn-danger" onclick="deleteUser(${user.id})">Delete</button>
                    </td>
                `;
                userTable.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Call loadUsers when the page loads
document.addEventListener('DOMContentLoaded', loadUsers);

// Function to get the total number of users and display it on the site
async function displayUserCount() {
    try {
        const response = await fetch('/get_user_count');
        const data = await response.json();
        document.getElementById('totalUsers').innerText = data.count;
    } catch (error) {
        console.error("Error fetching user count:", error);
    }
}

// Call the function to display the user count
displayUserCount();

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.error) {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Initial page load setup
$(document).ready(() => {
    loadProducts();
    showSection('dashboard');
});

