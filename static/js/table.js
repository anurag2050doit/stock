var renderResponse = function (data) {
  $('#myTable').dataTable({
    data: data,
    searching: false,
    destroy: true,
    columns: [
      {'data': 'name'},
      {
        'data': 'open',
        'searchable': false,
        'sortable': false
      },
      {
        'data': 'high',
        'searchable': false,
        'sortable': false
      },
      {
        'data': 'low',
        'searchable': false,
        'sortable': false
      },
      {
        'data': 'code',
        'searchable': false,
        'sortable': false
      }
    ]
  })
};

$(document).ready(function () {
  $.ajax({
    url: '/api',
    method: 'get',
    dataType: 'json',
    contentType: 'application/json',
    success: renderResponse
  });

  $('form').submit(function (event) {
    event.preventDefault();
    var formData = {
      'search': $('input[name=search]').val()
    };
    $.ajax({
      url: '/api',
      method: 'post',
      dataType: 'json',
      data: JSON.stringify(formData),
      contentType: 'application/json',
      success: renderResponse
    })
  });
});

