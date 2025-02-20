const salesperson = "Lindsey Rosales - Best TA and Datadog SWE";

// Load sales and clients from the server on page load
$(document).ready(function () {
    $("#client").autocomplete({ source: clients });

    $("#submit-sale").click(addSale);
    $("#reams").keypress(function (event) {
        if (event.key === "Enter") {
            addSale();
        }
    });

    renderSales(salesData);
});

// Function to render sales list
function renderSales(sales) {
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
                <button class='btn btn-danger btn-sm mt-2 delete-btn' onclick='deleteSale(${sale.id})'>X</button>
            </div>
        `);
        salesContainer.append(saleRow);
    });
}

// Function to add a new sale
function addSale() {
    const client = $("#client").val().trim();
    const reams = $("#reams").val().trim();

    if (!client || !reams || !/^[0-9]+$/.test(reams)) {
        alert("Invalid input.");
        return;
    }

    const newSale = { salesperson, client, reams };

    $.ajax({
        url: "/save_sale",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(newSale),
        success: function (response) {
            renderSales(response.sales);
            $("#client").autocomplete({ source: response.clients });
            $("#client, #reams").val("");
        },
        error: function () {
            console.error("Error saving sale.");
        }
    });
}

// Function to delete a sale
function deleteSale(id) {
    $.ajax({
        url: "/delete_sale",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ id }),
        success: function (response) {
            renderSales(response.sales);
        },
        error: function () {
            console.error("Error deleting sale.");
        }
    });
}

// Drag-and-drop delete functionality
function drag(event, id) {
    event.dataTransfer.setData("text", id);
}

$("#trash").on("dragover", function (event) {
    event.preventDefault();
    $(this).addClass("bg-warning").css("cursor", "grabbing");
});

$("#trash").on("dragleave", function () {
    $(this).removeClass("bg-warning").css("cursor", "default");
});

$("#trash").on("drop", function (event) {
    event.preventDefault();
    const id = event.originalEvent.dataTransfer.getData("text");
    deleteSale(id);
    $(this).removeClass("bg-warning").css("cursor", "default");
});
