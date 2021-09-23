

function courseNameValidator() {
    let courseName = document.getElementById("courseName");
    let courseNameErrorMessage = document.getElementById("nameMessage");
    // not equal zero
    if (!courseName.value.length) {
        courseName.classList.add("is-invalid");
        courseNameErrorMessage.innerHTML = "Please choose a course name.";
    }
    else if (!isNaN(courseName.value)) {
        courseName.classList.add("is-invalid");
        courseNameErrorMessage.innerHTML = "Enter a whole course name.";
    } else {
        courseName.classList.remove("is-invalid");
        courseName.classList.add("is-valid");
        return true;
    }
    return false;
}

function courseNumebrValidator() {
    let courseNumber = document.getElementById("courseNumber")
    let courseNumberV = courseNumber.value
    let courseNumberErrorMessage = document.getElementById("numberMessage");
    
    if (!courseNumberV.length) {
        courseNumber.classList.add("is-invalid");
        courseNumberErrorMessage.innerHTML = "Please enter a course number.";
    } else if (isNaN(courseNumberV)) {
        courseNumber.classList.add("is-invalid");
        courseNumberErrorMessage.innerHTML = "Enter a whole course number.";
    } else if (parseInt(courseNumberV) <= 100) {
        courseNumber.classList.add("is-invalid");
        courseNumberErrorMessage.innerHTML = "Course number should be bigger than 100.";
    } else if (parseInt(courseNumberV) >= 10000) {
        courseNumber.classList.add("is-invalid");
        courseNumberErrorMessage.innerHTML = "Course number should be less than 10000.";
    } else {
        courseNumber.classList.remove("is-invalid");
        courseNumber.classList.add("is-valid");
        return true;
    }
    return false;
}

function checkValidation() {
    let checks = document.getElementsByClassName("form-check-input")
    checks = [...checks]

    checks.forEach(check => {
        if (check.checked) {
            check.classList.remove("is-invalid")
            check.classList.add("is-valid")
        } else {
            check.classList.add("is-invalid")
            check.classList.remove("is-valid")
        }
    })
    return checks.every((check) => check.checked)
}

function addCourseValidation() {
    
    let validationArray = [
        courseNameValidator(),
        courseNumebrValidator(),
        checkValidation(),
    ];
    return validationArray.every((elm)=> elm);
}

(function() {
    'use strict';
    window.addEventListener('load', function() {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        let forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
            if (form.id == "addCourseForm") {
                if (!addCourseValidation()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
            }
        }, false);
        });
    }, false);
    })();