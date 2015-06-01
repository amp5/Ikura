$( document).ready(function(){
        console.log("loaded forms.js")

  document.getElementById("new_card").addEventListener("click", function( event ) {
    // display the current click count inside the clicked div
    //event.target.innerHTML = "click count: " + event.detail;

    document.getElementById('add_new_card').insertAdjacentHTML('beforeend', '<br><br>Credit Card Name:' + 
        '<br><input type="text" name="card1_name[]" required id="name"><br>Amount of Debt:<br>' + 
        '<input type="number" step="0.01" min="0" name="card1_debt[]" required id="debt"><br>' +
        'Annual Percentage Rate (APR):<br><input type="number" step="0.01" min="0" name="card1_apr[]" required id="apr">' +
        '<br><label> How is your minimum payment calculated?<select name="min_payment[]" id="min_payment">' + 
        '<option value="int_1per" selected="selected"t>Interest + 1% of the balance</option><option value="2.00_per">2.00%</option>' +
    '<option value="2.08_per">2.08%</option><option value="2.50_per">2.50%</option><option value="2.78_per">2.78%</option>' +
    '<option value="3.00_per">3.00%</option><option value="3.50_per">3.50%</option><option value="4.00_per">4.00%</option>' +
    '<option value="4.50_per">4.50%</option><option value="5.00_per">5.00%</option></select></label><br>' +
    'Select how long you want your payment plan to be: <input type="number" name="card1_date[]" min="1" max="36" id="date"><br><br>');
    console.log(event);
  }, false);
})



