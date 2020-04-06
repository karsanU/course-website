function myFunction() {
    var x = document.changerUserDisplay("selectAccType").value;

    if (x==="instructor"){
      document.getElementById("selectInstructors").style.display = "none"; 
      document.getElementById("selectStudents").style.display = "block"; 
      document.getElementById("selectStudentsLabel").style.display = "block"; 
      document.getElementById("selectInstructorsLabel").style.display = "none"; 


    }
    else if (x==="student"){
      document.getElementById("selectInstructors").style.display = "block"; 
      document.getElementById("selectStudents").style.display = "none"; 
      document.getElementById("selectStudentsLabel").style.display = "none"; 
      document.getElementById("selectInstructorsLabel").style.display = "block"; 


    }
};


function checkForm()
{
	if (value of first field is or isn't something)
	{
		// something is wrong
		alert('There is a problem with the first field');
		return false;
	}
	else if (value of next field is or isn't something)
	{
		// something else is wrong
		alert('There is a problem with...');
		return false;
	}
	// If the script gets this far through all of your fields
	// without problems, it's ok and you can submit the form

	return true;
}