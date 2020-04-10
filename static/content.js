function validateRemark() {
    var newMark = document.forms["regradeForm"]["newMark"].value;
    if ((newMark < 101) && (newMark >= 0) && newMark != "") {
        return true;
    } 
    alert("Mark must be between 0 and 100")
    return false;

}

// function that creates the collapsable view for the instructor's view feedback page. 
document.addEventListener('DOMContentLoaded', function () {
    var collapsible = document.getElementsByClassName("collapsible");
    var i;
    for (i = 0; i < collapsible.length; i++) {
        collapsible[i].addEventListener("click", function () {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
}, false);

// makes sure the user is not submitting empty feedback messages. 
function validateFeedback() {

    var q1 = document.forms["feedbackForm"]["q1"].value;
    var q2 = document.forms["feedbackForm"]["q2"].value;
    var q3 = document.forms["feedbackForm"]["q3"].value;
    var q4 = document.forms["feedbackForm"]["q4"].value;

    if (q1 != "" && q2 != "" && q3 != "" && q4 != "" ) {
        return true;
    }
    alert("Please answer all the feedback questions.")
    return false;

}