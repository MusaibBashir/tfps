// Main JavaScript file
document.addEventListener('DOMContentLoaded', function() {
    // Fix for mobile dropdown navigation
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    
    if (window.innerWidth < 768) {
        dropdowns.forEach(dropdown => {
            dropdown.addEventListener('click', function(e) {
                e.preventDefault();
                const dropdownContent = this.nextElementSibling;
                
                // Close all other dropdowns
                document.querySelectorAll('.dropdown-content').forEach(content => {
                    if (content !== dropdownContent) {
                        content.style.display = 'none';
                    }
                });
                
                // Toggle the clicked dropdown
                dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
            });
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.matches('.dropdown-toggle')) {
                const dropdowns = document.querySelectorAll('.dropdown-content');
                dropdowns.forEach(dropdown => {
                    dropdown.style.display = 'none';
                });
            }
        });
    }
    
    // Add active class to current page in navigation
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        
        if (currentLocation === linkPath || 
            (currentLocation.includes('/members') && linkPath.includes('/members')) ||
            (currentLocation.includes('/cameras') && linkPath.includes('/cameras')) ||
            (currentLocation.includes('/events') && linkPath.includes('/events'))) {
            link.classList.add('active');
        }
    });
    
    // Enable sorting on tables if present
    if (document.querySelector('table')) {
        makeSortable();
    }
});

// Function to make tables sortable
function makeSortable() {
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        
        headers.forEach((header, index) => {
            header.addEventListener('click', () => {
                const direction = header.classList.contains('sort-asc') ? 'desc' : 'asc';
                
                // Remove sort classes from all headers
                headers.forEach(h => {
                    h.classList.remove('sort-asc', 'sort-desc');
                });
                
                // Add sort class to current header
                header.classList.add(`sort-${direction}`);
                
                // Sort the table
                sortTable(table, index, direction);
            });
            
            // Add cursor and hover effect
            header.style.cursor = 'pointer';
            header.addEventListener('mouseover', () => {
                header.style.backgroundColor = '#2980b9';
            });
            header.addEventListener('mouseout', () => {
                header.style.backgroundColor = '#3498db';
            });
        });
    });
}

// Function to sort table
function sortTable(table, columnIndex, direction) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sortedRows = rows.sort((a, b) => {
        const aValue = a.querySelectorAll('td')[columnIndex].textContent.trim();
        const bValue = b.querySelectorAll('td')[columnIndex].textContent.trim();
        
        // Check if values are numbers
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return direction === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
        // Sort as strings
        return direction === 'asc' 
            ? aValue.localeCompare(bValue) 
            : bValue.localeCompare(aValue);
    });
    
    // Remove existing rows
    rows.forEach(row => {
        tbody.removeChild(row);
    });
    
    // Add sorted rows
    sortedRows.forEach(row => {
        tbody.appendChild(row);
    });
}
