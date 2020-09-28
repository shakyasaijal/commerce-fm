// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    "lengthMenu": [[20, 45, 100, -1], [20, 45, 100, "All"]]
  });
});
