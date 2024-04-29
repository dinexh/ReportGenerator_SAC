$(document).ready(function() {
    // Function to handle click event of the preview button
    $('#preview-btn').click(function() {
        // Redirect to the next page for preview
        window.location.href = '/next_page.html';
    });

    $('#activity-form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        // Serialize form data
        var formData = new FormData($(this)[0]);

        // Submit form data via AJAX
        $.ajax({
            type: 'POST',
            url: '/submit_form',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // Display toast message
                var toast = document.createElement('div');
                toast.classList.add('toast');
                toast.innerText = response.message;
                document.body.appendChild(toast);

                // Remove toast after 3 seconds
                setTimeout(function() {
                    toast.style.opacity = '0';
                    setTimeout(function() {
                        document.body.removeChild(toast);
                    }, 1000);
                }, 3000);

                // Trigger download of the generated report
                window.location.href = '/download_report';
            }
        });
    });
});
