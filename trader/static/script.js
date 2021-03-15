function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) {
                c_end = document.cookie.length;
            }
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

$(document).ready(() => {

    console.log('document ready...')

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
    });

    // $(document).on('keypress', function (e) {
    //     if (e.which == 13) {
    //         $('#searchBtn').click()
    //     }
    // });

    // Search for stock data by symbol
    // $('#searchBtn').click(function () {

    //     // preparing payload
    //     var url = "/findstock";
    //     var stock = $("#stockInput").val();
    //     var data = "name=" + stock;

    //     // call to server
    //     $.ajax({
    //         method: "POST",
    //         url: url,
    //         data: data
    //     // data: { csrfmiddlewaretoken: '{{ csrf_token }}'}
    //     }).done(function (resp) {
    //         var json = $.parseJSON(resp);
    //         $("#stockOutput").removeClass("hidden");
    //         console.log("Response data:", json);

    //         var price = json.price;
    //         var prevClose = json.close;
    //         var today = +((prevClose - price).toFixed(2));
    //         $("#stockName").text(json.name);
    //         $("#stockSymbol").text(json.symbol);
    //         $("#stockPrice").text(json.price);
    //         $("#stockToday").text(today);
    //         $("#stockHigh").text(json.high);
    //         $("#stockLow").text(json.low);
    //         //console.log('removing hidden from plotOuptut')
    //         //$("#plotOutput").removeClass("hidden")
    //         // $("#stockVolume").text(json.volume);
    //         // $("#stockCap").text(json.marketCap);
    //         // $("#stockfiftyTwoHigh").text(json.fiftyTwoHigh);
    //         // $("#stockfiftyTwoLow").text(json.fiftyTwoLow);

    //     }).fail(function (resp) {
    //         var json = $.parseJSON(resp);
    //         console.log("Error:", json)
    //         $("#stockName").text("Error: " + json)
    //     })

    // });


    // Buy stocks
    $('#buyBtn').click(() => {

        // preparing payload
        var url = "/buystock";

        var data = {
            symbol: $("#stockSymbol").text(),
            name: $("#stockName").text(),
            shares: $("#stockShares").val(),
            price: $("#stockPrice").text()
        }

        $.ajax({
            type: "POST",
            url: url,
            dataType: 'json',
            data: JSON.stringify(data),
            success: function (resp) {
                console.log('Success: ' + resp.message);
                //location.reload();
                
                // var output = $('#output')
                // var s = "<h1>" + resp.message + "</h1>"
                // output.html(s)

                $("#stockShares").val("")
                $("#result").text(resp.message)
                $("#sharesOwned").text(resp.owned)
                $("#balance").text(resp.balance)
                
            },
            error: function (resp) {
                console.log("Error: " + resp)
                $("#stockShares").val("")
                $("#result").text(resp.message)
            }
        })
    });

    // Sell stocks
    $('#sellBtn').click(() => {

        // preparing payload
        var url = "/sellstock";

        var data = {
            symbol: $("#stockSymbol").text(),
            shares: $("#stockShares").val(), 
            price: $("#stockPrice").text()
        }

        $.ajax({
            type: "POST",
            url: url,
            dataType: 'json',
            data: JSON.stringify(data),
            success: function (resp) {
                console.log('Success: ' + resp.message);
                $("#stockShares").val("")
                $("#result").text(resp.message)
                $("#sharesOwned").text(resp.owned)
                $("#balance").text(resp.balance)
            },
            error: function (resp) {
                console.log("Error: " + resp)
                $("#stockShares").val("")
                $("#result").text(resp.message)
            }
        })
    });

    (function() {
        'use strict';
        window.addEventListener('load', function() {
          // Fetch all the forms we want to apply custom Bootstrap validation styles to
          var forms = document.getElementsByClassName('needs-validation');
          // Loop over them and prevent submission
          var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
              if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
              }
              form.classList.add('was-validated');
            }, false);
          });
        }, false);
      })();
    

});
