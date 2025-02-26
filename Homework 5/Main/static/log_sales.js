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

    // ✅ Fully prevent text inputs from changing cursor during drag
    $("#client, #reams").on("dragenter dragover drop", function (event) {
        event.preventDefault();
        event.stopPropagation();
        $(this).blur(); // Removes focus to prevent cursor change
        $(this).css("cursor", "move"); // ✅ Force cursor to stay "move"
    });

    $("#trash").css({
        "background-color": "#d3d3d3",
        "cursor": "move"
    });
});

// ✅ When dragging starts, force the cursor to "move" globally
function drag(event, id) {
    event.dataTransfer.setData("text/plain", id);

    $("body, input").css("cursor", "move"); // ✅ Force cursor to "move" everywhere

    $(`#sale-${id}`).css("background-color", "#ffffcc");
}

// ✅ Reset cursor after dragging ends
function resetDrag(event, id) {
    $("body, input").css("cursor", "default");

    $(`#sale-${id}`).css("background-color", "");
}

/**
 * Displays the list of sales in the UI.
 */
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

/**
 * Handles processing a new sale.
 */
function processNewSale() {
    const client = $("#client").val().trim();
    const reams = $("#reams").val().trim();

    $("#client-warning").text("").hide();
    $("#reams-warning").text("").hide();

    if (!client) {
        $("#client-warning").text("Client name is required.").show();
        $("#client").focus();
        return;
    }

    if (!reams) {
        $("#reams-warning").text("Number of reams is required.").show();
        $("#reams").focus();
        return;
    }

    if (!/^[0-9]+$/.test(reams)) {
        $("#reams-warning").text("Valid number of reams is required.").show();
        $("#reams").focus();
        return;
    }

    const newSale = { salesperson, client, reams };

    save_sale(newSale);
}

/**
 * Saves a sale via AJAX request.
 */
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
        error: function () {
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
        error: function () {
            alert("Failed to delete sale. Check server logs.");
        }
    });
}

function drag(event, id) {
    event.dataTransfer.setData("text/plain", id);

    $("body").css("cursor", "move");

    $(`#sale-${id}`).css("background-color", "#ffffcc");
}


function resetDrag(event, id) {
    $("body").css("cursor", "default");

    $(`#sale-${id}`).css("background-color", "");
}

$("#trash").css({
    "background-color": "#d3d3d3",
    "cursor": "move"
});

$("#trash").on("dragover", function (event) {
    event.preventDefault();
    $(this).css({
        "background-color": "#ffffcc",
        "cursor": "default"
    });
});

$("#trash").on("dragleave", function () {
    $(this).css({
        "background-color": "#d3d3d3",
        "cursor": "normal"
    });
});

$("#trash").on("drop", function (event) {
    event.preventDefault();
    const id = event.originalEvent.dataTransfer.getData("text/plain");

    delete_sale(parseInt(id));

    $(this).css({
        "background-color": "#d3d3d3",
        "cursor": "move"
    });
});
