/* Fires an API call to the server and adds the reported city as an alien city
  */


document.addEventListener('DOMContentLoaded', function() {
    // Show the modal when "Apply Now" is clicked
    document.querySelectorAll('.apply-now').forEach(function(button) {
        button.addEventListener('click', function() {
            var myModal = new bootstrap.Modal(document.getElementById('applyModal'));
            myModal.show();
        });
    });

 /*   $("#apply-form").on("submit", function(event) {
        event.preventDefault();
        var form = document.getElementById('candidateForm');
    
        var formData = new FormData(this);  // Create a FormData object
    
        $.ajax({
            url: '/server/ApplicationHRappfun/add',
            method: 'POST',
            data: formData,
            processData: false,  // Important to prevent jQuery from processing the data
            contentType: false,  // Important to prevent jQuery from setting contentType
            success: function(response) {
                console.log('Success:', response);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });


    document.getElementById('apply-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        postcandidate();
    });
    
    function postcandidate() {
        var name = $("#name").val();
        var email = $("#email").val();
        var dataToSend = {
            name: name,
            email: email
        };
     //   formData.append('name', $("#name").val());
       // formData.append('email', $("#email").val());
     //   var resumeFile = $("#resume")[0].files[0];
       // formData.append('resume', resumeFile);
       // var dataToSend = {
       //     name: name,
        //    email: email
        //};
     
        // Fires an Ajax call to the URL defined in the index.js function file
    // All URLs to the Advanced I/O function will be of the pattern: /server/{function_name}/{url_path}
        $.ajax({
            url: "/server/ApplicationHRappfun/add",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({
                "name": name,
                "email": email
            }),
            success: function (data) {
                alert(data.message);
                console.log(data);
            },
            error: function (error) {
                console.log('error in add')
                alert(error.message);
                console.log('Error:',error);
            }
        });
    }*/


    // Handle form submission
    document.getElementById('apply-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        


        var formData = new FormData(this);

        fetch('https://aliencity-60032381908.development.catalystserverless.in/server/ApplicationHRappfun/add', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Response Status:', response.status);
            const contentType = response.headers.get('Content-Type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                return response.text();  // Handle non-JSON responses
            }
        })
        .then(responseText => {
            console.log('Raw Response:', responseText);  // Log the raw response
            let data;
            try {
                data = typeof responseText === 'string' ? JSON.parse(responseText) : responseText;
            } catch (e) {
                console.error('Error parsing response:', e);
                alert('Error: Unable to parse the response.');
                return;
            }
            if (data.error) {
                console.error('Server Error:', data.error);
                alert('Error: ' + (data.error || 'An error occurred'));
            } else if (data.message) {
                alert(data.message || 'Success');
                var myModal = bootstrap.Modal.getInstance(document.getElementById('applyModal'));
                myModal.hide(); // Hide the modal
                //window.location.href = 'hr_view.html'; // Redirect to hr_view.html
            } else {
                console.error('Unexpected response format:', data);
                alert('Error: Unexpected response format.');
            }
            })
            .catch(error=>{
            console.error('Error: console', error);
            //window.location.href = 'hr_view.html';
            alert('Error: Unable to Complete the request')
            });
        });    
    });

/*document.getElementById('apply-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    postcandidate();
});

function postcandidate() {
    var name = $("#name").val();
	var email = $("#email").val();
    var dataToSend = {
        name: name,
        email: email
    };
 
    // Fires an Ajax call to the URL defined in the index.js function file
// All URLs to the Advanced I/O function will be of the pattern: /server/{function_name}/{url_path}
    $.ajax({
        url: "/server/ApplicationHRappfun/app",
        type: "post",
        contentType: "application/json",
        data: JSON.stringify({
            "name": name,
			"email": email
        }),
        success: function (data) {
            alert(data.message);
        },
        error: function (error) {
            alert(error.message);
        }
    });
}*/

document.getElementById('apply-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    var formData = new FormData(document.getElementById('apply-form'));

    fetch('/server/ApplicationHRappfun/add', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        console.log(data);
    })
    .catch(error => {
        console.log('Error:', error);
        alert('Error: ' + error.message);
    });
});