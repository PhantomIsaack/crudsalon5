const deleteButtons = document.querySelectorAll('.btn-delete');

deleteButtons.forEach((btn) => {
  btn.addEventListener('click', (e) => {
    if (!confirm('Are you sure you want to delete this record?')) {
      e.preventDefault(); 
    }
  });
});
