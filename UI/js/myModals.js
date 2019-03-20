//Modal for the message 1
// Get the modal
var modal = document.getElementById('DisplayMessage');

// Get the button that opens the modal
var modalBtn  = document.getElementById("message");

// Get the <span> element that closes the modal
var closeBtn = document.getElementsByClassName("closeBtn2")[0];

//listen for click
modalBtn.addEventListener('click', openModal);

//listen for close click
closeBtn.addEventListener('click', closeModal);

//listen for outside click
window.addEventListener('click', clickOutside);

// When the user clicks the button, open the modal
function openModal(){
	modal.style.display = "block";
} 

//function to close modal
function closeModal(){

	modal.style.display = 'none';
}

//function to close modal if outside click

function clickOutside(e){
   if(e.target == modal){
   	modal.style.display = 'none';
   }
	
}


//Modal for the message 2
// Get the modal
var modal = document.getElementById('DisplayMessage');

// Get the button that opens the modal
var modalBtn  = document.getElementById("message2");

// Get the <span> element that closes the modal
var closeBtn = document.getElementsByClassName("closeBtn2")[0];

//listen for click
modalBtn.addEventListener('click', openModal);

//listen for close click
closeBtn.addEventListener('click', closeModal);

//listen for outside click
window.addEventListener('click', clickOutside);

// When the user clicks the button, open the modal
function openModal(){
	modal.style.display = "block";
} 

//function to close modal
function closeModal(){

	modal.style.display = 'none';
}

//function to close modal if outside click

function clickOutside(e){
   if(e.target == modal){
   	modal.style.display = 'none';
   }
	
}
function clickOutside(e){
   if(e.target == modal){
   	modal3.style.display = 'none';
   }
	
}
function mydeleteFunction() {
      confirm("Are you sure you want to delete this incident!");
  }