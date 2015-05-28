// """I want this .js script to take new user entered values for cards 
// and update the db and 
// then re-run calculations 
// and display new table and new D3"""





 $(function() {
    $('form#submit_update').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/dashboard', {
        names: $('input[name="names"]').val(),
        debts: $('input[name="debts"]').val(), 
        aprs: $('input[name="aprs"]').val(),
        dates: $('input[name="dates"]').val(),
        min_payment: $('input[name="min_payment"]').val(),
        session: $('input[name="session"]').val(),
        user_id: $('input[name="user_id"]').val()
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
  });