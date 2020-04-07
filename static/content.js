function validateRemark(){

    var newMark = document.forms["regradeForm"]["newMark"].value;
    if((newMark < 101) && (newMark >= 0)){
        return true;
    }
    alert("Mark must be between 0 and 100")
    return false; 

}