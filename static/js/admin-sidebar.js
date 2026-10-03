/**
 * Jazzmin Admin Scripting: Hash tabs fix + Sidebar grouping
 * 
 * Hash tabs functionality adapted from admin-hash-tabs.js
 * Sidebar grouping adapted from admin-sidebar-grouping.js
 */

/**
 * Function to activate tab based on URL hash
 */
function activateTabFromHash() {
    var hash = window.location.hash;
    if (hash) {
        // Find tab link that matches the hash
        var $tabLink = $('.nav-tabs a[href="' + hash + '"]');
        if ($tabLink.length > 0) {
            $tabLink.tab('show');
        } else {
            // Fallback for ID matching without the tab suffix if necessary
            var $tabById = $('.nav-tabs a[href="' + hash + '-tab"]');
            if ($tabById.length > 0) {
                $tabById.tab('show');
            }
        }
    }
}

/**
 * Jazzmin Sidebar Grouping Script
 * Groups sidebar models into categorized sections with headers
 */
const SIDEBAR_GROUPS = [
    {
        label: 'AKADEMIK',
        items: [
            'Jurusan', 'Kompetensi', 'Mitra Industri', 'Prospek Karir',
            'Fasilitas Jurusan', 'Testimoni Alumni', 'Sertifikasi',
            'Mata Pelajaran'
        ]
    },
    {
        label: 'KEPEGAWAIAN',
        items: [
            'Guru & Staff'
        ]
    },
    {
        label: 'PROGRAM',
        items: [
            'Ekstrakurikuler', 'Kategori Ekskul'
        ]
    },
    {
        label: 'INFORMASI',
        items: [
            'Berita', 'Kategori Berita', 'Pengumuman', 'Kategori Pengumuman', 'File Lampiran'
        ]
    },
    {
        label: 'FASILITAS & INDUSTRI',
        items: [
            'Laboratorium', 'Peralatan Lab'
        ]
    },
    {
        label: 'STATISTIK',
        items: [
            'Statistik Sekolah'
        ]
    }
];

function normalizeText(text) {
    return text.trim().toLowerCase();
}

function applyGrouping() {
    // Jazzmin sidebar uses .nav-sidebar > .nav-item > .nav-link
    // Each model appears as a .nav-item (sometimes nested under app)
    const $navItems = $('.main-sidebar .nav-sidebar .nav-item');
    
    // First, remove any existing group headers we might have added
    $('.sidebar-group-header').remove();
    
    // Collect all model nav-items with their text
    const itemMap = new Map();
    $navItems.each(function() {
        const $link = $(this).find('> .nav-link, > .nav-treeview > .nav-item > .nav-link').first();
        const text = $link.text().trim();
        if (text && !$(this).hasClass('sidebar-group-header')) {
            itemMap.set(normalizeText(text), $(this));
        }
    });

    // Process each group
    let firstGroup = true;
    SIDEBAR_GROUPS.forEach(function(group) {
        let groupItems = [];
        
        group.items.forEach(function(itemName) {
            const normalized = normalizeText(itemName);
            // Try exact match first
            if (itemMap.has(normalized)) {
                groupItems.push(itemMap.get(normalized));
                itemMap.delete(normalized);
            } else {
                // Try partial match
                for (const [key, $item] of itemMap.entries()) {
                    if (key.includes(normalized) || normalized.includes(key)) {
                        groupItems.push($item);
                        itemMap.delete(key);
                        break;
                    }
                }
            }
        });

        if (groupItems.length > 0) {
            // Create header element
            const $header = $('<li class="nav-item sidebar-group-header"></li>');
            $header.html('<p class="nav-header text-xs text-muted font-weight-bold text-uppercase px-3 py-2">' + group.label + '</p>');
            
            // Insert header before first item of this group
            if (!firstGroup) {
                // Add a small separator margin
                $header.css('margin-top', '8px');
            }
            groupItems[0].before($header);
            firstGroup = false;
        }
    });

    // Handle any remaining ungrouped items - put them under "Lainnya"
    const remainingItems = Array.from(itemMap.values());
    if (remainingItems.length > 0) {
        const $header = $('<li class="nav-item sidebar-group-header"></li>');
        $header.html('<p class="nav-header text-xs text-muted font-weight-bold text-uppercase px-3 py-2">LAINNYA</p>');
        $header.css('margin-top', '8px');
        remainingItems[0].before($header);
    }
}

/* ===== DOM Content Loaded ===== */
$(document).ready(function () {
    // Initialize hash tab functionality
    activateTabFromHash();
    
    // Listen for hash changes when navigating between tabs
    $(window).on('hashchange', function () {
        activateTabFromHash();
    });

    // Initialize sidebar grouping
    applyGrouping();
    
    // Also run after potential dynamic loads
    setTimeout(applyGrouping, 500);
    setTimeout(applyGrouping, 1500);
});

/* ===== MutationObserver for dynamic sidebar changes ===== */
const sidebar = document.querySelector('.main-sidebar .nav-sidebar');
if (sidebar) {
    const observer = new MutationObserver(function(mutations) {
        let shouldReapply = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                shouldReapply = true;
            }
        });
        if (shouldReapply) {
            setTimeout(applyGrouping, 100);
        }
    });
    observer.observe(sidebar, { childList: true, subtree: true });
}

/* ===== Background navbar on scroll (from original) ===== */
const navbar = document.getElementById('main-navbar');
const navContainer = document.getElementById('navbar-container');

function updateNavbar() {
    const currentScrollY = window.scrollY;

    if (currentScrollY > 20) {
        if (!navbar.classList.contains('shadow-lg')) {
            navbar.classList.add('shadow-lg', 'bg-white');
            navbar.classList.remove('bg-white/95');
            navContainer.classList.replace('h-20', 'h-16');
        }
    } else {
        if (navbar.classList.contains('shadow-lg')) {
            navbar.classList.remove('shadow-lg', 'bg-white');
            navbar.classList.add('bg-white/95');
            navContainer.classList.replace('h-16', 'h-20');
        }
    }
}

// Initialize state on load
updateNavbar();

window.addEventListener('scroll', updateNavbar, { passive: true });