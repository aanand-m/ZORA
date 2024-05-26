const button = document.getElementById("run-spider");
const loader = document.getElementsByClassName("loader-result");
const result = document.getElementsByClassName("result")

button.addEventListener("click", () => {
  result.style.display = "none";
//   loader.style.display = "block";
});


// $(document).ready(function() {
      //     $("#runScriptButton").click(function() {
      //         $.ajax({
      //             type: "POST",
      //             url: "{{ url_for('run_script') }}", // Your route to trigger script execution
      //             success: function(response) {
      //                 $("#result").html(response); // Update a part of the page with the response
      //             }
      //         });
      //     });
      // });