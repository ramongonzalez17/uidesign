const salesperson = "Lindsey Rosales - Best TA and Datadog SWE";  
$(document).ready(function () {
    $("#client").autocomplete({ source: window.clients });

    $("#submit-sale").click(processNewSale);

    $("#client, #reams").keypress(function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); 
            processNewSale();
        }
    });

    display_sales_list(window.salesData);
});

function display_sales_list(sales) {
    const salesContainer = $("#sales-records");
    salesContainer.empty();

    if (sales.length === 0) {
        salesContainer.append("<tr><td colspan='4' class='text-center'>No sales recorded yet.</td></tr>");
        return;
    }

    sales.forEach((sale) => {
        const saleRow = $(`
            <tr id="sale-${sale.id}" draggable='true' ondragstart='drag(event, ${sale.id})' ondragend='resetDrag(event, ${sale.id})' style='cursor: move;'>
                <td><strong>${sale.salesperson}</strong></td>
                <td>${sale.client}</td>
                <td>${sale.reams}</td>
                <td>
                    <button class='btn btn-danger btn-sm' onclick='delete_sale(${sale.id})'>X</button>
                </td>
            </tr>
        `);
        salesContainer.append(saleRow);
    });
}


function processNewSale() {
    const client = $("#client").val().trim();
    const reams = $("#reams").val().trim();

    $("#client-warning").text("").hide();
    $("#reams-warning").text("").hide();

    if (!client) {
        $("#client-warning").text("Client name is required.").show();
        $("#client").focus();
        hasError = true;
    }

    if (!reams) {
        $("#reams-warning").text("Number of reams is required.").show();
        $("#reams").focus();
        hasError = true;
    }

    if (!/^[0-9]+$/.test(reams)) {
        $("#reams-warning").text("Valid number of reams is required.").show();
        $("#reams").focus();
        hasError = true;
    }

    const newSale = { salesperson, client, reams };

    save_sale(newSale);
}

function save_sale(new_sale) {
    $.ajax({
        url: "/save_sale",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(new_sale),
        success: function (response) {
            display_sales_list(response.sales);
            $("#client").autocomplete({ source: response.clients });

            $("#client, #reams").val(""); 

            $("#client").focus(); 
        },
        error: function (xhr, status, error) {
            alert("Failed to save sale. Check server logs.");
        }
    });
}

function delete_sale(id) {
    $.ajax({
        url: "/delete_sale",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ id }),
        success: function (response) {
            display_sales_list(response.sales);
        },
        error: function (xhr, status, error) {
            alert("Failed to delete sale. Check server logs.");
        }
    });
}

function drag(event, id) {
    event.dataTransfer.setData("text/plain", id);

    $(`#sale-${id}`).css("background-color", "yellow");
}

function resetDrag(event, id) {
    $(`#sale-${id}`).css("background-color", "");  
}

$("#trash").on("dragover", function (event) {
    event.preventDefault();
    $(this).css({
        "background-color": "red",
        "cursor": "grabbing"
    });
});

$("#trash").on("dragleave", function () {
    $(this).css({
        "background-color": "grey",
        "cursor": "default"
    });
});

$("#trash").on("drop", function (event) {
    event.preventDefault();
    const id = event.originalEvent.dataTransfer.getData("text/plain");

    delete_sale(parseInt(id));

    $(this).css({
        "background-color": "grey",
        "cursor": "default"
    });
});
