function checkOnlyOne(element) {
  
  const checkboxes 
      = document.getElementsByName("chked");
  
  checkboxes.forEach((cb) => {
    cb.checked = false;
  })
  
  element.checked = true;
}

