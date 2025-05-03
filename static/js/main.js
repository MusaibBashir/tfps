// Main JavaScript file
document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    
    if (window.innerWidth < 768) {
        dropdowns.forEach(dropdown => {
            dropdown.addEventListener('click', function(e) {
                e.preventDefault();
                const dropdownContent = this.nextElementSibling;
            
                document.querySelectorAll('.dropdown-content').forEach(content => {
                    if (content !== dropdownContent) {
                        content.style.display = 'none';
                    }
                });
                
                
                dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
            });
        });
        
        document.addEventListener('click', function(e) {
            if (!e.target.matches('.dropdown-toggle')) {
                const dropdowns = document.querySelectorAll('.dropdown-content');
                dropdowns.forEach(dropdown => {
                    dropdown.style.display = 'none';
                });
            }
        });
    }
    
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
    
    if (document.querySelector('table')) {
        makeSortable();
    }
});

function makeSortable() {
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
        const headers = table.querySelectorAll('th');
        
        headers.forEach((header, index) => {
            header.addEventListener('click', () => {
                const direction = header.classList.contains('sort-asc') ? 'desc' : 'asc';
                
        
                headers.forEach(h => {
                    h.classList.remove('sort-asc', 'sort-desc');
                });
                
            
                header.classList.add(`sort-${direction}`);
                
            
                sortTable(table, index, direction);
            });
            
           
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


function sortTable(table, columnIndex, direction) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const sortedRows = rows.sort((a, b) => {
        const aValue = a.querySelectorAll('td')[columnIndex].textContent.trim();
        const bValue = b.querySelectorAll('td')[columnIndex].textContent.trim();
        
      
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return direction === 'asc' ? aNum - bNum : bNum - aNum;
        }
        
   
        return direction === 'asc' 
            ? aValue.localeCompare(bValue) 
            : bValue.localeCompare(aValue);
    });

    rows.forEach(row => {
        tbody.removeChild(row);
    });

    sortedRows.forEach(row => {
        tbody.appendChild(row);
    });
}
