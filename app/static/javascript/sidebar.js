document.getElementById('admin-item').addEventListener('click', function () {
    toggleSubMenu('admin-submenu');
  });
  
  document.getElementById('developers-item').addEventListener('click', function () {
    toggleSubMenu('developers-submenu');
  });
  
  function toggleSubMenu(subMenuId) {
    var subMenu = document.getElementById(subMenuId);
    if (subMenu.style.display === 'block') {
      subMenu.style.display = 'none';
    } else {
      subMenu.style.display = 'block';
    }
  }
  