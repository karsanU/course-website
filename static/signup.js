function changerUserDisplay() {
  var x = document.getElementById("selectAccType").value;
  if (x === "instructor") {
    document.getElementById("selectInstructors").style.display = "none";
    document.getElementById("selectStudents").style.display = "block";
    document.getElementById("selectStudentsLabel").style.display = "block";
    document.getElementById("selectInstructorsLabel").style.display = "none";

  }
  else if (x === "student") {
    document.getElementById("selectInstructors").style.display = "block";
    document.getElementById("selectStudents").style.display = "none";
    document.getElementById("selectStudentsLabel").style.display = "none";
    document.getElementById("selectInstructorsLabel").style.display = "block";


  }

}
function validateForm() {
  var accType = document.getElementById("selectAccType").value;
  var instructors = document.getElementById("selectInstructors").value;
  var students = document.getElementById("selectStudents").value;
  var username = document.forms["singUpForm"]["username"].value;
  var firstName = document.forms["singUpForm"]["firstName"].value;
  var lastName = document.forms["singUpForm"]["lastName"].value;
  var password1 = document.forms["singUpForm"]["password1"].value;
  var password2 = document.forms["singUpForm"]["password2"].value;
   var message = ""; 

  // check if they chose their students/teachers
  if (accType == "student") {
    if (instructors == '') {
        message += "- You must select at least one instructor.\n";   
    }  
  }
   if (accType == "instructor") {
    if (students == '') {
      message += "- You must select at least one student.\n";  
  }  }
 
   // username
   if (username == ""){
    message += "- Username cannot be empty.\n"   

  // check name is not empty 
  if (firstName == ""){
    message += "- First name cannot be empty.\n";

  }
  if (lastName == ""){
    message += "- Last name cannot be empty.\n";

  }
 

  }
  // password check
  if (password1 == "" & password2 == "" ) {
    message += "- Password cannot be empty.\n"   
  } else if (password1 !== password2) {
    message += "- Password do not match.\n"   
  }


  if (message !== ""){
    alert("Please correct these errors before you can signup: \n" + message)
    return false;
  } 
  
  return true;

}