const salesperson = "Lindsey Rosales - Best TA and Datadog SWE";

$(document).ready(function () {
    console.log("✅ log_sales.js has loaded!");
    console.log("✅ Checking salesData:", window.salesData);
    console.log("✅ Checking clients:", window.clients);

    $("#client").autocomplete({ source: window.clients });

    $("#submit-sale").click(processNewSale);
    $("#reams").keypress(function (event) {
        if (event.key === "Enter") {
            processNewSale();
        }
    });

    // ✅ Load sales data from the server on page load
    display_sales_list(window.salesData);
});

/**
 * Displays the list of sales in the UI.
 * @param {Array} sales - List of sales received from the server.
 */
function display_sales_list(sales) {
    const salesContainer = $("#sales-records");
    salesContainer.empty();

    if (sales.length === 0) {
        salesContainer.append("<p>No sales recorded yet.</p>");
        return;
    }

    sales.forEach((sale) => {
        const saleRow = $(`
            <div class='d-flex flex-column border p-3 mt-2 sale-row' draggable='true' 
                ondragstart='drag(event, ${sale.id})' style='cursor: move; width: 100%;'>
                <span><strong>${sale.salesperson}</strong></span>
                <span>Client: ${sale.client}</span>
                <span>Reams: ${sale.reams}</span>
                <button class='btn btn-danger btn-sm mt-2 delete-btn' onclick='delete_sale(${sale.id})'>X</button>
            </div>
        `);
        salesContainer.append(saleRow);
    });

    $(".sale-row").hover(
        function() {
            $(this).css("background-color", "lightyellow");
        }, 
        function() {
            $(this).css("background-color", "");
        }
    );
}

/**
 * Processes a new sale from user input.
 */
function processNewSale() {
    const client = $("#client").val().trim();
    const reams = $("#reams").val().trim();

    // Ensure warning spans exist
    if ($("#reams-warning").length === 0) {
        $("#reams").after("<span id='reams-warning' class='text-danger'></span>");
    }
    if ($("#client-warning").length === 0) {
        $("#client").after("<span id='client-warning' class='text-danger'></span>");
    }

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

    console.log("📤 Sending new sale to server:", newSale);
    save_sale(newSale);
}

/**
 * Sends a new sale to the server and updates the UI.
 * @param {Object} new_sale - The new sale data.
 */
function save_sale(new_sale) {
    $.ajax({
        url: "/save_sale",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(new_sale),
        success: function (response) {
            console.log("✅ Sale saved successfully:", response);
            display_sales_list(response.sales);
            $("#client").autocomplete({ source: response.clients });
            $("#client, #reams").val("");  // Clear input fields
        },
        error: function (xhr, status, error) {
            console.error("❌ Error saving sale:", xhr.responseText);
            alert("Failed to save sale. Check server logs.");
        }
    });
}

/**
 * Deletes a sale and updates the UI.
 * @param {number} id - The sale ID to delete.
 */
function delete_sale(id) {
    $.ajax({
        url: "/delete_sale",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ id }),
        success: function (response) {
            console.log("✅ Sale deleted successfully.");
            display_sales_list(response.sales);
        },
        error: function (xhr, status, error) {
            console.error("❌ Error deleting sale:", xhr.responseText);
            alert("Failed to delete sale. Check server logs.");
        }
    });
}

/**
 * Handles dragging a sale item.
 * @param {Event} event - Drag event.
 * @param {number} id - Sale ID being dragged.
 */
function drag(event, id) {
    event.dataTransfer.setData("text", id);
}

// Handle drag-over behavior on trash bin
$("#trash").on("dragover", function (event) {
    event.preventDefault();
    $(this).addClass("bg-warning").css("cursor", "grabbing");
});

// Handle drag-leave on trash bin
$("#trash").on("dragleave", function () {
    $(this).removeClass("bg-warning").css("cursor", "default");
});

// Handle drop event to delete a sale
$("#trash").on("drop", function (event) {
    event.preventDefault();
    const id = event.originalEvent.dataTransfer.getData("text");
    delete_sale(id);
    $(this).removeClass("bg-warning").css("cursor", "default");
});
