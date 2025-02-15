const salesperson = "John Doe";
let salesData = [];
let clients = ["Client A", "Client B", "Client C"];

$(document).ready(function() {
    $("#client").autocomplete({
        source: clients
    });

    $("#submit-sale").click(addSale);
    $("#reams").keypress(function(event) {
        if (event.key === "Enter") {
            addSale();
        }
    });
});

function addSale() {
    const client = $("#client").val().trim();
    const reams = $("#reams").val().trim();
    $("#client-warning").text("");
    $("#reams-warning").text("");
    
    if (!client) {
        $("#client-warning").text("Client name is required.");
        $("#client").focus();
        return;
    }
    
    if (!reams || isNaN(reams)) {
        $("#reams-warning").text("Valid number of reams is required.");
        $("#reams").focus();
        return;
    }
    
    if (!clients.includes(client)) {
        clients.push(client);
    }
    
    salesData.unshift({ client, reams, salesperson });
    renderSales();
    $("#client, #reams").val("");
    $("#client").focus();
}

function renderSales() {
    const salesContainer = $("#sales-records");
    salesContainer.empty();
    salesData.forEach((sale, index) => {
        const saleRow = $(
            `<div class='d-flex justify-content-between align-items-center border p-2 mt-2' draggable='true' ondragstart='drag(event, ${index})'>
                <span>${sale.client} - ${sale.reams} reams (by ${sale.salesperson})</span>
                <button class='btn btn-danger btn-sm' onclick='deleteSale(${index})'>Delete</button>
            </div>`
        );
        salesContainer.append(saleRow);
    });
}

function deleteSale(index) {
    salesData.splice(index, 1);
    renderSales();
}

function drag(event, index) {
    event.dataTransfer.setData("text", index);
}

$("#trash").on("dragover", function(event) {
    event.preventDefault();
    $(this).addClass("bg-warning");
});

$("#trash").on("dragleave", function() {
    $(this).removeClass("bg-warning");
});

$("#trash").on("drop", function(event) {
    event.preventDefault();
    const index = event.originalEvent.dataTransfer.getData("text");
    deleteSale(index);
    $(this).removeClass("bg-warning");
});
