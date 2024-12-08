import "./style.css";

const goButton: HTMLButtonElement = document.getElementById(
  "submit",
) as HTMLButtonElement;


//doesn't show the stuff, or work
function runPHP() {
  $.ajax({

    url : './index.php',
    type : 'POST',
    success : function (result) {
       console.log (result); // Here, you need to use response by PHP file.
    },
    error : function () {
       console.log ('error');
    }

  });
}


function runPHP2() {
  fetch('call_sql_model.py', {
    method: 'POST'
  })
    .then(response => response.text())
    .then(result => {
      console.log(result);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

goButton.addEventListener("click", runPHP);

//keeping this for now just in case we have time to add JS

