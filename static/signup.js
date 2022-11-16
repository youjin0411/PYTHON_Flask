function checkOnlyOne(element) {
  
  const checkboxes 
      = document.getElementsByName("chked");
  
  checkboxes.forEach((cb) => {
    cb.checked = false;
  })
  
  element.checked = true;

  let result = '';
  if(event.target.checked)  {
    result = event.target.value;
  }else {
    result = '';
  }
  
  document.getElementById('result').value = result;
}

